"""Module """
import json
from pathlib import Path
import re
import datetime

from .order_request import OrderRequest
from .order_management_exception import OrderManagementException
from .order_shipping import OrderShipping


class OrderManager:
    """Class for providing the methods for managing the orders"""

    def __init__(self):
        pass

    def register_order(
        self, product_id, delivery_address, order_type, phone_number, zip_code
    ): # pylint: disable=too-many-arguments
        """Register a new order in the system"""
        if not self.validate_ean13(product_id):
            raise OrderManagementException("Invalid EAN13 code")
        if order_type not in ["Regular", "Premium"]:
            raise OrderManagementException("Invalid order type")
        if not self.validate_address(delivery_address):
            raise OrderManagementException("Invalid delivery address")
        if not self.validate_phone_number(phone_number):
            raise OrderManagementException("Invalid phone number")
        if not self.validate_zip_code(zip_code):
            raise OrderManagementException("Invalid zip code")

        my_order_request = OrderRequest(
            product_id, order_type, delivery_address, phone_number, zip_code
        )
        order_id = my_order_request.order_id

        # change \\ to / for linux and mac
        home_path = str(Path.home()).replace("\\", "/")

        json_store_path = (
            home_path + "/PycharmProjects/G80.2023.T3.EG03/src/Json/Store/"
        )
        file_store = json_store_path + "store_request.json"

        try:
            with open(file_store, "r", encoding="UTF-8", newline="") as file:
                data_list = json.load(file)

        except FileNotFoundError:
            data_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException(
                "Json Decode Error - Wrong Json format"
            ) from ex

        data_list.append(my_order_request._dict_)  # pylint: disable=protected-access

        try:
            with open(file_store, "w", encoding="UTF-8", newline="") as file:
                json.dump(data_list, file, indent=2)

        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex

        return order_id

    @staticmethod
    def validate_ean13(ean13_code):
        """RETURNs TRUE IF THE CODE RECEIVED IS A VALID EAN13,
        OR FALSE IN OTHER CASE"""

        # EAN13 válido. (13 dígitos)
        if len(ean13_code) != 13:
            return False
        if not ean13_code.isdigit():
            return False

        # sum of odd digits
        sum_odd = 0
        for i in range(0, 12, 2):
            sum_odd += int(ean13_code[i])

        # sum of even digits
        sum_even = 0
        for i in range(1, 12, 2):
            sum_even += int(ean13_code[i])

        # checksum
        checksum = (10 - ((sum_odd + 3 * sum_even) % 10)) % 10

        if checksum != int(ean13_code[12]):
            return False

        return True

    @staticmethod
    def validate_address(delivery_address):
        """RETURNs TRUE IF THE ADDRESS RECEIVED IS VALID,
        OR FALSE IN OTHER CASE"""

        # Dirección a la que se envía el producto.
        # (entre 20 y 100caracteres con al menos 2 cadenas separadas por un espacio blanco)
        if len(delivery_address) < 20 or len(delivery_address) > 100:
            return False
        if delivery_address.count(" ") < 1:
            return False
        # CHECK IF THERE IS ANY TEXT
        if not re.search("[a-zA-Z]", delivery_address):
            return False

        return True

    @staticmethod
    def validate_phone_number(phone_number):
        """RETURNs TRUE IF THE PHONE NUMBER RECEIVED IS VALID,
        OR FALSE IN OTHER CASE"""

        # Número de teléfono válido. (9 dígitos) + 3 dígitos de código de país
        if len(phone_number) != 12:
            return False
        if not phone_number.startswith("+"):
            return False
        if not phone_number[1:].isdigit():
            return False

        return True

    @staticmethod
    def validate_zip_code(zip_code):
        """RETURNs TRUE IF THE ZIP CODE RECEIVED IS VALID,
        OR FALSE IN OTHER CASE"""

        # Código postal válido en España. (5 dígitos)
        if len(zip_code) != 5:
            return False
        if not zip_code.isdigit():
            return False
        return True

    def send_product(self, input_file):
        """Send the order to the warehouse"""
        # change \\ to / for linux and mac

        try:
            with open(input_file, "r", encoding="UTF-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as exc:
            raise OrderManagementException("Wrong file or file path") from exc
        except json.JSONDecodeError as exc:
            raise OrderManagementException(
                "Json Decode Error - Wrong Json format"
            ) from exc
        except Exception as exc:
            raise OrderManagementException(f"Error: {exc}") from exc
        if not self.check_order(data):
            raise OrderManagementException("Invalid order")

        store_request_path = Path.home().joinpath(
            "PycharmProjects/G80.2023.T3.EG03/src/Json/Store/store_request.json"
        )
        with open(str(store_request_path), "r", encoding="UTF-8", newline="") as file:
            store_request = json.load(file)
            #  is a list of dicts with the store requests

        for request in store_request:
            if request["_OrderRequest__order_id"] == data["OrderID"]:
                store_request = request
                break
        # now store_request is a dict with the store request

        ord_shipping = OrderShipping(
            store_request["_OrderRequest__product_id"],
            data["OrderID"],
            data["ContactEmail"],
            store_request["_OrderRequest__order_type"],
        )

        shipping_path = Path.home().joinpath(
            "PycharmProjects/G80.2023.T3.EG03/src/Json/Shipping/order_shippings.json"
        )

        try:
            with open(shipping_path, "r", encoding="UTF-8", newline="") as file:
                data_list = json.load(file)

        except FileNotFoundError:
            data_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException(
                "Json Decode Error - Wrong Json format"
            ) from ex

        data_list.append(ord_shipping._dict_)  # pylint: disable=protected-access
        with open(str(shipping_path), "w", encoding="UTF-8", newline="") as file:
            json.dump(data_list, file, indent=2)  # pylint: disable=protected-access

        return ord_shipping.tracking_code

    @staticmethod
    def check_order(data): # pylint: disable=too-many-return-statements
        """
        El archivo de entrada JSON debe cumplir con el siguiente formato:
        {
            "OrderID":"<String having 32 hexadecimal characters>",
            "ContactEmail": “<valid email>”
        }"""
        if not isinstance(data, dict):
            return False
        for key in ["OrderID", "ContactEmail"]:
            if key not in data:
                return False
        for key in data:
            if key not in ["OrderID", "ContactEmail"]:
                return False

        if not isinstance(data["OrderID"], str):
            return False

        # OrderID debe estar contenido en store_request.json
        store_request_path = Path.home().joinpath(
            "PycharmProjects/G80.2023.T3.EG03/src/Json/Store/store_request.json"
        )
        with open(str(store_request_path), "r", encoding="UTF-8", newline="") as file:
            store_request = json.load(file)
        if data["OrderID"] not in [
            order["_OrderRequest__order_id"] for order in store_request
        ]:
            return False

        if not isinstance(data["ContactEmail"], str):
            return False
        if len(data["OrderID"]) != 32:
            return False
        # un email válido debe cumplir con la siguiente expresión regular
        # [a-z0-9]+@[a-z0-9]+\.[a-z]{1,3}
        if not re.search(r"^[a-z0-9]+@[a-z]+\.[a-z]{1,3}$", data["ContactEmail"]):
            return False
        return True

    def deliver_product(self, tracking_number):
        """Deliver the product to the customer"""

        shippings_path = Path.home().joinpath(
            "PycharmProjects/G80.2023.T3.EG03/src/Json/Shipping/order_shippings.json"
        )
        try:
            with open(shippings_path, "r", encoding="UTF-8", newline="") as file:
                data_list = json.load(file)

        except FileNotFoundError:
            data_list = []

        # en data_list tengo una lista de diccionarios con todos los envios

        if not isinstance(data_list, list):
            raise OrderManagementException("Json Decode Error - Wrong Json format")

        if not self.validate_tracking_number(tracking_number):
            raise OrderManagementException("The tracking code is not valid")

        if tracking_number not in [
            shipping["_OrderShipping__tracking_code"] for shipping in data_list
        ]:
            raise OrderManagementException("The tracking code is not registered")
        # localizar el pedido en el json
        shipping = None
        for shipping in data_list:
            if shipping["_OrderShipping__tracking_code"] == tracking_number:
                # shipping = shipping
                break
        # sacar la fecha de entrega estimada
        estimated_date = shipping["_OrderShipping__delivery_day"]
        # sacar la fecha actual
        actual_date = datetime.datetime.now().timestamp()

        if estimated_date != actual_date:
            raise OrderManagementException("The delivery date is not valid")
        # guardar archivo que registra la entrega en un archivo con la marca de
        # tiempo (hora UTC) de la entrega y el código de seguimiento.
        deliveries_path = Path.home().joinpath(
            "PycharmProjects/G80.2023.T3.EG03/src/Json/deliveries/deliveries.json"
        )
        try:
            with open(deliveries_path, "r", encoding="UTF-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            data_list = []

        if not isinstance(data_list, list):
            raise OrderManagementException("Json Decode Error - Wrong Json format")

        delivery = {"tracking_code": tracking_number, "delivery_date": actual_date}
        data_list.append(delivery)

        with open(str(deliveries_path), "w", encoding="UTF-8", newline="") as file:
            json.dump(data_list, file, indent=2)

        return True

    @staticmethod
    def validate_tracking_number(tracking_number):
        """Validates if the tracking number recived is a correct sha256 code"""
        if not isinstance(tracking_number, str):
            return False
        if len(tracking_number) != 64:
            return False
        if not tracking_number.isalnum():
            return False
        return True
