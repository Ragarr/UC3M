import os
import subprocess
import signal
import argparse
import time
# argumentos --build, --clean y --run (-b, -c, -r) o (-bcr)


server_process, logger_process, ws_time_service_process = None, None, None
server_out, logger_out, ws_time_service_out = None, None, None

def build():
    os.chdir('rpc_service')
    subprocess.run(['make'])
    subprocess.run(['cp', 'liblogger.so', '../server'])
    os.chdir('../server')
    subprocess.run(['make'])
    os.chdir('../web_service')
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
    os.chdir('../client')
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
    os.chdir('..') # end in the same folder where it started
    print('Build done.\n\n')

def clean():
    os.chdir('rpc_service')
    subprocess.run(['make', 'clean'])
    os.chdir('../server')
    subprocess.run(['make', 'clean'])
    os.chdir('..') # end in the same folder where it started
    # remove de .out files
    if os.path.exists('logger.out'):
        os.remove('logger.out')
    if os.path.exists('server.out'):
        os.remove('server.out')
    if os.path.exists('ws_time_service.out'):
        os.remove('ws_time_service.out')
    # remove all files ened in .log (even in subdirectories)
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.log'):
                os.remove(os.path.join(root, file))

    # eliminar los __pycache__ de todos los subdirectorios
    for root, dirs, files in os.walk('.'):
        for dir in dirs:
            if dir == '__pycache__':
                os.system('rm -r ' + os.path.join(root, dir))
                
    print('Clean done.')
    
def run():
    # create server.out, logger.out and ws_time_service.out files to redirect output 
    try:    
        import regex as re # type: ignore
    except ImportError:
        subprocess.run(['pip', 'install', 'regex'])
        import regex as re # type: ignore
        
    # set the env variables
    os.environ['LD_LIBRARY_PATH'] = os.getcwd() + '/server'
    os.environ['LOGGER_HOST'] = 'localhost'
     
    # run the processes
    global server_process, logger_process, ws_time_service_process
    logger_process = subprocess.Popen(['./rpc_service/rpc_logger_server'])
    
    
    
    
    server_process = subprocess.Popen(['./server/server', '-p', '9090'],  stdout=open('server.out', 'w'), stderr=subprocess.STDOUT )
    ws_time_service_process = subprocess.Popen(['python3', 'web_service/ws_time_service.py'], stdout=open('ws_time_service.out', 'w'), stderr=subprocess.STDOUT)
    print("\n\n")
    print('Server, logger and web service running.')
    print('Server PID:', server_process.pid)
    print('Logger PID:', logger_process.pid)
    print('Web service PID:', ws_time_service_process.pid)
    print("\n")
    
    # wait for the server to start (until there is some output in the server.out file)
    timeout = 10
    while timeout > 0:
        with open('server.out', 'r') as f:
            server_out = f.read()
            # if there is any output in the server.out file, break the loop
            if len(server_out) > 0:
                break            
        time.sleep(0.5)
        timeout -= 0.5
    
    if timeout == 0:
        print('Server did not start. This may cause errors, try to run the server manually.')
    
    time.sleep(0.5)
    
    # obtain the ip and port of the server
    with open('server.out', 'r') as f:
        server_out = f.read()
        ip_port = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})', server_out)
        
        if ip_port is not None:
            ip = ip_port.group(1).split(':')[0]
            port = ip_port.group(1).split(':')[1]                    
            print('Server IP:', ip)
            print('Server Port:', port)
            
    # wait for the web service to start (until there is some output in the ws_time_service.out file)
    timeout = 10
    while timeout > 0:
        with open('ws_time_service.out', 'r') as f:
            ws_time_service_out = f.read()
            # if there is any output in the ws_time_service.out file, break the loop
            if len(ws_time_service_out) > 0:
                break            
        time.sleep(0.5)
        timeout -= 0.5
    if timeout == 0:
        print('Web service did not start. This may cause errors, try to run the web service manually.')
    time.sleep(0.5)
    
    
    # obtain the url of the web service
    with open('ws_time_service.out', 'r') as f:
        # INFO:root:listening to http://127.0.0.1:8000;  wsdl is at: http://localhost:8000/?wsdl
        ws_time_service_out = f.read()
        url = re.search(r'http://(\d+\.\d+\.\d+\.\d+):\d+', ws_time_service_out)
        if url is not None:
            url = url.group(0)
            print('Web service URL:', url)
            print("Web service WSDL URL:", url + '/?wsdl')
            os.environ['WSDL_URL'] = url + '/?wsdl'
        else:
            print('Web service URL not found. Set it manually.')
            os.environ['WSDL_URL'] = ''
            
    print("Para ejecutar el cliente establece la variable de entorno 'WSDL_URL a '", str(url) + '/?wsdl' + "'")
    
    print('Press Ctrl+C to stop the processes.')
    print("\n\n")
    print('Server output will be shown in server.out file.')
    print('Web service output will be shown in ws_time_service.out file.')
    print('Logger output will be shown in this terminal.\n')
    
    
    
    # wait until ctrl+c is pressed
    while True:
        time.sleep(1)
    
    
def stop(signum, frame):
    global server_process, logger_process, ws_time_service_process
    print('Stopping server, logger and web service...')
    if server_process:
        server_process.send_signal(signal.SIGINT)
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.send_signal(signal.SIGKILL)
            server_process.wait()        
        print('Server stopped.')
    if logger_process:
        logger_process.send_signal(signal.SIGINT)
        try:
            logger_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            logger_process.send_signal(signal.SIGKILL)
            logger_process.wait()
        print('Logger stopped.')
        
    if ws_time_service_process:
        ws_time_service_process.send_signal(signal.SIGINT)
        try:
            ws_time_service_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            ws_time_service_process.send_signal(signal.SIGKILL)
            ws_time_service_process.wait()
            
        print('Web service stopped.')
    
        
    print('All services stopped.')
    exit()

if __name__ == '__main__':
    
    signal.signal(signal.SIGINT, stop)

    parser = argparse.ArgumentParser(description='Build, clean and run the project.')
    parser.add_argument('-b', '--build', action='store_true', help='Build the project.')
    parser.add_argument('-c', '--clean', action='store_true', help='Clean the project.')
    parser.add_argument('-r', '--run', action='store_true', help='Run the project.')
    args = parser.parse_args()


    if args.clean:
        print('Cleaning the project...')
        clean()
    if args.build:
        print('Building the project...')
        build()
    if args.run:
        print('Running the project...')
        run()
    if not args.build and not args.clean and not args.run:
        parser.print_help()
