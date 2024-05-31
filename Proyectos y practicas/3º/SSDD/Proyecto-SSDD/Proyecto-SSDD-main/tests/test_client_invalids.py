import unittest
import socket
import sys
sys.path.append("client")
from client import client
from unittest.mock import MagicMock, patch
import threading

class TestClientErrorCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_ip = "127.0.0.1"
        cls.server_port = 9091
        # sustituir el constructor de zeep.Client por un MagicMock 
        # para evitar errores de conexión con el servicio web ya que 
        # no se está ejecutando
        with patch('client.zeep.Client'):
            cls.client = client()
            cls.client.ws_client = MagicMock()
            cls.client.ws_client.service.get_time.return_value = "2077/06/01 12:00:00"
        cls.client._server = cls.server_ip
        cls.client._port = cls.server_port
        cls.client._server_dir = (cls.server_ip, cls.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.client.quit()
        print_active_threads()
        
    def setUp(self):
        with patch('client.zeep.Client'):
            self.client = client()
            self.client.ws_client = MagicMock()
            self.client.ws_client.service.get_time.return_value = "2077/06/01 12:00:00"
        self.client._server = self.server_ip
        self.client._port = self.server_port
        self.client._server_dir = (self.server_ip, self.server_port)
        
    def tearDown(self):
        self.client.quit()
        
        


    @patch('client.socket.socket')
    def test_register_error1(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x01'
        result = self.client.register("test_user")
        self.assertEqual(result, "c> USERNAME IN USE")

    @patch('client.socket.socket')
    def test_register_error2(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x02'
        result = self.client.register("test_user")
        self.assertEqual(result, "c> REGISTER FAIL")

    @patch('client.socket.socket')
    def test_unregister_error1(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x01'
        result = self.client.unregister("test_user")
        self.assertEqual(result, "c> USER DOES NOT EXIST")

    @patch('client.socket.socket')
    def test_unregister_error2(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x02'
        result = self.client.unregister("test_user")
        self.assertEqual(result, "c> UNREGISTER FAIL")

    @patch('client.socket.socket')
    def test_connect_error1(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x01'
        result = self.client.connect("test_user")
        self.assertEqual(result, "c> CONNECT FAIL, USER DOES NOT EXIST")
    
    @patch('client.socket.socket')
    def test_connect_error2(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x02'
        result = self.client.connect("test_user")
        self.assertEqual(result, "c> USER ALREADY CONNECTED")
    
    @patch('client.socket.socket')
    def test_connect_error3(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x03'
        result = self.client.connect("test_user")
        self.assertEqual(result, "c> CONNECT FAIL")
    
    @patch('client.socket.socket')
    def test_publish_error1(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x01'
        self.client._conected_user = "test_user"
        result = self.client.publish("test_file.txt", "Test file description")
        self.assertEqual(result, "c> PUBLISH FAIL, USER DOES NOT EXIST")
    
    @patch('client.socket.socket')
    def test_publish_error2(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x02'
        self.client._conected_user = "test_user"
        result = self.client.publish("test_file.txt", "Test file description")
        self.assertEqual(result, "c> PUBLISH FAIL, USER NOT CONNECTED")
    
    @patch('client.socket.socket')
    def test_publish_error3(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x03'
        self.client._conected_user = "test_user"
        result = self.client.publish("test_file.txt", "Test file description")
        self.assertEqual(result, "c> PUBLISH FAIL, CONTENT ALREADY PUBLISHED")
    
    @patch('client.socket.socket')
    def test_publish_error4(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x04'
        self.client._conected_user = "test_user"
        result = self.client.publish("test_file.txt", "Test file description")
        self.assertEqual(result, "c> PUBLISH FAIL")
        
    @patch('client.socket.socket')
    def test_delete_error1(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x01'
        self.client._conected_user = "test_user"
        result = self.client.delete("test_file.txt")
        self.assertEqual(result, "c> DELETE FAIL, USER DOES NOT EXIST")
    
    @patch('client.socket.socket')
    def test_delete_error2(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x02'
        self.client._conected_user = "test_user"
        result = self.client.delete("test_file.txt")
        self.assertEqual(result, "c> DELETE FAIL, USER NOT CONNECTED")
    
    @patch('client.socket.socket')
    def test_delete_error3(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x03'
        self.client._conected_user = "test_user"
        result = self.client.delete("test_file.txt")
        self.assertEqual(result, "c> DELETE FAIL, CONTENT NOT PUBLISHED")
    
    @patch('client.socket.socket')
    def test_delete_error4(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x04'
        self.client._conected_user = "test_user"
        result = self.client.delete("test_file.txt")
        self.assertEqual(result, "c> DELETE FAIL")
    
    @patch('client.socket.socket')
    def test_list_users_error1(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x01'
        self.client._conected_user = "test_user"
        result = self.client.listusers()
        self.assertEqual(result, "c> LIST_USERS FAIL, USER DOES NOT EXIST")
    
    @patch('client.socket.socket')
    def test_list_users_error2(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x02'
        self.client._conected_user = "test_user"
        result = self.client.listusers()
        self.assertEqual(result, "c> LIST_USERS FAIL, USER NOT CONNECTED")
    
    @patch('client.socket.socket')
    def test_list_users_error3(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x03'
        self.client._conected_user = "test_user"
        result = self.client.listusers()
        self.assertEqual(result, "c> LIST_USERS FAIL")
    
    @patch('client.socket.socket')
    def test_list_content_error1(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x01'
        self.client.register("test_user")
        self.client._conected_user = "test_user"
        result = self.client.listcontent("test_user")
        self.assertEqual(result, "c> LIST_CONTENT FAIL, USER DOES NOT EXIST")
    
    @patch('client.socket.socket')
    def test_list_content_error2(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x02'
        self.client._conected_user = "test_user"
        result = self.client.listcontent("test_user")
        self.assertEqual(result, "c> LIST_CONTENT FAIL, USER NOT CONNECTED")
    
    @patch('client.socket.socket')
    def test_list_content_error3(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x03'
        self.client._conected_user = "test_user"
        result = self.client.listcontent("test_user")
        self.assertEqual(result, "c> LIST_CONTENT FAIL, REMOTE USER DOES NOT EXIST")
    
    @patch('client.socket.socket')
    def test_list_content_error4(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x04'
        self.client._conected_user = "test_user"
        result = self.client.listcontent("test_user")
        self.assertEqual(result, "c> LIST_CONTENT FAIL")
    
    @patch('client.socket.socket')
    def test_disconnect_error1(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x01'
        self.client._conected_user = "test_user"
        self.client.connect("test_user")
        result = self.client.disconnect("test_user")
        self.assertEqual(result, "c> DISCONNECT FAIL / USER DOES NOT EXIST")
    
    @patch('client.socket.socket')
    def test_disconnect_error2(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x02'
        self.client._conected_user = "test_user"
        self.client.connect("test_user")
        result = self.client.disconnect("test_user")
        self.assertEqual(result, "c> DISCONNECT FAIL / USER NOT CONNECTED")
    
    @patch('client.socket.socket')
    def test_disconnect_error3(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x03'
        self.client._conected_user = "test_user"
        self.client.connect("test_user")
        result = self.client.disconnect("test_user")
        self.assertEqual(result, "c> DISCONNECT FAIL")
        
        
        
def print_active_threads():
    print("Subprocesos activos:")
    for thread in threading.enumerate():
        print(f"ID: {thread.ident}, Nombre: {thread.name}, Estado: {thread.is_alive()}")

   
        

if __name__ == '__main__':
    unittest.main()
