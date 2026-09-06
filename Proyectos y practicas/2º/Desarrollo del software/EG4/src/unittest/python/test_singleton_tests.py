import unittest
from uc3m_logistics.store.json_shipments_stores import JsonShipping
from uc3m_logistics.store.json_shipments_delivered import JsonDelivered
from uc3m_logistics.store.json_store_orders import JsonStoreOrders

class SingletonTest(unittest.TestCase):
    def test_singleton(self):
        my_instance1 = JsonStoreOrders()
        my_instance2 = JsonStoreOrders()
        self.assertEqual(my_instance1,my_instance2)

    def test_singletonMeta(self):
        my_instance1 = JsonShipping()
        my_instance2 = JsonShipping()
        self.assertEqual(my_instance1,my_instance2)

    def test_singletonDelivered(self):
        my_instance1 = JsonDelivered()
        my_instance2 = JsonDelivered()
        self.assertEqual(my_instance1, my_instance2)

if __name__ == '__main__':
    unittest.main()