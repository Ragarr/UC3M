"""Tests for get_vaccine_date method"""
from unittest import TestCase
import os
import json
import hashlib
import shutil
from freezegun import freeze_time
from uc3m_logistics import OrderManager
from uc3m_logistics import OrderManagementException
from uc3m_logistics import JSON_FILES_PATH
from uc3m_logistics import JSON_FILES_RF2_PATH


param_list_nok =[("node10_deleted.json","JSON Decode Error - Wrong JSON Format"),
                 ("node10_duplicated.json","JSON Decode Error - Wrong JSON Format"),
                 ("node11_deleted.json","JSON Decode Error - Wrong JSON Format"),
                 ("node11_duplicated.json","JSON Decode Error - Wrong JSON Format"),
                 ("node12_deleted.json","JSON Decode Error - Wrong JSON Format"),
                 ("node12_duplicated.json","JSON Decode Error - Wrong JSON Format"),
                 ("node13_modified.json","JSON Decode Error - Wrong JSON Format"),
                 ("node14_deleted.json","JSON Decode Error - Wrong JSON Format"),
                 ("node14_duplicated.json","JSON Decode Error - Wrong JSON Format"),
                 ("node16_deleted.json","JSON Decode Error - Wrong JSON Format"),
                 ("node16_duplicated.json","JSON Decode Error - Wrong JSON Format"),
                 ("node17_deleted.json","JSON Decode Error - Wrong JSON Format"),
                 ("node17_duplicated.json","JSON Decode Error - Wrong JSON Format"),
                 ("node18_deleted.json","Bad label"),
                 ("node18_duplicated.json","Bad label"),
                 ("node19_deleted.json","JSON Decode Error - Wrong JSON Format"),
                 ("node19_duplicated.json","JSON Decode Error - Wrong JSON Format"),
                 ("node20_modified.json","JSON Decode Error - Wrong JSON Format"),
                 ("node21_deleted.json","JSON Decode Error - Wrong JSON Format"),
                 ("node21_duplicated.json","JSON Decode Error - Wrong JSON Format"),
                 ("node22_deleted.json","order id is not valid"),
                 ("node22_duplicated.json","order id is not valid"),
                 ("node23_deleted.json","JSON Decode Error - Wrong JSON Format"),
                 ("node23_duplicated.json","JSON Decode Error - Wrong JSON Format"),
                 ("node25_deleted.json","Bad label"),
                 ("node25_duplicated.json","Bad label"),
                 ("node29_deleted.json","contact email is not valid"),
                 ("node29_duplicated.json","contact email is not valid"),
                 ("node2_deleted.json","JSON Decode Error - Wrong JSON Format"),
                 ("node2_duplicated.json","JSON Decode Error - Wrong JSON Format"),
                 ("node31_modified.json","JSON Decode Error - Wrong JSON Format"),
                 ("node32_modified.json","Bad label"),
                 ("node33_modified.json","JSON Decode Error - Wrong JSON Format"),
                 ("node34_modified.json","JSON Decode Error - Wrong JSON Format"),
                 ("node35_deleted.json","order id is not valid"),
                 ("node35_duplicated.json","order id is not valid"),
                 ("node35_modified.json","order id is not valid"),
                 ("node36_modified.json","JSON Decode Error - Wrong JSON Format"),
                 ("node38_modified.json","Bad label"),
                 ("node3_deleted.json","Bad label"),
                 ("node3_duplicated.json","JSON Decode Error - Wrong JSON Format"),
                 ("node4_deleted.json","JSON Decode Error - Wrong JSON Format"),
                 ("node4_duplicated.json","JSON Decode Error - Wrong JSON Format"),
                 ("node5_modified.json","JSON Decode Error - Wrong JSON Format"),
                 ("node6_deleted.json","JSON Decode Error - Wrong JSON Format"),
                 ("node6_duplicated.json","JSON Decode Error - Wrong JSON Format"),
                 ("node7_deleted.json","JSON Decode Error - Wrong JSON Format"),
                 ("node7_duplicated.json","JSON Decode Error - Wrong JSON Format"),
                 ("node8_deleted.json","JSON Decode Error - Wrong JSON Format"),
                 ("node8_duplicated.json","JSON Decode Error - Wrong JSON Format"),
                 ("node9_modified.json","JSON Decode Error - Wrong JSON Format"),
                 ("node_at_deleted.json","contact email is not valid"),
                 ("node_at_duplicated.json","contact email is not valid"),
                 ("node_dom1_modified.json","contact email is not valid"),
                 ("node_dot_dom1_duplicated.json","contact email is not valid"),
                 ("node_dot_dom1_modified.json","contact email is not valid"),
                 ("node_ext1_deleted.json","contact email is not valid"),
                 ("node_ext1_modified.json","contact email is not valid"),
                 ("node_ext2_duplicated.json","contact email is not valid"),
                 ("node_user_email_modified.json","contact email is not valid")]


