"""Module for testing request_vaccination_id"""
import os
import unittest
import json
import hashlib

from freezegun import freeze_time
from uc3m_logistics import OrderManager
from uc3m_logistics import OrderManagementException
from uc3m_logistics import JSON_FILES_PATH


param_list_ok=[("8421691423220", "calle con20chars1esp","Regular",
                "+34123456789", "01000", "4f5ff74ce8c5aa97f9675dbd44035d9d", "test_1"),
               ("8470007568339", "calle con21chars 2esp", "Premium",
                "+34333456789","01001","7b5598dd46cdab4dc3f9588641816d7a","test_2"),
               ("8470006607824",
                "calle conlalongitudnecesariaparaconseguirlos99char poniendole "
                "muchos caracteres este caso de prueba",
                "Regular", "+34333456789", "52998", "13cd904cbe5ffd57061e0e8cea2912e8","test_3"),
               ("8436552698662",
                "calle conlalongitudnecesariaparaconseguirlos100char poniendole "
                "muchos caracteres este caso de prueba",
                "Regular", "+44333456789", "52999", "ccdd94369dec3654941c2917154a5894","test_4")
               ]

param_list_nok=[("842169142322X",
                 "calle con20chars1esp","Regular",
                "+34123456789",
                 "01000", "Invalid EAN13 code string", "test_5 , Invalid EAN13 code string"),
                ("8421691423223",
                 "calle con20chars1esp", "Regular",
                 "+34123456789",
                 "01000", "Invalid EAN13 control digit", "test_6 , Invalid EAN13 control digit"),
                ("842169142322",
                 "calle con20chars1esp", "Regular",
                 "+34123456789",
                 "01000", "Invalid EAN13 code string",
                 "test_7 , Invalid EAN13 string - lt 13 chars"),
                ("84216914232200",
                 "calle con20chars1esp", "Regular",
                 "+34123456789",
                 "01000", "Invalid EAN13 code string",
                 "test_8 , Invalid EAN13 string - gt 13 chars"),
                ("8421691423220",
                 "calle con20chars1esp", "IRREGULAR",
                 "+34123456789",
                 "01000", "order_type is not valid", "test_9 , order_type is nor valid"),
                ("8421691423220",
                 "calle con20@chars1esp", "Regular",
                 "+34123456789",
                 "01000", "address is not valid",
                 "test_10 , address is not valid - invalid character @"),
                ("8421691423220",
                 "calle conlalongitudnecesariaparaconseguirlos100char "
                 "poniendole muchos caracteres este caso de pruebaa",
                 "Regular", "+34123456789",
                 "01000", "address is not valid", "test_11 , address with 101 characteres"),
                ("8421691423220",
                 "calleconlalongitudnecesariaparaconseguirlos100charponien"
                 "dolemuchoscaracteresestecasodepruebaa",
                 "Regular",
                 "+34123456789",
                 "01000", "address is not valid", "test_12 , address with no spaces"),
                ("8421691423220",
                 "calle con19char1esp",
                 "Regular",
                 "+34123456789",
                 "01000", "address is not valid", "test_13 , address with 19 characters"),
                ("8421691423220",
                 "calle con20chars1esp",
                 "Regular",
                 "+3412345678X",
                 "01000", "phone number is not valid",
                 "test_14 , phone number is not valid - not numeric character"),
                ("8421691423220",
                 "calle con20chars1esp",
                 "Regular",
                 "+341234567890",
                 "01000", "phone number is not valid", "test_15 , phone number 13 chars"),
                ("8421691423220",
                 "calle con20chars1esp",
                 "Regular",
                 "+3412345678",
                 "01000", "phone number is not valid", "test_16 , phone number 11 chars"),
                ("8421691423220",
                 "calle con20chars1esp",
                 "Regular",
                 "+34123456789",
                 "0100Z", "value format is not valid", "test_17 , value not numeric "),
                ("8421691423220",
                 "calle con20chars1esp",
                 "Regular",
                 "+34123456789",
                 "010000", "value format is not valid", "test_18 , value 6 chars "),
                ("8421691423220",
                 "calle con20chars1esp",
                 "Regular",
                 "+34123456789",
                 "0100", "value format is not valid", "test_19 , value 4 chars "),
                ("8421691423220",
                 "calle con20chars1esp",
                 "Regular",
                 "+34123456789",
                 "00999", "value is not valid", "test_20 , value bellow 01 "),
                ("8421691423220",
                 "calle con20chars1esp",
                 "Regular",
                 "+34123456789",
                 "53000", "value is not valid", "test_21, value above 52 "),
                ]


