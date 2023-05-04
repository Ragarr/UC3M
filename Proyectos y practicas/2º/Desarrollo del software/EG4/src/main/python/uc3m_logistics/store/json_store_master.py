"""imports"""
import json
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from uc3m_logistics.config.order_manager_config import ERRORFORMAT, ERRORFILEPATH


class JsonStoreMaster:
    """Class for storing the orders in a JSON file"""
    _FILE_PATH = ""
    _data_list = []
    _ID_FIELD = ""

    @classmethod
    def __init__(cls):
        """Constructor"""
        cls.get_data_list_from_json()

    @classmethod
    def get_data_list_from_json(cls) -> None:
        """Method"""
        try:
            with open(cls._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                cls._data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init data
            cls._data_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException(ERRORFORMAT) from ex

    @classmethod
    def store_order(cls) -> None:
        """
        Method for saving the orders store
        """
        try:
            with open(cls._FILE_PATH, "w", encoding="utf-8", newline="") as file:
                json.dump(cls._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise OrderManagementException(ERRORFILEPATH) from ex

    @classmethod
    def is_item_in_data_list(cls, item_value: str) -> str or bool:
        """
        Method for search if item is in data_list
        """
        item_found = False
        for item in cls._data_list:
            if item[cls._ID_FIELD] == item_value:
                item_found = item
        return item_found

    @classmethod
    def add_item(cls, item) -> None:
        """
        Method for adding item in the store
        """
        cls.get_data_list_from_json()
        cls._data_list.append(item.__dict__)
        cls.store_order()
