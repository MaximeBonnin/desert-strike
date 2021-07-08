

# make this a client file.

import socket
from typing import ByteString

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5555        # The port used by the server

test = [1, 2, 3, 4]
test_str = str(test)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Client trying to connect.")
    s.connect((HOST, PORT))
    s.sendall(test_str.encode())
    data = s.recv(1024)

list2 = data.decode()

print('Received', eval(list2))

