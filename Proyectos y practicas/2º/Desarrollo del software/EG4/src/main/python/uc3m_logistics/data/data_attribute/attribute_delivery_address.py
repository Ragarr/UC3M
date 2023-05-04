"""Module"""
from uc3m_logistics.data.data_attribute.attribute import Attribute


class DeliveryAddress(Attribute):
    """Class representing the delivery address"""

    def __init__(self, attr_value: str):
        """Constructor"""
        super().__init__()
        self._error_message = "address is not valid"
        self._validation_pattern = r"^(?=^.{20,100}$)(([a-zA-Z0-9]+\s)+[a-zA-Z0-9]+)$"
        self._value = self._validate(attr_value)
