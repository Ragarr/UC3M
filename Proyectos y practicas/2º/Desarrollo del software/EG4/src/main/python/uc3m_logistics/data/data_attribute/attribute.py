"""Module"""
import re
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from uc3m_logistics.config.order_manager_config import ERRORLABEL


class Attribute:
    """Class representing an attribute"""
    def __init__(self):
        """Constructor"""
        self._value = ""
        self._error_message = ""
        self._validation_pattern = r""

    def _validate(self, value: str):
        """Method to validate the attribute value"""
        attr_regex = re.compile(self._validation_pattern)
        regex_match = attr_regex.fullmatch(value)
        if not regex_match:
            raise OrderManagementException(self._error_message)
        return value

    @classmethod
    def validate_key_label(cls, data, label):
        """Validate key level"""
        try:
            output = data[label]
        except KeyError as ex:
            raise OrderManagementException(ERRORLABEL) from ex
        return output

    @property
    def value(self):
        """Property representing the attribute value"""
        return self._value

    @value.setter
    def value(self, value):
        """Setter for the attribute value"""
        self._value = self._validate(value)

    @property
    def error_message(self):
        """Property representing the error message to be displayed"""
        return self._error_message

    @property
    def validation_pattern(self):
        """Property representing the validation pattern"""
        return self._validation_pattern
