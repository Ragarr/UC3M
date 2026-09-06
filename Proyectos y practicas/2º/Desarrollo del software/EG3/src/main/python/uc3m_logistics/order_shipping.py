"""Contains the class OrderShipping"""
from datetime import datetime
import hashlib
# pylint: disable=too-many-instance-attributes


class OrderShipping:
    """Class representing the information required for shipping of an order"""

    def __init__(self, product_id, order_id, delivery_email, order_type):
        self.__alg = "SHA-256"
        self.__type = "UC3M"
        self.__product_id = product_id
        self.__order_id = order_id
        self.__delivery_email = delivery_email
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)

        if order_type == "Regular":
            delivery_days = 7
        else:
            delivery_days = 1

        # timestamp is represented in seconds.microseconds
        # __delivery_day must be expressed in seconds to be added to the timestap
        self.__delivery_day = self.__issued_at + (delivery_days * 24 * 60 * 60)
        self.__tracking_code = hashlib.sha256(self.__signature_string().encode()).hexdigest()

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + self.__alg + ",typ:" + str(self.__type) + ",order_id:" + \
               str(self.__order_id) + ",issuedate:" + str(self.__issued_at) + \
               ",deliveryday:" + str(self.__delivery_day) + "}"

    @property
    def product_id(self):
        """Property that represents the product_id of the patient"""
        return self.__product_id

    @product_id.setter
    def product_id(self, value):
        self.__product_id = value

    @property
    def order_id(self):
        """Property that represents the order_id"""
        return self.__order_id

    @order_id.setter
    def order_id(self, value):
        self.__order_id = value

    @property
    def email(self):
        """Property that represents the phone number of the client"""
        return self.__delivery_email

    @email.setter
    def email(self, value):
        self.__delivery_email = value

    @property
    def issued_at(self):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at(self, value):
        self.__issued_at = value

    @property
    def delivery_day(self):
        """Returns the delivery day for the order"""
        return self.__delivery_day

    @property
    def tracking_code(self):
        """Returns the tracking code for the order"""
        return self.__tracking_code

    @property
    def _dict_(self):
        return self.__dict__
