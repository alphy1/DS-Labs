import socket
import sys
import os.path

file_name = str(sys.argv[1])
address = str(sys.argv[2])
port = int(sys.argv[3])

print('Start working on', file_name, address, port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((address, port))

s.send(file_name.encode())
file = open(file_name, 'rb')

file_size = os.path.getsize(file_name)
data = file.read(1024)
t = 1024
print(s.recv(1024).decode())

while data:
    print('Sent: {}%'.format(t * 100 // file_size))
    t += 1024
    s.send(data)
    data = file.read(1024)
file.close()
print('End')
s.close()
