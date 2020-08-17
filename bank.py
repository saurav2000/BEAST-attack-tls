import socket
from crypto import CryptoHelper
from crypto import ALPHANUMERIC


class Bank:
  def __init__(self):
    """
      Constructor with sockets
    """
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((socket.gethostname(), 4876))
    serversocket.listen(1)
    self.server_socket = serversocket

  def run(self):
    """
      Main running loop
    """
    clientsocket, addr = self.server_socket.accept()
    for i in range(8):
      # Receiving and decrypting the requests
      request_encoded = clientsocket.recv(112)
      request_decoded = CryptoHelper.decrypt(request_encoded)
      # Printing 404 error
      print('Decoded Request:\n', repr(request_decoded)[2:-1], sep="")
      print('ERROR 404', repr(request_decoded[6:28-i])[2:-1], 'NOT FOUND\n')
      for j in ALPHANUMERIC:
        # Receiving and decrypting the requests
        request_encoded = clientsocket.recv(112)
        request_decoded = CryptoHelper.decrypt(request_encoded)
        # Printing Invalid requests
        print('Decoded Request:\n', repr(request_decoded)[2:-1], sep="")
        print('Invalid HTTP request\n')
      print('\n\n')
    clientsocket.close()
    self.server_socket.close()


if __name__ == '__main__':
  Bank().run()
