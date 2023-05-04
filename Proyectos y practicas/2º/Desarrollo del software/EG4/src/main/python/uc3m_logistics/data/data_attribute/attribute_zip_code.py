"""Module"""
from uc3m_logistics.data.data_attribute.attribute import Attribute
from uc3m_logistics.exception.order_management_exception import OrderManagementException


class ZipCode(Attribute):
    """Class representing the zip code of the client"""
    def __init__(self, attr_value: str):
        """Constructor"""
        super().__init__()
        self._error_message = "zip code is not valid"
        self._validation_pattern = r"^[0-9]{5}"
        self._value = self._validate(attr_value)

    _error_value = "value is not valid"
    _error_value_format = "value format is not valid"

    @classmethod
    def _validate(cls, value: str):
        if value.isnumeric() and len(value) == 5:
            if int(value) > 52999 or int(value) < 1000:
                raise OrderManagementException(cls._error_value)
        else:
            raise OrderManagementException(cls._error_value_format)
        return value
