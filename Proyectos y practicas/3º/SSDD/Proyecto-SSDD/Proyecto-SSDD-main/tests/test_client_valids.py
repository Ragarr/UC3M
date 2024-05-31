import unittest
import socket
import time
import sys
sys.path.append("client")
from client import client
from unittest.mock import patch, MagicMock

class TestClient(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.server_ip = "localhost"
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
        

    @patch('client.socket.socket')
    def test_register(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x00'
        result = self.client.register("test_user")
        self.assertEqual(result, "c> REGISTER OK")

    @patch('client.socket.socket')
    def test_unregister(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x01'
        result = self.client.unregister("test_user")
        self.assertEqual(result, "c> USER DOES NOT EXIST")

    @patch('client.socket.socket')
    def test_connect(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x00'
        self.client._local_server_thread = MagicMock()
        result = self.client.connect("test_user")
        self.assertEqual(result, "c> CONNECT OK")
        self.assertEqual(self.client._conected_user, "test_user")

    @patch('client.socket.socket')
    def test_disconnect(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x00'
        self.client._conected_user = "test_user"

        # Crear el hilo local_server_thread antes de desconectarse

        self.client.connect("test_user")

        result = self.client.disconnect("test_user")
        self.assertEqual(result, "c> DISCONNECT OK")
        self.assertIsNone(self.client._conected_user)

        # Verificar que el hilo se haya detenido y se haya unido correctamente
        if self.client._local_server_thread is not None:
            self.client._local_server_thread.stop.assert_called_once()
            self.client._local_server_thread.join.assert_called_once()

    @patch('client.socket.socket')
    def test_publish(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x00'
        self.client._conected_user = "test_user"
        result = self.client.publish("test_file.txt", "Test file description")
        self.assertEqual(result, "c> PUBLISH OK")

    @patch('client.socket.socket')
    def test_delete(self, mock_socket):
        mock_socket.return_value.recv.return_value = b'\x03'
        self.client._conected_user = "test_user"
        result = self.client.delete("test_file.txt")
        self.assertEqual(result, "c> DELETE FAIL, CONTENT NOT PUBLISHED")

    @patch('client.socket.socket')
    def test_listusers(self, mock_socket):
        mock_socket.return_value.recv.side_effect = [b'\x00', b'2\0', b'user1\0', b'127.0.0.1\0', b'5000\0', b'user2\0', b'192.168.1.1\0', b'5001\0']
        self.client._conected_user = "test_user"
        result = self.client.listusers()
        expected_output = "c> LIST_USERS OK\n\tuser1 127.0.0.1 5000\n\tuser2 192.168.1.1 5001\n"
        self.assertEqual(result, expected_output)

    @patch('client.socket.socket')
    def test_listcontent(self, mock_socket):
        mock_socket.return_value.recv.side_effect = [b'\x00', b'1\0', b'file1.txt\0', b'Description 1\0']
        self.client._conected_user = "test_user"
        result = self.client.listcontent("test_user")
        expected_output = "c> LIST_CONTENT OK\n\tfile1.txt Description 1\n"
        self.assertEqual(result, expected_output)

    @patch('client.socket.socket')
    @patch('client.client.listusers')
    def test_getfile(self, mock_listusers, mock_socket):
        mock_listusers.return_value = "c> LIST_USERS OK\n\ttest_user 127.0.0.1 5000\n"
        mock_socket.return_value.recv.side_effect = [b'\x00', b'test_data', b''] # la cadena de bytes vacia simula el fin del archivo
        self.client._conected_user = "test_user"
        result = self.client.getfile("test_user", "test_file.txt", "local_file.txt")
        self.assertEqual(result, "c> GET_FILE OK")
        with open("local_file.txt", "r") as f:
            content = f.read()
            self.assertEqual(content, "test_data")

if __name__ == '__main__':
    unittest.main()