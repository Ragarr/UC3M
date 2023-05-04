"""imports"""
from uc3m_logistics.store.json_store_master import JsonStoreMaster
from uc3m_logistics.config.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from uc3m_logistics.config.order_manager_config import ERRORREGISTEDORDER


class JsonStoreOrders(JsonStoreMaster):
    """Class for storing the orders in a JSON file"""
    _FILE_PATH = JSON_FILES_PATH + "orders_store.json"
    _data_list = []
    _ID_FIELD = "_OrderRequest__order_id"
    _instance = None

    # pylint: disable=all warnings
    @staticmethod
    def __new__(self):
        if JsonStoreOrders._instance is None:
            JsonStoreOrders._instance = JsonStoreMaster.__new__(self)
        return JsonStoreOrders._instance

    @classmethod
    def add_item(cls, item):
        """add_item"""
        cls.get_data_list_from_json()
        item_found = cls.is_item_in_data_list(item.order_id)
        if not item_found:
            cls._data_list.append(item.__dict__)
        else:
            raise OrderManagementException(ERRORREGISTEDORDER)
        cls.store_order()
