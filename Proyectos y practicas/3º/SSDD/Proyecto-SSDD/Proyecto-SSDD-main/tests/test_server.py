from socket import gethostbyname
import sys
from unittest.mock import MagicMock, patch
sys.path.append("client")
from client import client
import unittest
import subprocess
import signal
import time
import os

server_port = 9091

class TestServer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # killall server in case there is a server running
        subprocess.run(["killall", "server"])

        with open("server/server.log", "a") as f:
            cls.server = subprocess.Popen(["./server/server", "-p", f"{server_port}"], stdout=f, stderr=f)
        time.sleep(0.5) # wait for server to start
        # start the logger
        with open("logger.log", "a") as f:
            cls.logger = subprocess.Popen(["./rpc_service/rpc_logger_server"], stdout=f, stderr=f)
        
        # asegurarse de que existe liblogger.so
        if not os.path.exists("server/liblogger.so"):
            raise FileNotFoundError("liblogger.so not found, is necessary to run the server")
        # add to the LD_LIBRARY_PATH the path to the server directory
        os.environ['LD_LIBRARY_PATH'] = os.getcwd() + '/server/'
        time.sleep(0.5) # server needs time to start
        
        
        
                    
        
    
    @classmethod
    def tearDownClass(cls):
        cls.server.send_signal(signal.SIGINT)
        try:
            cls.server.wait(timeout=1)
        except subprocess.TimeoutExpired:
            cls.server.kill()
        
        # run killall server to kill all server instances
        subprocess.run(["killall", "server"])
        
        # kill the logger
        cls.logger.send_signal(signal.SIGINT)
        try:
            cls.logger.wait(timeout=1)
        except subprocess.TimeoutExpired:
            cls.logger.kill()
            
        
        
    def reset_server(self):
        global server_port
        server_port = server_port + 1
        self.server.send_signal(signal.SIGINT)
        try:
            self.server.wait(timeout=1)
        except subprocess.TimeoutExpired:
            self.server.kill()
        with open("server/server.log", "a") as f:
            self.server = subprocess.Popen(["./server/server", "-p", f"{server_port}"], stdout=f, stderr=f)        
        # reset the client
        self.client.quit()
        with patch('client.zeep.Client'):
            self.client = client()
            self.client.ws_client = MagicMock()
            self.client.ws_client.service.get_time.return_value = "2077/06/01 12:00:00"
        self.client._server = gethostbyname("localhost")
        self.client._port = server_port
        self.client._server_dir = (self.client._server, self.client._port)
               
        time.sleep(0.5) # wait for server to start 
    
    def setUp(self) -> None:
        global server_port
        with patch('client.zeep.Client'):
            self.client = client()
            self.client.ws_client = MagicMock()
            self.client.ws_client.service.get_time.return_value = "2077/06/01 12:00:00"
        self.client._server = gethostbyname("localhost")
        self.client._port = server_port
        self.client._server_dir = (self.client._server, self.client._port)
    
    def tearDown(self) -> None:
        self.client.quit()
        

    def test_register(self):
        self.reset_server()
        output = self.client.register("test")
        self.assertEqual(output, "c> REGISTER OK")
        
    
    def test_register_fail1(self):
        self.reset_server()
        self.client.register("test")
        output = self.client.register("test")
        self.assertEqual(output, "c> USERNAME IN USE")
    
    def test_register_fail2(self):
        self.reset_server()
        output = self.client.register("")
        self.assertEqual(output, "c> REGISTER FAIL")
        
    def test_connect(self):
        self.reset_server()
        self.client.register("test")
        output = self.client.connect("test")
        self.assertEqual(output, "c> CONNECT OK")
    
    def test_connect_fail1(self):
        self.reset_server()
        output = self.client.connect("abc")
        self.assertEqual(output, "c> CONNECT FAIL, USER DOES NOT EXIST")
    
    def test_connect_fail2(self):
        self.reset_server()
        self.client.register("test")
        self.client.connect("test")
        output = self.client.connect("test")
        self.assertEqual(output, "c> USER ALREADY CONNECTED")
    

    def test_publish(self):
        self.reset_server()
        self.client.register("test")
        self.client.connect("test")
        output = self.client.publish("file.txt", "descr")
        self.assertEqual(output, "c> PUBLISH OK")
    
    
    def test_publish_fail1(self):
        self.client.register("test")
        output = self.client.publish("file.txt", "descr")
        self.assertEqual(output, "c> PUBLISH FAIL, USER NOT CONNECTED")
    
    def test_publish_fail2(self):
        self.client.register("test")
        self.client.connect("test")
        output = self.client.publish("file.txt", "descr")
        self.assertEqual(output, "c> PUBLISH FAIL, CONTENT ALREADY PUBLISHED")
    
    def test_delete(self):
        self.reset_server()
        global server_port
        self.client.register("test")
        self.client.connect("test")
        self.client.publish("file.txt", "descr")
        output = self.client.delete("file.txt")
        self.assertEqual(output, "c> DELETE OK")
    
    def test_delete_fail1(self):
        self.client.register("test")
        self.client.connect("test")
        output = self.client.delete("file.txt")
        self.assertEqual(output, "c> DELETE FAIL, CONTENT NOT PUBLISHED")
    
    def test_listusers(self):
        self.reset_server()
        global server_port
        self.client.register("test")
        self.client.connect("test")
        ip = self.client._local_server_thread.ip
        port = self.client._local_server_thread.port
        output = self.client.listusers()
        self.assertEqual(output, f"c> LIST_USERS OK\n\ttest {ip} {port}\n")
    
    def test_listusers_fail1(self):
        self.reset_server()
        self.client.register("test")
        output = self.client.listusers()
        self.assertEqual(output, "c> LIST_USERS FAIL, USER NOT CONNECTED")
        
    def test_listcontent(self):
        self.reset_server()
        global server_port
        self.client.register("test")
        self.client.connect("test")
        self.client.publish("file.txt", "descr")
        output = self.client.listcontent("test")
        self.assertEqual(output, "c> LIST_CONTENT OK\n\tfile.txt descr\n")
    
    
    def test_listcontent_fail1(self):
        self.reset_server()
        self.client.register("test")
        output = self.client.listcontent("test")
        self.assertEqual(output, "c> LIST_CONTENT FAIL, USER NOT CONNECTED")
    
    def test_listcontent_fail2(self):
        self.reset_server()
        self.client.register("test")
        self.client.connect("test")
        output = self.client.listcontent("abcd")
        self.assertEqual(output, "c> LIST_CONTENT FAIL, REMOTE USER DOES NOT EXIST")
    
    def test_disconnect(self):
        self.reset_server()
        global server_port
        self.client.register("test")
        self.client.connect("test")
        output = self.client.disconnect("test")
        self.assertEqual(output, "c> DISCONNECT OK")
    
    def test_disconnect_fail1(self):
        output = self.client.disconnect("test")
        self.assertEqual(output, "c> DISCONNECT FAIL / USER NOT CONNECTED")

        
    
    
tests_order = [
    "test_register",
    "test_register_fail1",
    "test_register_fail2",
    "test_connect",
    "test_connect_fail1",
    "test_connect_fail2",
    "test_publish",
    "test_publish_fail1",
    "test_publish_fail2",
    "test_delete",
    "test_delete_fail1",
    "test_listusers",
    "test_listusers_fail1",
    "test_listcontent",
    "test_listcontent_fail1",
    "test_listcontent_fail2",
    "test_disconnect",
    "test_disconnect_fail1"
]


test_suite = unittest.TestSuite()
for test in tests_order:
    test_suite.addTest(TestServer(test))

unittest.TextTestRunner().run(test_suite)