class TestSendProduct(TestCase):
    """Class for testing get_vaccine_date"""
    @freeze_time("2023-03-08")
    def test_send_product_regular(self):
        """test ok"""
        file_test = JSON_FILES_RF2_PATH + "valid.json"
        my_manager = OrderManager()

    #first , prepare the test , remove orders_store
        file_orders_store = JSON_FILES_PATH + "orders_store.json"
        file_shipments_store = JSON_FILES_PATH + "shipments_store.json"
        if os.path.isfile(file_orders_store):
            os.remove(file_orders_store)
        if os.path.isfile(file_shipments_store):
            os.remove(file_shipments_store)
    # add an order to the store
        my_manager.register_order(product_id="8421691423220",
                                  address="calle con20chars1esp",
                                  order_type="Regular",
                                  phone_number="+34123456789",
                                  zip_code="01000")
    #check the method
        value = my_manager.send_product(file_test)
        self.assertEqual(value, "847dfd443d86c9c222242010c11a44bd9a09c37b42b6e956db97ba173abefe83")

    #check shipments_store
        with open(file_shipments_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = False
        for item in data_list:
            if item["_OrderShipping__tracking_code"] == \
                    "847dfd443d86c9c222242010c11a44bd9a09c37b42b6e956db97ba173abefe83":
                found = True
        self.assertTrue(found)

    @freeze_time("2023-03-08")
    def test_send_product_premium( self ):
        """test ok"""
        file_test = JSON_FILES_RF2_PATH + "valid_premium.json"
        my_manager = OrderManager()

        # first , prepare the test , remove orders_store
        file_orders_store = JSON_FILES_PATH + "orders_store.json"
        file_shipments_store = JSON_FILES_PATH + "shipments_store.json"
        if os.path.isfile(file_orders_store):
            os.remove(file_orders_store)
        if os.path.isfile(file_shipments_store):
            os.remove(file_shipments_store)
        # add an order to the store
        my_manager.register_order(product_id="8470007568339",
                                  address="calle con21chars 2esp",
                                  order_type="Premium",
                                  phone_number="+34333456789",
                                  zip_code="01001")
        # check the method
        value = my_manager.send_product(file_test)
        self.assertEqual(value, "4677574bebf6737df4d85993dace90d988595649c918dad033151235749887ab")

        # check store_date
        with open(file_shipments_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = False
        for item in data_list:
            if item["_OrderShipping__tracking_code"] == \
                    "4677574bebf6737df4d85993dace90d988595649c918dad033151235749887ab":
                found = True
        self.assertTrue(found)

    @freeze_time("2023-03-08")
    def test_get_vaccine_date_no_ok_parameter(self):
        """tests no ok"""
        file_store_date = JSON_FILES_PATH + "orders_store.json"
        my_manager = OrderManager()
        for file_name,expected_value in param_list_nok:
            with self.subTest(test=file_name):
                file_test = JSON_FILES_RF2_PATH + file_name

                # read the file to compare file content before and after method call
                if os.path.isfile(file_store_date):
                    with open(file_store_date, "r", encoding="utf-8", newline="") as file:
                        hash_original = hashlib.md5(str(file).encode()).hexdigest()
                else:
                    hash_original = ""

                # check the method
                with self.assertRaises(OrderManagementException) as c_m:
                    my_manager.send_product(file_test)
                self.assertEqual(c_m.exception.message, expected_value)

                # read the file again to compare
                if os.path.isfile(file_store_date):
                    with open(file_store_date, "r", encoding="utf-8", newline="") as file:
                        hash_new = hashlib.md5(str(file).encode()).hexdigest()
                else:
                    hash_new = ""

                self.assertEqual(hash_new, hash_original)



    @freeze_time("2023-03-08")
    def test_get_vaccine_date_no_ok_data_manipulated( self ):
        """ no quotes , not valid """
        file_test = JSON_FILES_RF2_PATH + "valid.json"
        my_manager = OrderManager()
        file_store = JSON_FILES_PATH + "orders_store.json"
        file_store_date = JSON_FILES_PATH + "shipments_store.json"

        if os.path.isfile(JSON_FILES_PATH + "swap.json"):
            os.remove(JSON_FILES_PATH + "swap.json")
        if not os.path.isfile(JSON_FILES_PATH + "orders_store_manipulated.json"):
            shutil.copy(JSON_FILES_RF2_PATH + "orders_store_manipulated.json",
                        JSON_FILES_PATH + "orders_store_manipulated.json")

        #rename the manipulated order's store
        if os.path.isfile(file_store):
            os.rename(file_store, JSON_FILES_PATH + "swap.json")
        os.rename(JSON_FILES_PATH + "orders_store_manipulated.json",file_store)

        # read the file to compare file content before and after method call
        if os.path.isfile(file_store_date):
            with open(file_store_date, "r", encoding="utf-8", newline="") as file_org:
                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
        else:
            hash_original = ""

        # check the method
        exception_message = "Exception not raised"
        try:
            my_manager.send_product(file_test)
        #pylint: disable=broad-except
        except Exception as exception_raised:
            exception_message = exception_raised.__str__()

        #restore the original orders' store
        os.rename(file_store, JSON_FILES_PATH + "orders_store_manipulated.json")
        if os.path.isfile(JSON_FILES_PATH + "swap.json"):

            os.rename(JSON_FILES_PATH + "swap.json", file_store)
        # read the file again to campare
        if os.path.isfile(file_store_date):
            with open(file_store_date, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_new = ""

        self.assertEqual(exception_message, "Orders' data have been manipulated")
        self.assertEqual(hash_new, hash_original)
