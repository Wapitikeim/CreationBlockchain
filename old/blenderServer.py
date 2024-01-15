""" import bpy
import socket
import asyncio

def execute_command(command):
    try:
        exec(command)
    except Exception as e:
        print(f"Error executing command: {e}")

def is_port_open(port):
    # Check if the specified port is open
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0

def find_free_port(start_port, max_attempts=10):
    # Find an available port starting from the specified port
    for port in range(start_port, start_port + max_attempts):
        if is_port_open(port):
            currentPortWriter = open('C:/Users/Wenz/Desktop/CreationBlockchain/scripts/currentPort.txt', "w")
            currentPortWriter.write(str(port))
            currentPortWriter.close()
            return port
    raise RuntimeError(f"Unable to find an available port in the range {start_port}-{start_port + max_attempts - 1}")

async def handle_connection(client_socket):
    data = (await loop.sock_recv(client_socket, 1024)).decode('utf-8')
    print(f"Received command: {data}")
    execute_command(data)
    client_socket.close()

async def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)
    print(f"Server listening on port {port}")

    server_socket.setblocking(False)
    while True:
        client_socket, _ = await loop.sock_accept(server_socket)
        loop.create_task(handle_connection(client_socket))



# Specify the initial port and maximum attempts to find a free port
initial_port = 12345
max_attempts = 10

# Find an available port
selected_port = find_free_port(initial_port, max_attempts)

# Start the server on the selected port
loop = asyncio.get_event_loop()
loop.create_task(start_server(selected_port))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.close() """




import bpy
import socket
import threading

def is_port_open(port):
    # Check if the specified port is open
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

def port_check(port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.settimeout(2) #Timeout in case of port not open
   try:
      s.connect(('localhost', port)) #Port ,Here 22 is port 
      return True
   except:
      return False

def find_open_port():
    """
    Use socket's built in ability to find an open port.
    """
    sock = socket.socket()
    sock.bind(('', 0))

    _, port = sock.getsockname()

    currentPortWriter = open('C:/Users/Wenz/Desktop/CreationBlockchain/scripts/currentPort.txt', "w")
    currentPortWriter.write(str(port))
    currentPortWriter.close()

    return sock


def find_free_port(start_port, max_attempts):
    # Find an available port starting from the specified port
    for port in range(start_port, start_port + max_attempts):
        if port_check(port):
            currentPortWriter = open('C:/Users/Wenz/Desktop/CreationBlockchain/scripts/currentPort.txt', "w")
            currentPortWriter.write(str(port))
            currentPortWriter.close()
            return port
    raise RuntimeError(f"Unable to find an available port in the range {start_port}-{start_port + max_attempts - 1}")

def execute_command(command):
    try:
        exec(command)
    except Exception as e:
        print(f"Error executing command: {e}")

def handle_connection(client_socket):
    data = client_socket.recv(1024).decode('utf-8')
    print(f"Received command: {data}")
    execute_command(data)
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 0))

    _, port = server_socket.getsockname()

    currentPortWriter = open('C:/Users/Wenz/Desktop/CreationBlockchain/scripts/currentPort.txt', "w")
    currentPortWriter.write(str(port))
    currentPortWriter.close()

    #server_socket.bind(('localhost', port))
    server_socket.listen(1)
    print(f"Server listening on port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_connection, args=(client_socket))
        client_handler.start()

# Specify the initial port and maximum attempts to find a free port
initial_port = 12345
max_attempts = 10

try:
    # Find an available port
    # Start the server on the selected port
    start_server()

except RuntimeError as e:
    print(f"Error: {e}")
