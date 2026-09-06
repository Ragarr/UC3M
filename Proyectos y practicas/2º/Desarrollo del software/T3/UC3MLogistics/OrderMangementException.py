"""
This module contains the OrderManagementException class.
is a subclass of Exception.
"""
class OrderManagementException(Exception):
    """
    Exception class for OrderManagement 
    """
    def __init__(self, message):
        """Constructor"""
        self.__message = message
        super().__init__(self.message)

    @property
    def message(self):
        """Message property"""
        return self.__message

    @message.setter
    def message(self,value):
        """Message property setter"""
        self.__message = value
