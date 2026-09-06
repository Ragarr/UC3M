"""Module"""
from uc3m_logistics.data.data_attribute.attribute import Attribute


class OrderType(Attribute):
    """Class representing the order type"""

    def __init__(self, attr_value: str):
        """Constructor"""
        super().__init__()
        self._error_message = "order_type is not valid"
        self._validation_pattern = r"(Regular|Premium)"
        self._value = self._validate(attr_value)
