import socket
import time

def send_command(command):
    time.sleep(2)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ portFile = open('scripts/currentPort.txt', "r")
    port = portFile.readline(0)
    portFile.close() """

    client_socket.connect(('localhost', 51625))
    client_socket.send(command.encode('utf-8'))
    

# Example: Send a command to print the current scene name
send_command('bpy.ops.screen.screenshot(filepath="//C://Users//Wenz//Desktop//CreationBlockchain//media//Screenshots//output.png")')
