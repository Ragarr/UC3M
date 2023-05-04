"""Module"""
from uc3m_logistics.data.data_attribute.attribute import Attribute


class PhoneNumber(Attribute):
    """Class representing the phone number of the client"""
    def __init__(self, attr_value: str):
        """Constructor"""
        super().__init__()
        self._error_message = "phone number is not valid"
        self._validation_pattern = r"^(\+)[0-9]{11}"
        self._value = self._validate(attr_value)
