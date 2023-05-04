"""Contains the class OrderShipping"""
import json
from datetime import datetime
import hashlib
from freezegun import freeze_time

from uc3m_logistics.data.data_attribute.attribute_order_id import OrderId
from uc3m_logistics.data.data_attribute.attribute_email import Email
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from uc3m_logistics.config.order_manager_config import JSON_FILES_PATH, ERRORFOUND, ERRORFORMAT, ERRORNOTFOUNDID, ERRORDATAORDERSMANIPULATED
from uc3m_logistics.data.data_attribute.attribute_porduct_id import ProductId
from uc3m_logistics.data.data_attribute.attribute_order_type import OrderType
from uc3m_logistics.data.order_request import OrderRequest


# pylint: disable=too-many-instance-attributes
class OrderShipping:
    """Class representing the shipping of an order"""
    _order_store = "orders_store.json"
    _order_ID = "OrderID"
    _oR_ID = "_OrderRequest__order_id"
    _oR_PID = "_OrderRequest__product_id"
    _oR_address = "_OrderRequest__delivery_address"
    _oR_type = "_OrderRequest__order_type"
    _oR_phone_number = "_OrderRequest__phone_number"
    _oR_time_stamp = "_OrderRequest__time_stamp"
    _oR_zip_code = "_OrderRequest__zip_code"

    def __init__(self, input_file):
        # leer file
        self.__json_content = self._read_json_file(input_file)
        # validate los labels
        order_id = OrderId.validate_key_label(self.__json_content, "OrderID")
        email = Email.validate_key_label(self.__json_content, "ContactEmail")
        # validate el order id y el email
        self.__order_id = OrderId(order_id).value
        self.__delivery_email = Email(email).value
        self.__alg = "SHA-256"
        self.__type = "DS"

        product_id, order_type = self._check_order_id(self.__json_content)
        self.__product_id = ProductId(product_id).value
        order_type = OrderType(order_type).value

        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        if order_type == "Regular":
            delivery_days = 7
        else:
            delivery_days = 1
        # timestamp is represented in seconds.microseconds
        # __delivery_day must be expressed in seconds to be added to the timestamp
        self.__delivery_day = self.__issued_at + (delivery_days * 24 * 60 * 60)
        self.__tracking_code = hashlib.sha256(self.__signature_string().encode()).hexdigest()

    def __signature_string(self):
        """Composes the string to be used for generating the tracking_code"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",order_id:" + \
            self.__order_id + ",issuedate:" + str(self.__issued_at) + \
            ",deliveryday:" + str(self.__delivery_day) + "}"

    @property
    def product_id(self):
        """Property that represents the product_id of the order"""
        return self.__product_id

    @product_id.setter
    def product_id(self, value):
        self.__product_id = value

    @property
    def order_id(self):
        """Property that represents the order_id"""
        return self.__order_id

    @order_id.setter
    def order_id(self, value):
        self.__order_id = value

    @property
    def email(self):
        """Property that represents the email of the client"""
        return self.__delivery_email

    @email.setter
    def email(self, value):
        self.__delivery_email = value

    @property
    def tracking_code(self):
        """returns the tracking code"""
        return self.__tracking_code

    @property
    def issued_at(self):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at(self, value):
        self.__issued_at = value

    @property
    def delivery_day(self):
        """Returns the delivery day for the order"""
        return self.__delivery_day

    @classmethod
    def _read_json_file(cls, input_file):
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            # file is not found
            raise OrderManagementException(ERRORFOUND) from ex
        except json.JSONDecodeError as ex:
            raise OrderManagementException(ERRORFORMAT) from ex
        return data

    @classmethod
    def _check_order_id(cls, data):
        file_store = JSON_FILES_PATH + cls._order_store
        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = False
        for item in data_list:
            if item[cls._oR_ID] == data[cls._order_ID]:
                found = True
                # retrieve the orders data
                proid = item[cls._oR_PID]
                address = item[cls._oR_address]
                reg_type = item[cls._oR_type]
                phone = item[cls._oR_phone_number]
                order_timestamp = item[cls._oR_time_stamp]
                zip_code = item[cls._oR_zip_code]
                # set the time when the order was registered for checking the md5
                with freeze_time(datetime.fromtimestamp(order_timestamp).date()):
                    order = OrderRequest(product_id=proid,
                                         delivery_address=address,
                                         order_type=reg_type,
                                         phone_number=phone,
                                         zip_code=zip_code)

                if order.order_id != data[cls._order_ID]:
                    raise OrderManagementException(ERRORDATAORDERSMANIPULATED)
        if not found:
            raise OrderManagementException(ERRORNOTFOUNDID)
        return proid, reg_type
