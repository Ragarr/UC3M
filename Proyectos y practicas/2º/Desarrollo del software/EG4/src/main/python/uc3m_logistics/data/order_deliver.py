"""Module that contains the OrderDeliver class."""
from datetime import datetime
from uc3m_logistics.data.data_attribute.attribute_tracking_code import TrackingCode
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from uc3m_logistics.store.json_shipments_delivered import JsonDelivered
from uc3m_logistics.store.json_shipments_stores import JsonShipping
from uc3m_logistics.config.order_manager_config import ERRORDELIVERYDATE


class OrderDeliver:
    """Class that represents an order deliver."""
    def __init__(self, tracking_code):
        """Constructor """
        self._tracking_code = TrackingCode(tracking_code).value
        self._deliver_date = str(datetime.utcnow())
        # Check Shipping
        data_list = JsonShipping.read_shipping_store()
        delivery_timestamp = JsonDelivered.find_tracking_code(data_list, tracking_code)
        self.check_date(delivery_timestamp)

    @classmethod
    def check_date(cls, delivery_timestamp):
        """
        Method for checking the delivery date
        :param delivery_timestamp: timestamp of the delivery date
        """
        today = datetime.today().date()
        delivery_date = datetime.fromtimestamp(delivery_timestamp).date()
        if delivery_date != today:
            raise OrderManagementException(ERRORDELIVERYDATE)
