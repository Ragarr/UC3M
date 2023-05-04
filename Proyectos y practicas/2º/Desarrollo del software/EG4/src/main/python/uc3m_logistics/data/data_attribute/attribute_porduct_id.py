"""Module"""
from uc3m_logistics.data.data_attribute.attribute import Attribute, OrderManagementException


class ProductId(Attribute):
    """Class representing the product id"""

    def __init__(self, value):
        super().__init__()
        self._error_message = "Invalid EAN13 code string"
        self._validation_pattern = r"^[0-9]{13}$"
        self._value = self._validate(value)

    def _validate(self, value: str) -> str:
        """
        method for validating an ean13 code
        :param value: string with the ean13 code to be validated
        :return: True if the ean13 is right, or False in other case
        """
        # Then, we calculate the checksum
        super()._validate(value)
        checksum = 0
        code_read = -1

        for i, digit in enumerate(value):
            try:
                current_digit = int(digit)
            except ValueError as v_e:
                raise OrderManagementException("Invalid EAN13 code string") from v_e
            if i == 0:
                code_read = current_digit
            else:
                if i % 2 != 0:
                    checksum += current_digit * 3
                else:
                    checksum += current_digit

        # Finally, we check if the checksum is correct
        control_digit = (10 - (checksum % 10)) % 10
        if code_read != -1 and code_read == control_digit:
            return value
        raise OrderManagementException("Invalid EAN13 control digit")
