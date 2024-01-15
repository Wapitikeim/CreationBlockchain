import bpy
import socket

def execute_command(command):
    try:
        exec(command)
    except Exception as e:
        print(f"Error executing command: {e}")

def handle_connection(server_socket):
    try:
        client_socket, _ = server_socket.accept()
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received command: {data}")
        execute_command(data)
        client_socket.close()
    except socket.error as e:
        pass  # No incoming connection, ignore the error

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 0))
    _, port = server_socket.getsockname()

    currentPortWriter = open('C:/Users/Wenz/Desktop/CreationBlockchain/scripts/currentPort.txt', "w")
    currentPortWriter.write(str(port))
    currentPortWriter.close()

    server_socket.listen(1)
    print(f"Server listening on port {port}")
    server_socket.setblocking(False)
    return server_socket

def check_for_commands(dummy):
    handle_connection(server_socket)

# Start the server on the selected port
server_socket = start_server()

# Register the check_for_commands function to run every frame
bpy.app.handlers.frame_change_pre.append(check_for_commands)
