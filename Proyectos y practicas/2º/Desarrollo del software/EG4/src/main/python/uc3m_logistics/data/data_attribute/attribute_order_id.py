"""Module for the TrackingCode class."""
from uc3m_logistics.data.data_attribute.attribute import Attribute


class OrderId(Attribute):
    """Class representing the tracking code"""
    def __init__(self, attr_value):
        """Constructor"""
        super().__init__()
        self._error_message = "order id is not valid"
        self._validation_pattern = r"[0-9a-fA-F]{32}$"
        self._value = self._validate(attr_value)
