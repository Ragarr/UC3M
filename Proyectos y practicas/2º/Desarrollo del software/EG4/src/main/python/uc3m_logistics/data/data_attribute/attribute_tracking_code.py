"""Module for the TrackingCode class."""
from uc3m_logistics.data.data_attribute.attribute import Attribute


class TrackingCode(Attribute):
    """Class representing the tracking code"""
    def __init__(self, attr_value):
        """Constructor"""
        super().__init__()
        self._error_message = "tracking_code format is not valid"
        self._validation_pattern = r"[0-9a-fA-F]{64}$"
        self._value = self._validate(attr_value)
