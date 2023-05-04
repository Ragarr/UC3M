"""test for function 3"""
import json
import unittest
from pathlib import Path
import copy

from freezegun import freeze_time
from uc3m_logistics.order_management_exception import OrderManagementException

from uc3m_logistics.order_manager import OrderManager


class MyTestCase(unittest.TestCase):
    """test for function 3"""

    @freeze_time("2023-03-17")
    def test_path1_2_5(self):
        """Debe fallar decodificando el json de shippings"""
        my_order = OrderManager()

        file_path = Path.home().joinpath(
            "PycharmProjects/G80.2023.T3.EG03/src/Json/Shipping/order_shippings.json"
        )

        # get file content
        with open(file_path, "r", encoding="UTF-8", newline="") as file:
            file_content = json.load(file)

        file_content = copy.deepcopy(file_content)

        # write wrong json
        with open(file_path, "w", encoding="UTF-8", newline="") as file:
            json.dump("wrong json", file)

        # test function
        with self.assertRaises(OrderManagementException) as context_manager:
            my_order.deliver_product(
                "e3966dc2cc732ab30f763a75bfb6b63ec1c48cc330cc3449d402e80507b3adeb"
            )

        # write original json
        with open(file_path, "w", encoding="UTF-8", newline="") as file:
            json.dump(file_content, file)

        self.assertEqual(
            context_manager.exception.message, "Json Decode Error - Wrong Json format"
        )

    def test_path1_2_4_6_7(self):
        """debe fallar por que el tracking code no es valido"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            my_order.deliver_product("1234")
        self.assertEqual(
            context_manager.exception.message, "The tracking code is not valid"
        )

    def test_path1_2_3_6_8_9(self):
        """debe fallar porque el pedido no existe en el json de shippings"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            my_order.deliver_product(
                "e3966dc2cc732ab30f763a75bfb6b63ec1c48cc330cc3449d402e80507b3adec"
            )
        self.assertEqual(
            context_manager.exception.message, "The tracking code is not registered"
        )

    @freeze_time("2029-01-01")
    def test_path1_2_3_6_8_10_11_10_11_12_13_14_15_16(self):
        """debe fallar por que la fecha de entrega no es igual a la fecha actual"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            my_order.deliver_product(
                "e3966dc2cc732ab30f763a75bfb6b63ec1c48cc330cc3449d402e80507b3adeb"
            )
        self.assertEqual(
            context_manager.exception.message, "The delivery date is not valid"
        )

    @freeze_time("2023-03-17")
    def test_path1_2_3_6_8_10_11_12_13_14_15_16_17_18_23(self):
        """debe fallar por que el segundo json no se ha podido decodificar"""
        my_order = OrderManager()
        file_path = Path.home().joinpath(
            "PycharmProjects/G80.2023.T3.EG03/src/Json/deliveries/deliveries.json"
        )
        with open(file_path, "r", encoding="UTF-8", newline="") as file:
            file_content = json.load(file)

        file_content = copy.deepcopy(file_content)

        with open(file_path, "w", encoding="UTF-8", newline="") as file:
            json.dump("wrong json", file)

        with self.assertRaises(OrderManagementException) as context_manager:
            my_order.deliver_product(
                "e3966dc2cc732ab30f763a75bfb6b63ec1c48cc330cc3449d402e80507b3adeb"
            )

        # write original json
        with open(file_path, "w", encoding="UTF-8", newline="") as file:
            json.dump(file_content, file)

        self.assertEqual(
            context_manager.exception.message, "Json Decode Error - Wrong Json format"
        )

    @freeze_time("2023-03-17")
    def test_path1_2_3_6_8_10_11_12_13_14_15_16_17_18_20_22(self):
        """debe funcionar con datalist (deliveries json) vacia"""

        my_order = OrderManager()
        my_order.deliver_product(
            "e3966dc2cc732ab30f763a75bfb6b63ec1c48cc330cc3449d402e80507b3adeb"
        )
        deliveries_path = Path.home().joinpath(
            "PycharmProjects/G80.2023.T3.EG03/src/Json/deliveries/deliveries.json"
        )
        with open(deliveries_path, "r", encoding="UTF-8", newline="") as file:
            data = json.load(file)

        # escribir una lista vacia en el json
        with open(deliveries_path, "w", encoding="UTF-8", newline="") as file:
            json.dump([], file)

        output = my_order.deliver_product(
            "e3966dc2cc732ab30f763a75bfb6b63ec1c48cc330cc3449d402e80507b3adeb"
        )

        # ver que se ha escrito bien en el json
        with open(deliveries_path, "r", encoding="UTF-8", newline="") as file:
            output_json = json.load(file)

        # si output_json tiene exactamente 1 elemento (un diccionario), es que se ha escrito bien
        self.assertEqual(len(output_json), 1)

        # escribir la lista original en el json
        with open(deliveries_path, "w", encoding="UTF-8", newline="") as file:
            json.dump(data, file)

        self.assertTrue(output)

    @freeze_time("2023-03-17")
    def test_path1_2_3_6_8_10_11_12_13_14_15_16_17_18_19_22(self):
        """debe funcionar con datalist (deliveries json) con algun elemento (caso normal)"""
        my_order = OrderManager()

        deliveries_path = Path.home().joinpath(
            "PycharmProjects/G80.2023.T3.EG03/src/Json/deliveries/deliveries.json"
        )
        with open(deliveries_path, "r", encoding="UTF-8", newline="") as file:
            data = json.load(file)

        # meter almenos un elemento en el deliveries json
        if len(data) == 0:
            data.append(
                {
                    "tracking_code": "e3966dc2cc732ab30f763a75bfb6b63ec"
                                     "1c48cc330cc3449d402e80507b3adeb",
                    "delivery_date": "2023-03-17",
                }
            )
            with open(deliveries_path, "w", encoding="UTF-8", newline="") as file:
                json.dump(data, file)

        output = my_order.deliver_product(
            "e3966dc2cc732ab30f763a75bfb6b63ec1c48cc330cc3449d402e80507b3adeb"
        )

        self.assertTrue(output)


if __name__ == "__main__":
    unittest.main()
