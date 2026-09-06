import argparse
import socket
from modules import ServerThread, recvUntilZero
import signal
import zeep
import os


class client:
    def __init__(self) -> None:
        self._server = None  # Server IP
        self._port = -1  # Server port
        self._server_dir = ()
        self._local_server_thread = None
        self._conected_user = None
        wsdl = os.environ.get("WSDL_URL", "http://localhost:8000/?wsdl")
        try:
            self.ws_client = zeep.Client(wsdl=wsdl)
        except ConnectionError as e:
            print(
                "Error connecting to web service: "
                + str(e)
                + "Is the web service running?"
            )
            raise e

    # ******************** METHODS ******************

    def register(self, user: str):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self._server_dir)
        result_code = 2
        try:
            sock.sendall("REGISTER\0".encode())
            sock.sendall((self.ws_client.service.get_time() + "\0").encode())
            sock.sendall((user + "\0").encode())
            result_code = int.from_bytes(sock.recv(1), byteorder="big")
        except Exception as e:
            result_code = 2
        finally:
            sock.close()

        if result_code == 0:
            return "c> REGISTER OK"
        elif result_code == 1:
            return "c> USERNAME IN USE"
        elif result_code == 2:
            return "c> REGISTER FAIL"

    def unregister(self, user):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result_code = 2
        try: # enviar solicitud de desregistro
            sock.connect(self._server_dir)
            sock.sendall("UNREGISTER\0".encode())
            sock.sendall((self.ws_client.service.get_time() + "\0").encode())
            sock.sendall((user + "\0").encode())
            result_code = int.from_bytes(sock.recv(1), byteorder="big")
        except Exception as e:
            result_code = 2
        finally:
            sock.close()

        if result_code == 0:
            return "c> UNREGISTER OK"
        elif result_code == 1:
            return "c> USER DOES NOT EXIST"
        elif result_code == 2:
            return "c> UNREGISTER FAIL"

    def connect(self, user):

        if self._conected_user is not None:
            return "c> USER ALREADY CONNECTED"

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result_code = 3
        
        # crear un hilo que escuche en el puerto seleccionado
        self._local_server_thread = ServerThread()
        self._local_server_thread.start()
        port = self._local_server_thread.port

        try: # conectar con el servidor y enviar la solicitud de conexión
            sock.connect(self._server_dir)
            sock.sendall("CONNECT\0".encode())
            sock.sendall((self.ws_client.service.get_time() + "\0").encode())
            sock.sendall((user + "\0").encode())
            sock.sendall((str(port) + "\0").encode())
            result_code = int.from_bytes(sock.recv(1), byteorder="big")
        except Exception as e:
            result_code = 3
        finally:
            sock.close()

        if result_code == 0:
            self._conected_user = user
            return "c> CONNECT OK"
        elif result_code == 1:
            return "c> CONNECT FAIL, USER DOES NOT EXIST"
        elif result_code == 2:
            return "c> USER ALREADY CONNECTED"
        elif result_code == 3:
            return "c> CONNECT FAIL"

    def disconnect(self, user):
        if self._conected_user is None:
            return "c> DISCONNECT FAIL / USER NOT CONNECTED"

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result_code = 3
        try: # enviar solicitud de desconexión
            sock.connect(self._server_dir)
            sock.sendall("DISCONNECT\0".encode())
            sock.sendall((self.ws_client.service.get_time() + "\0").encode())
            sock.sendall((user + "\0").encode())
            result_code = int.from_bytes(sock.recv(1), byteorder="big")
        except Exception as e:
            result_code = 3
        finally:
            sock.close()

        if result_code == 0:
            # Detener el hilo ServerThread después de recibir la respuesta del servidor
            if self._local_server_thread is not None:
                self._local_server_thread.close()  # Cerrar el socket (se deberia hacer implicitamente en kill pero por si acaso)
                self._local_server_thread.kill()  # Detener el hilo
                self._local_server_thread = None
                self._conected_user = None
            return "c> DISCONNECT OK"
        elif result_code == 1:
            return "c> DISCONNECT FAIL / USER DOES NOT EXIST"
        elif result_code == 2:
            return "c> DISCONNECT FAIL / USER NOT CONNECTED"
        elif result_code == 3:
            return "c> DISCONNECT FAIL"

    def publish(self, fileName, description):
        if self._conected_user is None:
            return "c> PUBLISH FAIL, USER NOT CONNECTED"

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result_code = 4
        try: # enviar solicitud de publicación
            sock.connect(self._server_dir)
            sock.sendall("PUBLISH\0".encode())
            sock.sendall((self.ws_client.service.get_time() + "\0").encode())
            sock.sendall((self._conected_user + "\0").encode())
            sock.sendall((fileName + "\0").encode())
            sock.sendall((description + "\0").encode())
            result_code = int.from_bytes(sock.recv(1), byteorder="big")
        except Exception as e:
            result_code = 4
        finally:
            sock.close()

        if result_code == 0:
            return "c> PUBLISH OK"
        elif result_code == 1:
            return "c> PUBLISH FAIL, USER DOES NOT EXIST"
        elif result_code == 2:
            return "c> PUBLISH FAIL, USER NOT CONNECTED"
        elif result_code == 3:
            return "c> PUBLISH FAIL, CONTENT ALREADY PUBLISHED"
        else:
            return "c> PUBLISH FAIL"

    def delete(self, fileName):
        if self._conected_user is None:
            return "c> USER NOT CONNECTED"

        if len(fileName) > 255 or len(fileName) == 0:
            return "c> FILE NAME NOT VALID"

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result_code = 4
        try: # enviar solicitud de eliminación
            sock.connect(self._server_dir)
            sock.sendall("DELETE\0".encode())
            sock.sendall((self.ws_client.service.get_time() + "\0").encode())
            sock.sendall((self._conected_user + "\0").encode())
            sock.sendall((fileName + "\0").encode())
            result_code = int.from_bytes(sock.recv(1), byteorder="big")
        except Exception as e:
            result_code = 4
        finally:
            sock.close()

        if result_code == 0:
            return "c> DELETE OK"
        elif result_code == 1:
            return "c> DELETE FAIL, USER DOES NOT EXIST"
        elif result_code == 2:
            return "c> DELETE FAIL, USER NOT CONNECTED"
        elif result_code == 3:
            return "c> DELETE FAIL, CONTENT NOT PUBLISHED"
        else:
            return "c> DELETE FAIL"

    def listusers(self):
        if self._conected_user is None:
            return "c> LIST_USERS FAIL, USER NOT CONNECTED"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result_code = 3
        try: # enviar solicitud de listado de usuarios
            sock.connect(self._server_dir)
            sock.sendall("LIST_USERS\0".encode())
            sock.sendall((self.ws_client.service.get_time() + "\0").encode())
            sock.sendall((self._conected_user + "\0").encode())
            result_code = int.from_bytes(sock.recv(1), byteorder="big")
        except Exception as e:
            result_code = 3
        finally:
            if result_code == 0:
                """
                Una cadena que codifica el n ́umero de usuarios cuya informaci ́on se va a enviar.
                Si se recibe la cadena ”5”, el servidor a continuaci ́on enviar ́a la informaci ́on aso-
                ciada a 5 clientes. Por cada cliente enviar ́a 3 cadenas de caracteres codificando
                el nombre del usuario, la direcci ́on IP y el puerto
                """
                clients = []
                data = recvUntilZero(sock).decode()
                num_users = int(data)

                for i in range(num_users):
                    user = recvUntilZero(sock).decode()
                    ip = recvUntilZero(sock).decode()
                    port = recvUntilZero(sock).decode()
                    clients.append((user, ip, port))

                str_val = "c> LIST_USERS OK\n"
                for c in clients:
                    str_val += "\t" + c[0] + " " + c[1] + " " + c[2] + "\n"

                sock.close()
                return str_val

        sock.close()
        if result_code == 1:
            return "c> LIST_USERS FAIL, USER DOES NOT EXIST"
        elif result_code == 2:
            return "c> LIST_USERS FAIL, USER NOT CONNECTED"
        elif result_code == 3:
            return "c> LIST_USERS FAIL"

    def listcontent(self, user):
        if self._conected_user is None:
            return "c> LIST_CONTENT FAIL, USER NOT CONNECTED"

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self._server_dir)
        result_code = 3
        try: # enviar solicitud de listado de contenido
            sock.sendall("LIST_CONTENT\0".encode())
            sock.sendall((self.ws_client.service.get_time() + "\0").encode())
            sock.sendall((self._conected_user + "\0").encode())
            sock.sendall((user + "\0").encode())
            result_code = int.from_bytes(sock.recv(1), byteorder="big")
        except Exception as e:
            result_code = 4
        finally:
            if result_code == 0:
                """
                Una cadena que codifica el n ́umero de ficheros publicados por el usuario. Si se
                recibe la cadena ”5”, el servidor a continuaci ́on enviar ́a la informaci ́on asociada a
                5 ficheros. Por cada fichero enviar ́a 2 cadenas de caracteres codificando el nom-
                bre del fichero y la descripci ́on
                """
                files = []
                data = recvUntilZero(sock).decode()
                num_files = int(data)

                for i in range(num_files):
                    file = recvUntilZero(sock).decode()
                    description = recvUntilZero(sock).decode()
                    files.append((file, description))

                str_val = "c> LIST_CONTENT OK\n"
                for f in files:
                    str_val += "\t" + f[0] + " " + f[1] + "\n"

                sock.close()
                return str_val

        sock.close()
        if result_code == 1:
            return "c> LIST_CONTENT FAIL, USER DOES NOT EXIST"
        elif result_code == 2:
            return "c> LIST_CONTENT FAIL, USER NOT CONNECTED"
        elif result_code == 3:
            return "c> LIST_CONTENT FAIL, REMOTE USER DOES NOT EXIST"
        else:
            return "c> LIST_CONTENT FAIL"

    def getfile(self, user, remote_FileName, local_FileName):
        if self._conected_user is None:
            return "c> USER NOT CONNECTED"

        result_code = 3
        # list users and searchg for the user
        response_data = self.listusers()
        if "LIST_USERS OK" in response_data:
            users = response_data.split("\n")
            user_found = False
            for u in users:
                # buscar el usuario en la lista
                if user in u:
                    result_code = 0
                    ip = u.split(" ")[1]
                    port = u.split(" ")[2]
                    user_found = True
                    break
            if not user_found:
                return "c> GET_FILE FAIL"  # remote client not found
        else:
            return "c> GET_FILE FAIL"  # error in list users

        # conectar con el otro cliente y solicitar el archivo
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result_code = 3
        try:
            sock.connect((ip, int(port)))
            sock.sendall("GET_FILE\0".encode())
            sock.sendall((remote_FileName + "\0").encode())
            result_code = int.from_bytes(sock.recv(1), byteorder="big")
        except Exception as e:
            return "c> GET_FILE FAIL"

        if result_code == 2:
            return "c> GET_FILE FAIL / FILE NOT EXIST"
        elif result_code >= 3:
            return "c> GET_FILE FAIL"

        # recive and save file until connection is closed
        with open(local_FileName, "wb") as f:
            while True:
                data = sock.recv(1)
                if not data:
                    break
                f.write(data)

        sock.close()
        return "c> GET_FILE OK"

    @staticmethod
    def help():
        print("REGISTER <userName>")
        print("UNREGISTER <userName>")
        print("CONNECT <userName>")
        print("PUBLISH <fileName> <description>")
        print("DELETE <fileName>")
        print("LIST_USERS")
        print("LIST_CONTENT <userName>")
        print("DISCONNECT <userName>")
        print("GET_FILE <userName> <remote_fileName> <local_fileName>")
        print("QUIT")

    def quit(self):
        try:
            self.disconnect(self._conected_user)
        except Exception as e:
            print("Caution! Error when disconecting: " + str(e))
        try:
            if self._local_server_thread is not None:
                self._local_server_thread.close()  # Cierra el socket
                self._local_server_thread.kill()  # Detiene el hilo
        except Exception as e:
            print("Caution! Error when closing thread: " + str(e))
        self.running = False

    # *
    # **
    # * @brief Command interpreter for the client. It calls the protocol functions.

    def shell(self):
        """Command interpreter for the client. It calls the protocol functions."""
        while self.running:
            try:
                command = input("c> ")
                line = command.split(" ")
                if len(line) > 0:

                    line[0] = line[0].upper()

                    if line[0] == "REGISTER":
                        if len(line) == 2:
                            print(self.register(line[1]))
                        else:
                            print("Syntax error. Usage: REGISTER <userName>")

                    elif line[0] == "UNREGISTER":
                        if len(line) == 2:
                            print(self.unregister(line[1]))
                        else:
                            print("Syntax error. Usage: UNREGISTER <userName>")

                    elif line[0] == "CONNECT":
                        if len(line) == 2:
                            print(self.connect(line[1]))
                        else:
                            print("Syntax error. Usage: CONNECT <userName>")

                    elif line[0] == "PUBLISH":
                        if len(line) >= 3:
                            #  Remove first two words
                            description = " ".join(line[2:])
                            print(self.publish(line[1], description))
                        else:
                            print(
                                "Syntax error. Usage: PUBLISH <fileName> <description>"
                            )

                    elif line[0] == "DELETE":
                        if len(line) == 2:
                            print(self.delete(line[1]))
                        else:
                            print("Syntax error. Usage: DELETE <fileName>")

                    elif line[0] == "LIST_USERS":
                        if len(line) == 1:
                            print(self.listusers())
                        else:
                            print("Syntax error. Use: LIST_USERS")

                    elif line[0] == "LIST_CONTENT":
                        if len(line) == 2:
                            print(self.listcontent(line[1]))
                        else:
                            print("Syntax error. Usage: LIST_CONTENT <userName>")

                    elif line[0] == "DISCONNECT":
                        if len(line) == 2:
                            print(self.disconnect(line[1]))
                        else:
                            print("Syntax error. Usage: DISCONNECT <userName>")

                    elif line[0] == "GET_FILE":
                        if len(line) == 4:
                            print(self.getfile(line[1], line[2], line[3]))
                        else:
                            print(
                                "Syntax error. Usage: GET_FILE <userName> <remote_fileName> <local_fileName>"
                            )

                    elif line[0] == "QUIT":
                        if len(line) == 1:
                            self.quit()
                        else:
                            print("Syntax error. Use: QUIT")
                    elif line[0] == "HELP":
                        self.help()

                    else:
                        print("Error: command " + line[0] + " not valid.")
            except Exception as e:
                print("Exception: " + str(e))

    # *
    # * @brief Prints program usage
    @staticmethod
    def usage():
        """prints program usage"""
        print("Usage: python3 client.py -s <server> -p <port>")

    # *
    # * @brief Parses program execution arguments

    def parseArguments(self, argv):
        """Parses program execution arguments"""
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", type=str, required=True, help="Server IP")
        parser.add_argument("-p", type=int, required=True, help="Server Port")
        args = parser.parse_args()

        if args.s is None:
            parser.error("Usage: python3 client.py -s <server> -p <port>")
            return False

        if (args.p < 1024) or (args.p > 65535):
            parser.error("Error: Port must be in the range 1024 <= port <= 65535")
            return False

        self._server = socket.gethostbyname(args.s)
        self._port = args.p
        self._server_dir = (self._server, self._port)

        return True

    # ******************** MAIN *********************

    def main(self, argv):
        if not self.parseArguments(argv):
            self.usage()
            return

        #  Write code here
        self.running = True
        self.shell()
        print("+++ FINISHED +++")

    def __del__(self):
        self.quit()


if __name__ == "__main__":

    def signal_handler(sig, frame):
        print("ctrl+c pressed, exiting...")
        localclient.quit()
        exit(0)

    localclient = client()
    # sigsev handler
    signal.signal(signal.SIGINT, signal_handler)
    localclient.main([])
