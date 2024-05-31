import socket

def recvUntilZero(sock):
    """
    Receives data from the socket until a null byte (0) is encountered.

    Args:
        sock (socket.socket): The socket object to receive data from.

    Returns:
        bytes: The received data, excluding the null byte.

    """
    data = b''
    while True:
        data += sock.recv(1)
        if data[-1] == 0:
            break
    return data[:-1]


def handleConnection(conn: socket):
    """
    Handles the connection with a client.

    Parameters:
    conn (socket): The socket object representing the connection with the client.

    Returns:
    None
    """
    # recive function name
    funcName = recvUntilZero(conn).decode()
    if funcName == 'GET_FILE':
        # receive filename and send file
        filename = recvUntilZero(conn).decode()
        sendFile(conn, filename)
        
    conn.close()
    
        
def get_host_ip():
    """
    Get the IP address of the host machine.

    Returns:
        str: The IP address of the host machine.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
        

def sendFile(sock, filename):
    """
    Sends a file over a socket connection.

    Args:
        sock (socket.socket): The socket object used for the connection.
        filename (str): The path of the file to be sent.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        Exception: If an error occurs while sending the file.

    """
    try:
        with open(filename, "rb") as f:
            sock.send(b'\x01') # file exists
            data = f.read(1)
            while data:
                sock.send(data)
                data = f.read(1)
    except FileNotFoundError:
        print("File not found: ", filename)
        sock.send(b'\x02')
    except Exception as e:
        try:
            sock.send(b'\x03')
        except:
            pass
    finally:
        sock.close()
        