""" 
OrderRequest class
This class is used to create an order request
"""

import json
from datetime import datetime


class OrderRequest:
    """
    OrderRequest class
    This class is used to create an order request
    """

    def __init__(self, idCode, phoneNumber):
        """Constructor for OrderRequest class"""
        self.__phoneNumber = phoneNumber
        self.__idCode = idCode
        justnow = datetime.utcnow()
        self.__timeStamp = datetime.timestamp(justnow)

    def __str__(self):
        """String representation of the class"""
        return "OrderRequest:" + json.dumps(self.__dict__)

    @property
    def phone(self):
        """phone number of the client"""
        return self.__phoneNumber

    @phone.setter
    def phone(self, value):
        """phone number of the client"""
        self.__phoneNumber = value

    @property
    def productCode(self):
        """Product code of the product to be ordered"""
        return self.__idCode

    @productCode.setter
    def productCode(self, value):
        """Product code of the product to be ordered"""
        self.__idCode = value

    @property
    def timeStamp(self):
        """time stamp of the creation of the instance"""
        return self.__timeStamp
