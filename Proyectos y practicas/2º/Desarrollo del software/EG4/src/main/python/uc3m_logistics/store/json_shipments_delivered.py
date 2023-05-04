"""Imports"""
from uc3m_logistics.store.json_store_master import JsonStoreMaster
from uc3m_logistics.config.order_manager_config import JSON_FILES_PATH, ERRORTRAKINGNOTFOUND
from uc3m_logistics.exception.order_management_exception import OrderManagementException


class JsonDelivered(JsonStoreMaster):
    """Class for storing the orders in a JSON file"""
    _FILE_PATH = JSON_FILES_PATH + "shipments_delivered.json"
    _data_list = []
    _ID_FIELD = "_OrderShipping__tracking_code"
    _instance = None
    _delivery_day = "_OrderShipping__delivery_day"

    @staticmethod
    def __new__(self):
        if JsonDelivered._instance is None:
            JsonDelivered._instance = JsonStoreMaster.__new__(self)
        return JsonDelivered._instance

    @classmethod
    def find_tracking_code(cls, data_list, tracking_code: str) -> str:
        """
        Method for finding the tracking code in the shipments store
        :param data_list: data of the shipment
        :param tracking_code: tracking code of the shipment
        :return: timestamp of the delivery date
        """
        item_found = False
        for item in data_list:
            if item[cls._ID_FIELD] == tracking_code:
                item_found = True
                delivery_timestamp = item[cls._delivery_day]
        if not item_found:
            raise OrderManagementException(ERRORTRAKINGNOTFOUND)
        return delivery_timestamp
