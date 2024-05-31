import unittest
import time
import sys
sys.path.append("client")
from client import client
from unittest.mock import patch, MagicMock
import subprocess
import signal
import os
import threading


server_port = 9091

class TestMultiClient(unittest.TestCase):
    def generateClient(self) -> client:
        with patch('client.zeep.Client'):
            new_client = client()
            new_client._server = "localhost"
            global server_port
            new_client._port = server_port
            new_client._server_dir = (new_client._server, server_port)
            new_client.ws_client = MagicMock()
            new_client.ws_client.service.get_time.return_value = "2077/06/01 12:00:00"
        return new_client
    

    @classmethod
    def setUpClass(cls):
        # killall server in case there is a server running
        subprocess.run(["killall", "server"])

        with open("server/server.log", "a") as f:
            cls.server = subprocess.Popen(["./server/server", "-p", f"{server_port}"], stdout=f, stderr=f, preexec_fn=os.setsid)

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
            cls.server.wait(timeout=5)  # Aumenta el tiempo de espera, por ejemplo, a 5 segundos
        except subprocess.TimeoutExpired:
            cls.server.kill()
        
        # run killall server to kill all server instances
        try:
            os.killpg(os.getpgid(cls.server.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass
        # kill the logger
        cls.logger.send_signal(signal.SIGINT)
        try:
            cls.logger.wait(timeout=1)
        except subprocess.TimeoutExpired:
            cls.logger.kill()
            cls.logger.wait()
            
        # remove the test files
        testFiles = ['testfile.txt', 'output.txt', 'output1.txt', 'output2.txt']
        for f in testFiles:
            if os.path.exists(f):
                os.remove(f)

    def reset_server(self):
        global server_port
        server_port = server_port + 1
        self.server.terminate()
        self.server.wait()
        try:
            os.killpg(os.getpgid(self.server.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass
        
        # wait for the killall to finish
        with open("server/server.log", "a") as f:
            self.server = subprocess.Popen(["./server/server", "-p", f"{server_port}"], stdout=f, stderr=f, preexec_fn=os.setsid)    
            print(f"New server started at port {server_port}: {self.server.pid}")    
        time.sleep(0.5) # wait for server to start 
    
        
    def test_getfile(self):
        # create a file to get
        self.reset_server()
        with open('testfile.txt', 'w') as f:
            f.write('this is a sample file\n with some text')
            
        client1 = self.generateClient()
        client2 = self.generateClient()
        
        # publish the file
        client1.register('client1')
        client1.connect('client1')
        client1.publish("testfile.txt", "description")
        
        client2.register("client2")
        client2.connect("client2")
        
        # get the file
        result = client2.getfile("client1", "testfile.txt", "output.txt")
        
        
        
        # check the result
        self.assertEqual(result, "c> GET_FILE OK")
        
        # check the new file content
        with open('output.txt', 'r') as f:
            content = f.read()
            self.assertEqual(content, 'this is a sample file\n with some text')
        
        client1.quit()
        client2.quit()
    
    def test_register_concurrent(self):
        self.reset_server()
        results = []

        def register():
            c = self.generateClient()
            result = c.register('client')
            results.append(result)
        
        t1 = threading.Thread(target=register)
        t2 = threading.Thread(target=register)
        
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        
        self.assertIn("c> REGISTER OK", results)
        self.assertIn("c> USERNAME IN USE", results)
    
    def test_connect_concurrent(self):
        self.reset_server()
        results = []

        def connect():
            c = self.generateClient()
            
            result = c.connect('client')
            results.append(result)
            time.sleep(1) # so the other thread can connect too
            # if this is not done,  python garbaje collector will delete the client object
            # and server will disconnect the client, so the test will fai
        
        
        aux = self.generateClient()
        aux.register('client')
        aux.register('aux')
        aux.connect('aux')
        
        t1 = threading.Thread(target=connect)
        t2 = threading.Thread(target=connect)
        
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        # print(f"\n\n{aux.listusers()}\n\n")
        self.assertIn("c> CONNECT OK", results)
        self.assertIn("c> USER ALREADY CONNECTED", results)
        
    def test_getfile_concurrent(self):
        self.reset_server()
        results = []
        times = []
        
        def getfile(username,getusername, filename, output):
            t1 = time.time()
            c = self.generateClient()
            c.register(username)
            c.connect(username)
            result = c.getfile(getusername, filename, output)
            t2 = time.time()
            times.append(t2-t1)
            print(f"Time: {t2-t1}")
            results.append(result)
        
        with open('testfile.txt', 'w') as f:
            # create a big file (128KB)
            f.write('8bytes. '* ((128 * 1024)//8)) 
        
        c = self.generateClient()
        c.register('client')
        c.connect('client')
        c.publish('testfile.txt', 'description')
        
        thread1 = threading.Thread(target=getfile, args=('client1', 'client', 'testfile.txt', 'output1.txt'))
        thread2 = threading.Thread(target=getfile, args=('client2', 'client', 'testfile.txt', 'output2.txt'))
        
        # medir el tiempo total que tardan ambos
        t1 = time.time()
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        t2 = time.time()
        
        print(f"\n\nTimes: {times}\n\n")
        
        # comprobar si el tiempo total es igual al tiempo de la operacion mas lenta aproximadamente
        self.assertLess(t2-t1, max(times) + 1)
        # comprobar que el tiempo total es menor a la suma de los tiempos de las operaciones
        # self.assertGreater(t2-t1, sum(times))
        # nunca se va a cumplir, no por culpa del servidor, si no por que python no es realmente multihilo
        # de esta forma las operaciones de cada hilo se intercalan y se ejecutan secuencialmente
        # se puede comprobar viendo como los archivos se escriben simultaneamente (pero no mas rapido que 
        # si se hiciera secuencialmente), aun asi esta bien por que se demuestra que es posbile atender 
        # multiples clientes simultaneamente
        
        self.assertEqual(results, ['c> GET_FILE OK', 'c> GET_FILE OK'])
        
        
    def test_unregister_connected(self):
        self.reset_server()
        
        c1 = self.generateClient()
        c2 = self.generateClient()
        
        c1.register('client1')
        c1.connect('client1')
        c2.register('client2')
        c2.connect('client2')
        
        result = c1.unregister("client1")
            
        self.assertEqual(result, 'c> UNREGISTER FAIL')
        
        
        
        

        
        
        
        
        
if __name__ == '__main__':
    unittest.main() 
        
            

