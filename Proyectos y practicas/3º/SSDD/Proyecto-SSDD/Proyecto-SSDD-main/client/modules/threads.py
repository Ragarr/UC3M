import threading
import socket
import time
from .connectionFuns import *

class ServerThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(ServerThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.__ip = None
        self.__port = None
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to localhost and any available port
        self.sock.bind((get_host_ip(), 0))
        # get the port number
        self.__port = self.sock.getsockname()[1]
        # get the ip address
        self.__ip = get_host_ip()
        # listen for incoming connections
        self.sock.listen()
        # print(f"Server started at {self.__ip}:{self.__port}")


    @property
    def ip(self):
        return self.__ip
    
    @property
    def port(self):
        return self.__port
    
    @property
    def sock(self):
        return self.__sock
    

    def stop(self):
        """
        Pause the server thread. This method closes the socket and sets the stop event.
        """
        self.sock.close()
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    
    def kill(self):
        """
        Stop the server thread and wait for it to finish.
        """
        self.stop()
        self.join()
    
    def close(self):
        self.sock.close()

    def run(self):
        """ 
        Start the server thread. This method listens for incoming connections and creates a new thread to handle each connection.
        """
        while not self.stopped():
            # check for new connection, the timout is necessary to check if the thread is stopped
            self.sock.settimeout(0.1)
            try:
                # accept a new connection
                conn, addr = self.sock.accept()
                # create a new detached thread to handle the connection
                connThread = threading.Thread(target=handleConnection, args=(conn,))
                connThread.daemon = True
                connThread.start()
            except socket.timeout:
                # check if the thread is stopped
                continue
            except ValueError:
                continue
            except OSError as e:
                if self.stopped():
                    break
                else:
                    raise e            
            