class TestRegisterOrder(unittest.TestCase):
    """Class for testing register_order"""
    #pylint: disable=too-many-locals
    @freeze_time("2023-03-08")
    def test_parametrized_valid_request_vaccination(self):
        "Parametrized tests: valid cases"
        file_store = JSON_FILES_PATH + "orders_store.json"
        if os.path.isfile(file_store):
            os.remove(file_store)
        my_request = OrderManager()

        for product_id,address,order_type,phone_number,\
            zip_code,expected_result,comment in param_list_ok:
            with self.subTest(test=comment):
                value = my_request.register_order(product_id=product_id,
                                                  address=address,
                                                  order_type=order_type,
                                                  phone_number=phone_number,
                                                  zip_code=zip_code)
                self.assertEqual(value , expected_result)

                with open(file_store, "r", encoding="utf-8", newline="") as file:
                    data_list = json.load(file)
                found = False
                for item in data_list:
                    if item["_OrderRequest__order_id"] == value:
                        found = True
                self.assertTrue(found)

    def test_parametrized_not_valid_request_vaccination( self ):
        """Method for testing order_request: invalid cases"""
        file_store = JSON_FILES_PATH + "orders_store.json"
        my_request = OrderManager()

        for product_id, address, order_type, phone_number, zip_code, \
            expected_result, comment in param_list_nok:
            with self.subTest(test = comment):
                if os.path.isfile(file_store):
                    with open(file_store, "r", encoding="utf-8", newline="") as file:
                        hash_original = hashlib.md5(str(file).encode()).hexdigest()
                else:
                    hash_original = ""
                with self.assertRaises(OrderManagementException) as context_manager:
                    my_request.register_order(product_id=product_id,
                                              order_type=order_type,
                                              address=address,
                                              phone_number=phone_number,
                                              zip_code=zip_code)
                self.assertEqual(context_manager.exception.message, expected_result)
                if os.path.isfile(file_store):
                    with open(file_store, "r", encoding="utf-8", newline="") as file:
                        hash_new = hashlib.md5(str(file).encode()).hexdigest()
                else:
                    hash_new = ""
                self.assertEqual(hash_original,hash_new)

    @freeze_time("2023-03-08")
    def test__duplicate_valid_order_id(self):
        """ Test 20 , order id is registered in store (only with freezetime)"""
        file_store = JSON_FILES_PATH + "orders_store.json"
        if os.path.isfile(file_store):
            os.remove(file_store)
        my_request = OrderManager()

        value = my_request.register_order(product_id="8421691423220",
                                          order_type="Regular",
                                          address="calle con20chars1esp",
                                          phone_number="+34123456789",
                                          zip_code="28911")

        with self.assertRaises(OrderManagementException) as context_manager:
            my_request.register_order(product_id="8421691423220",
                                              order_type="Regular",
                                              address="calle con20chars1esp",
                                              phone_number="+34123456789",
                                              zip_code="28911")
        self.assertEqual(context_manager.exception.message,
                         "order_id is already registered in orders_store")

        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = 0
        for item in data_list:
            if item["_OrderRequest__order_id"] \
                    == value :
                found = found + 1
        self.assertEqual(found,1)


if __name__ == '__main__':
    unittest.main()
