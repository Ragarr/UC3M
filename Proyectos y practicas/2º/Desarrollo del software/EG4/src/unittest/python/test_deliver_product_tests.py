"""Module for testing deliver_product"""
from unittest import TestCase
import os
import hashlib
import json
from freezegun import freeze_time
from uc3m_logistics import OrderManager
from uc3m_logistics import OrderManagementException
from uc3m_logistics import JSON_FILES_PATH
from uc3m_logistics import JSON_FILES_RF2_PATH


class TestDeliverProduct(TestCase):
    """Class for testing deliver_product"""
    @freeze_time("2023-03-08")
    def setUp(self):
        """first prepare the stores"""
        file_store_patient = JSON_FILES_PATH + "orders_store.json"
        file_shipments_store = JSON_FILES_PATH + "shipments_store.json"


        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)
        if os.path.isfile(file_shipments_store):
            os.remove(file_shipments_store)

        #add orders and shipping info in the stores
        my_manager = OrderManager()
        # add an order in the store
        file_test = JSON_FILES_RF2_PATH + "valid.json"
        my_manager.register_order(product_id="8421691423220",
                                  address="calle con20chars1esp",
                                  order_type="Regular",
                                  phone_number="+34123456789",
                                  zip_code="01000")
        my_manager.send_product(file_test)



    @freeze_time("2023-03-15")
    def test_deliver_product_ok(self):
        """basic path , tracking_code is found , and date = today"""
        my_manager = OrderManager()
        value = my_manager.deliver_product(
            "847dfd443d86c9c222242010c11a44bd9a09c37b42b6e956db97ba173abefe83")
        self.assertTrue(value)

        file_shipments_delivered = JSON_FILES_PATH + "shipments_delivered.json"
        # check store_vaccine
        with open(file_shipments_delivered, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = False
        if "847dfd443d86c9c222242010c11a44bd9a09c37b42b6e956db97ba173abefe83" in data_list:
            found = True
        self.assertTrue(found)

    @freeze_time("2023-04-18")
    def test_deliver_product_no_date(self):
        """path tracking_code is found , and date is not today"""
        file_shipments_delivered = JSON_FILES_PATH + "shipments_delivered.json"
        my_manager = OrderManager()

        # read the file  to compare
        if os.path.isfile(file_shipments_delivered):
            with open(file_shipments_delivered, "r", encoding="utf-8", newline="") as file:
                hash_original = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_original = ""

        with self.assertRaises(OrderManagementException) as context_manager:
            my_manager.deliver_product(
                "847dfd443d86c9c222242010c11a44bd9a09c37b42b6e956db97ba173abefe83")
        self.assertEqual(context_manager.exception.message, "Today is not the delivery date")

        # read the file again to compare
        if os.path.isfile(file_shipments_delivered):
            with open(file_shipments_delivered, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_new = ""

        self.assertEqual(hash_new, hash_original)

    @freeze_time("2023-03-18")
    def test_deliver_product_bad_date_signature(self):
        """path signature is not valid format , only 63 chars"""
        file_store_shipments = JSON_FILES_PATH + "shipments_delivered.json"
        my_manager = OrderManager()
        # read the file  to compare

        if os.path.isfile(file_store_shipments):
            with open(file_store_shipments, "r", encoding="utf-8", newline="") as file:
                hash_original = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_original = ""

        with self.assertRaises(OrderManagementException) as context_manager:
            my_manager.deliver_product(
                "a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(context_manager.exception.message, "tracking_code format is not valid")

        # read the file again to compare
        if os.path.isfile(file_store_shipments):
            with open(file_store_shipments, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_new = ""

        self.assertEqual(hash_new, hash_original)

    @freeze_time("2023-03-18")
    def test_tracking_code_not_found_date_signature(self):
        """path: signature is not found in shipments_store"""
        file_store_vaccine = JSON_FILES_PATH + "store_vaccine.json"
        my_manager = OrderManager()
        # read the file  to compare

        if os.path.isfile(file_store_vaccine):
            with open(file_store_vaccine, "r", encoding="utf-8", newline="") as file:
                hash_original = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_original = ""

        with self.assertRaises(OrderManagementException) as context_manager:
            my_manager.deliver_product(
                "7a8403d8605804cf2534fd7885940f3c3d8ec60ba578bc158b5dc2b9fb68d524")
        self.assertEqual(context_manager.exception.message, "tracking_code is not found")

        # read the file again to compare
        if os.path.isfile(file_store_vaccine):
            with open(file_store_vaccine, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_new = ""

        self.assertEqual(hash_new, hash_original)

    @freeze_time("2023-03-18")
    def test_deliver_product_no_shipments_store(self):
        """path: shipments_store is not found, so remove shimpents_store.json"""
        file_shipments_store = JSON_FILES_PATH + "shipments_store.json"
        if os.path.isfile(file_shipments_store):
            os.remove(file_shipments_store)

        my_manager = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            my_manager.deliver_product(
                "847dfd443d86c9c222242010c11a44bd9a09c37b42b6e956db97ba173abefe83")
        self.assertEqual(context_manager.exception.message, "shipments_store not found")

    @freeze_time("2023-03-18")
    def test_deliver_product_shipments_store_is_empty(self):
        """for testing: shipments_store is empty"""
        #write a shipments_store empty
        file_shipments_store = JSON_FILES_PATH + "shipments_store.json"
        data_list=[]
        with open(file_shipments_store, "w", encoding="utf-8", newline="") as file:
            json.dump(data_list, file, indent=2)

        my_manager = OrderManager()
        with self.assertRaises(OrderManagementException) as context_manager:
            my_manager.deliver_product(
                "847dfd443d86c9c222242010c11a44bd9a09c37b42b6e956db97ba173abefe83")
        self.assertEqual(context_manager.exception.message, "tracking_code is not found")
