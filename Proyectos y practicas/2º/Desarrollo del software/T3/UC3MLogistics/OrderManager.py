"""
This file is part of UC3MLogistics.
is used to manage the orders
"""
import json
import re
from .OrderMangementException import OrderManagementException
from .OrderRequest import OrderRequest


class OrderManager:
    """manages codes of the orders """
    def __init__(self):
        """Constructor"""

    @staticmethod
    def ValidateEAN13(ean13):
        # regex pattern for ean13
        pattern = r"^[0-9]{13}$"
        # check if the ean13 is valid
        if not re.match(pattern, ean13):
            return False
        # calculate the check digit
        check_digit = 0
        for i in range(12):
            if (i+1) % 2 == 0:
                check_digit += 3*int(ean13[i])
            else:
                check_digit += int(ean13[i])
        check_digit = 10 - (check_digit % 10)
        if check_digit == 10:
            check_digit = 0
        # check if the check digit is correct
        if check_digit != int(ean13[12]):
            return False
        return True

    def ReadproductcodefromJSON(self, file):
        """Reads the product code from a JSON file"""

        try:
            with open(file, encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise OrderManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise OrderManagementException("JSON decode Error - Wrong JSON Format") from e

        try:
            product = data["id"]
            ph = data["phoneNumber"]
            req = OrderRequest(product, ph)
        except KeyError as e:
            raise OrderManagementException("JSON decode Error - Invalid JSON Key") from e
        if not self.ValidateEAN13(product):
            raise OrderManagementException("Invalid PRODUCT code")
        # Close the file
        return req
