"""test for function 1"""
import json
import unittest
from pathlib import Path

from freezegun import freeze_time
from uc3m_logistics.order_management_exception import OrderManagementException

from uc3m_logistics.order_manager import OrderManager


class MyTestCase(unittest.TestCase):
    """Test for function 1"""
    @freeze_time("2023-03-16")
    def test_register_order_valid_1(self):
        """test valid 1"""
        my_order = OrderManager()
        my_value = my_order.register_order(product_id="3662168005326",
                                           delivery_address="C/SAN JUAN DE LA CRUZ,17,MADRID, SPAIN"
                                           ,
                                           order_type="Regular",
                                           phone_number="+34123456789",
                                           zip_code="28005")

        self.assertEqual("b8ddf917bbc85eb9fd75b55a971a8083", my_value)

        json_store_path = str(Path.home()).replace("\\", "/") + \
                          "/PycharmProjects/G80.2023.T3.EG03/src/Json/Store/"
        file_store = json_store_path + "store_request.json"
        with (open(file_store, "r", encoding="UTF-8", newline="")) as file:
            data_list = json.load(file)
        found = False
        for item in data_list:
            if item["_OrderRequest__order_id"] == my_value:
                found = True
        self.assertTrue(found)

    @freeze_time("2023-03-16")
    def test_register_order_invalid_2(self):
        """test invalid 2"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            # pylint: disable=unused-variable
            my_value = my_order.register_order(product_id="8421691423228",
                                               delivery_address=
                                               "C/SAN JUAN DE LA CRUZ,17,MADRID, SPAIN",
                                               order_type="Regular",
                                               phone_number="+34123456789",
                                               zip_code="28005")
        self.assertEqual(context_manager.exception.message, "Invalid EAN13 code")

    @freeze_time("2023-03-16")
    def test_register_order_invalid_3(self):
        """test invalid 3"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            # pylint: disable=unused-variable
            my_value = my_order.register_order(product_id="842169142322",
                                               delivery_address=
                                               "C/SAN JUAN DE LA CRUZ,17,MADRID, SPAIN",
                                               order_type="Regular",
                                               phone_number="+34123456789",
                                               zip_code="28005")
        self.assertEqual(context_manager.exception.message, "Invalid EAN13 code")

    @freeze_time("2023-03-16")
    def test_register_order_invalid_4(self):
        """test invalid 4"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            # pylint: disable=unused-variable
            my_value = my_order.register_order(product_id="84216914232201",
                                               delivery_address=
                                               "C/SAN JUAN DE LA CRUZ,17,MADRID, SPAIN",
                                               order_type="Regular",
                                               phone_number="+34123456789",
                                               zip_code="28005")
        self.assertEqual(context_manager.exception.message, "Invalid EAN13 code")

    @freeze_time("2023-03-16")
    def test_register_order_valid_5(self):
        """test valid 5"""
        my_order = OrderManager()

        my_value = my_order.register_order(product_id="8421691423220",
                                               delivery_address=
                                               "C/SAN JUAN DE LA CRUZ,17,MADRID, SPAIN",
                                               order_type="Premium",
                                               phone_number="+34123456789",
                                               zip_code="28005")
        self.assertEqual("99929ce9c86213e64b577acb17af6ab0",my_value)

        json_store_path = str(Path.home()).replace("\\", "/") + \
                          "/PycharmProjects/G80.2023.T3.EG03/src/Json/Store/"
        file_store = json_store_path + "store_request.json"
        with (open(file_store, "r", encoding="UTF-8", newline="")) as file:
            data_list = json.load(file)
        found = False
        for item in data_list:
            if item["_OrderRequest__order_id"] == my_value:
                found = True
        self.assertTrue(found)

    def test_register_order_invalid_6(self):
        """test invalid 6"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            # pylint: disable=unused-variable
            my_value = my_order.register_order(product_id="8421691423220",
                                               delivery_address=
                                               "C/SAN JUAN DE LA CRUZ,17,MADRID, SPAIN",
                                               order_type="ERROR",
                                               phone_number="+34123456789",
                                               zip_code="28005")
        self.assertEqual(context_manager.exception.message, "Invalid order type")
    def test_register_order_invalid_7(self):
        """test invalid 7"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            # pylint: disable=unused-variable
            my_value = my_order.register_order(product_id="8421691423220",
                                               delivery_address="C/SAN JUAN DE LA CR",
                                               order_type="Premium",
                                               phone_number="+34123456789",
                                               zip_code="28005")
        self.assertEqual(context_manager.exception.message, "Invalid delivery address")

    def test_register_order_invalid_8(self):
        """test invalid 8"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            # pylint: disable=unused-variable
            my_value = my_order.register_order(product_id="8421691423220",
                                               delivery_address=
                                               "C/SAN JUAN DE LA CRUZzzzzzzzzzzzzzzz"
                                               "zzzzzzzzzzzzzzzzzzzzzZZZZZZZZZZZZZZZZZZ"
                                               "ZZZZZZZZCRUZzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
                                               "zzzZZZZZZZZZZZZZZZZZZZZZZZZZZCRUZzzzzzzzzzzzzzzz"
                                               "zzzzzzzzzzzzzzzzzzzzzZZZZZZZZZZZZZZZZZZZZZZZZZZCR"
                                               "UZzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzZZZZZZZZZZ"
                                               "ZZZZZZZZZZZZZZZZ,17,MADRID, SPAIN",
                                               order_type="Premium",
                                               phone_number="+34123456789",
                                               zip_code="28005")
        self.assertEqual(context_manager.exception.message, "Invalid delivery address")

    @freeze_time("2023-03-16")
    def test_register_order_invalid_9(self):
        """test invalid 9"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            # pylint: disable=unused-variable
            my_value = my_order.register_order(product_id="8421691423220",
                                               delivery_address=
                                               "C/SANJUANDELACRUZ,17,MADRID,SPAIN",
                                               order_type="Premium",
                                               phone_number="+34123456789",
                                               zip_code="28005")
        self.assertEqual(context_manager.exception.message, "Invalid delivery address")

    @freeze_time("2023-03-16")
    def test_register_order_valid_10(self):
        """test valid 10"""
        my_order = OrderManager()
        # pylint: disable=unused-variable
        my_value = my_order.register_order(product_id="8421691423220",
                                               delivery_address=
                                               "C/SANJUANDELACRUZ,17, MADRID,SPAIN",
                                               order_type="Premium",
                                               phone_number="+34123456789",
                                               zip_code="28005")
        self.assertEqual("dc03478368816c642e3ca99c8a4f76cb", my_value)

        json_store_path = str(Path.home()).replace("\\", "/") + \
                          "/PycharmProjects/G80.2023.T3.EG03/src/Json/Store/"
        file_store = json_store_path + "store_request.json"
        with (open(file_store, "r", encoding="UTF-8", newline="")) as file:
            data_list = json.load(file)
        found = False
        for item in data_list:
            if item["_OrderRequest__order_id"] == my_value:
                found = True
        self.assertTrue(found)

    def test_register_order_invalid_11(self):
        """test invalid 11"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            # pylint: disable=unused-variable
            my_value = my_order.register_order(product_id="8421691423220",
                                               delivery_address="                           ",
                                               order_type="Premium",
                                               phone_number="+34123456789",
                                               zip_code="28005")
        self.assertEqual(context_manager.exception.message, "Invalid delivery address")

    def test_register_order_invalid_12(self):
        """test invalid 12"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            # pylint: disable=unused-variable
            my_value = my_order.register_order(product_id="8421691423220",
                                               delivery_address=
                                               "C/SAN JUAN DE LA CRUZ,17,MADRID, SPAIN",
                                               order_type="Premium",
                                               phone_number="+3412345678",
                                               zip_code="28005")
        self.assertEqual(context_manager.exception.message, "Invalid phone number")

    def test_register_order_invalid_13(self):
        """test invalid 13"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            # pylint: disable=unused-variable
            my_value = my_order.register_order(product_id="8421691423220",
                                               delivery_address=
                                               "C/SAN JUAN DE LA CRUZ,17,MADRID, SPAIN",
                                               order_type="Premium",
                                               phone_number="+341234567890",
                                               zip_code="28005")
        self.assertEqual(context_manager.exception.message, "Invalid phone number")

    def test_register_order_invalid_14(self):
        """test invalid 14"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            # pylint: disable=unused-variable
            my_value = my_order.register_order(product_id="8421691423220",
                                               delivery_address=
                                               "C/SAN JUAN DE LA CRUZ,17,MADRID, SPAIN",
                                               order_type="Premium",
                                               phone_number="+3A123456789",
                                               zip_code="28005")
        self.assertEqual(context_manager.exception.message, "Invalid phone number")

    def test_register_order_invalid_15(self):
        """test invalid 15"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            # pylint: disable=unused-variable
            my_value = my_order.register_order(product_id="8421691423220",
                                               delivery_address=
                                               "C/SANJUANDELACRUZ,17, MADRID,SPAIN",
                                               order_type="Premium",
                                               phone_number="+34123456789",
                                               zip_code="2800")
        self.assertEqual(context_manager.exception.message, "Invalid zip code")

    def test_register_order_invalid_16(self):
        """test invalid 16"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            # pylint: disable=unused-variable
            my_value = my_order.register_order(product_id="8421691423220",
                                               delivery_address=
                                               "C/SANJUANDELACRUZ,17, MADRID,SPAIN",
                                               order_type="Premium",
                                               phone_number="+34123456789",
                                               zip_code="280050")
        self.assertEqual(context_manager.exception.message, "Invalid zip code")

    def test_register_order_invalid_17(self):
        """test invalid 17"""
        my_order = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            # pylint: disable=unused-variable
            my_value = my_order.register_order(product_id="8421691423220",
                                               delivery_address=
                                               "C/SANJUANDELACRUZ,17, MADRID,SPAIN",
                                               order_type="Premium",
                                               phone_number="+34123456789",
                                               zip_code="280A5")
        self.assertEqual(context_manager.exception.message, "Invalid zip code")

if __name__ == '__main__':
    unittest.main()
