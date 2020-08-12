import socket
from crypto import BLOCK_SIZE
from crypto import ALPHANUMERIC

class Attacker:
  def __init__(self):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((socket.gethostname(), 4875))
    serversocket.listen(1)
    self.server_socket = serversocket

  def run(self):
    print('Waiting for victim')
    clientsocket, addr = self.server_socket.accept()
    print('Victim accepted')
    cookie = ''
    for i in range(8):
      request_encoded = clientsocket.recv(96)
      cookie_block = request_encoded[4*BLOCK_SIZE:5*BLOCK_SIZE]
      for j in ALPHANUMERIC:
        changed_request = clientsocket.recv(96)
        if cookie_block == changed_request[:BLOCK_SIZE]:
          # print('This letter is ', j)
          cookie += j
    clientsocket.close()
    self.server_socket.close()
    print("The victim's cookie is", cookie)

if __name__ == '__main__':
  attacker = Attacker()
  attacker.run()
