"""Imports"""
import json
from uc3m_logistics.store.json_store_master import JsonStoreMaster
from uc3m_logistics.config.order_manager_config import JSON_FILES_PATH, ERRORFORMAT, ERRORSHIPNOTFOUND
from uc3m_logistics.exception.order_management_exception import OrderManagementException


class JsonShipping(JsonStoreMaster):
    """Class for storing the orders in a JSON file"""
    _FILE_PATH = JSON_FILES_PATH + "shipments_store.json"
    _data_list = []
    _ID_FIELD = "_OrderRequest__order_id"
    _instance = None

    @staticmethod
    def __new__(self):
        if JsonShipping._instance is None:
            JsonShipping._instance = JsonStoreMaster.__new__(self)
        return JsonShipping._instance

    @classmethod
    def read_shipping_store(cls) -> list:
        """
        Method for reading the shipments store
        :return: list of dictionaries with the data of the shipments
        """
        try:
            with open(cls._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as ex:
            raise OrderManagementException(ERRORFORMAT) from ex
        except FileNotFoundError as ex:
            raise OrderManagementException(ERRORSHIPNOTFOUND) from ex
        return data_list
