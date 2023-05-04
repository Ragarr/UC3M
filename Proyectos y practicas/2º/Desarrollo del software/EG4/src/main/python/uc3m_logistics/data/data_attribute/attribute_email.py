"""Module for the TrackingCode class."""
from uc3m_logistics.data.data_attribute.attribute import Attribute


class Email(Attribute):
    """Class representing the tracking code"""
    def __init__(self, attr_value):
        """Constructor"""
        super().__init__()
        self._error_message = "contact email is not valid"
        self._validation_pattern = r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$'
        self._value = self._validate(attr_value)
