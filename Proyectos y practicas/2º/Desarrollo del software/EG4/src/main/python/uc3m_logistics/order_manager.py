"""MODULE: order_manager.py. This module contains the class OrderManager
and the methods for managing the orders process"""
from uc3m_logistics.data.order_request import OrderRequest
from uc3m_logistics.data.order_shipping import OrderShipping
from uc3m_logistics.data.order_deliver import OrderDeliver
from uc3m_logistics.store.json_store_orders import JsonStoreOrders
from uc3m_logistics.store.json_shipments_stores import JsonShipping
from uc3m_logistics.store.json_shipments_delivered import JsonDelivered


class OrderManager:
    """Class for providing the methods for managing the orders process"""

    def __init__(self):
        pass

    # pylint: disable=too-many-arguments
    @staticmethod
    def register_order(product_id: str, order_type: str, address: str, phone_number: str,
                       zip_code: str) -> OrderRequest:
        """
        Register the orders into the order's file
        :param product_id: string with the product id
        :param order_type: string with the order type
        :param address: string with the address
        :param phone_number: string with the phone number
        :param zip_code: string with the zip code
        :return: OrderRequest object with the order data
        """
        my_order = OrderRequest(product_id,
                                order_type,
                                address,
                                phone_number,
                                zip_code)

        JsonStoreOrders.add_item(my_order)
        return my_order.order_id

    # pylint: disable=too-many-locals
    @staticmethod
    def send_product(input_file: str) -> str:
        """
        Sends the order included in the input_file
        :param input_file: string with the path of the input file
        :return: tracking code of the shipment"""
        my_sign = OrderShipping(input_file)
        JsonShipping.add_item(my_sign)
        return my_sign.tracking_code

    @staticmethod
    def deliver_product(tracking_code: str) -> bool:
        """
        Register the delivery of the product
        :param tracking_code: string with the tracking code
        :return: True if the product was delivered
        """
        deliver = OrderDeliver(tracking_code)
        JsonDelivered.add_item(deliver)
        return True
