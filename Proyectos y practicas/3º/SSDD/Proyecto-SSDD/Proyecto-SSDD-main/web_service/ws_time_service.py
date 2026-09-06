import logging
from datetime import datetime
from wsgiref.simple_server import make_server
from spyne import Application, ServiceBase, Integer, Unicode, rpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import socket

def get_host_ip():
    '''
    extract the ip address of the host, needed for the server to listen on 
    the correct ip address when running on a network.
    '''
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
class TimeService(ServiceBase):
    @rpc(_returns=Unicode)
    def get_time(ctx):
        return datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
application = Application(
    services=[TimeService],
    tns='http://tests.python-zeep.org/', # CHECK THIS 
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

application = WsgiApplication(application)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
    ip = get_host_ip()
    server = make_server(ip, 8000, application)
    logging.info(f"listening to http://{server.server_address[0]}:{server.server_address[1]}; wsdl is at: http://{server.server_address[0]}:{server.server_address[1]}/?wsdl")
    server.serve_forever()



