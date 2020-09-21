import socket
from threading import Thread
import os

clients = []


# Thread to listen one particular client
class ClientListener(Thread):
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name

    # clean up
    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')

    def run(self):
        # Receive file name
        file_name = self.sock.recv(1024).decode()
        # Check that file with the sam ename alreasy exists
        if os.path.exists(file_name):
            extension = file_name[file_name.rfind('.') + 1:]
            n = 1
            new_name = file_name[:file_name.rfind('.')] + ' (' + str(n) + ')'
            # Find free name
            while os.path.exists(new_name + '.' + extension):
                new_name = new_name[ : -(len(str(n)) + 1)]
                n = n + 1 
                new_name += str(n) + ')'
            # Rename file
            file_name = new_name + '.' + extension
            print('Upload a file:', file_name)
            
        # Copy content of the file
        file = open(file_name, 'wb')
        # Receive file
        new_data = self.sock.recv(1024)
        while (new_data):
            file.write(new_data)
            new_data = self.sock.recv(1024)
        print('File is uploaded. Closing file')
        # Close file
        file.close()
        # Disconnected from server
        self._close()

def main():
    next_name = 1

    # AF_INET – IPv4, SOCK_STREAM – TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # reuse address; in OS address will be reserved after app closed for a while
    # so if we close and imidiatly start server again – we'll get error
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # listen to all interfaces at 8800 port
    sock.bind(('', 8800))
    sock.listen()
    while True:
        # blocking call, waiting for new client to connect
        con, addr = sock.accept()
        clients.append(con)
        name = 'u' + str(next_name)
        next_name += 1
        print(str(addr) + ' connected as ' + name)
        # start new thread to deal with client
        ClientListener(name, con).start()


if __name__ == "__main__":
    main()
