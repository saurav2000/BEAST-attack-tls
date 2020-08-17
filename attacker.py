import socket
from crypto import BLOCK_SIZE
from crypto import ALPHANUMERIC


class Attacker:
  def __init__(self):
    """
      Constructor with sockets
    """
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((socket.gethostname(), 4875))
    serversocket.listen(1)
    self.server_socket = serversocket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((socket.gethostname(), 4876))
    self.sock = sock

  def run(self):
    """
      Main running loop
    """
    print('Waiting for victim')
    clientsocket, addr = self.server_socket.accept()
    print('Victim accepted')
    cookie = ''
    for i in range(8):
      # Receiving the main request to keep track of the blue block and sending to bank 
      request_encoded = clientsocket.recv(112)
      self.sock.send(request_encoded)
      # The ciphertext block of the important part
      cookie_block = request_encoded[5*BLOCK_SIZE:6*BLOCK_SIZE]
      # Receving all the guesses
      for j in ALPHANUMERIC:
        guessed_request = clientsocket.recv(112)
        # Sending to bank without changing
        self.sock.send(guessed_request)
        print('The letter being guessed for position #', i+1, 'is', j)
        # Checking if the guess is correct by comparing the ciphertext blocks
        if cookie_block == guessed_request[BLOCK_SIZE:2*BLOCK_SIZE]:
          print('The guess is correct')
          cookie += j
        else:
          print('The guess is wrong')
        print('The cookie until now is', cookie, end="\n\n")
    clientsocket.close()
    self.server_socket.close()
    self.sock.close()
    print("\n\nI AM THE ATTACKER.\nTHE VICTIM'S COOKIE IS", cookie)


if __name__ == '__main__':
  Attacker().run()
