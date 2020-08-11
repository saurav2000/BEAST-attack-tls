import socket
from crypto import CryptoAttacker

class Attacker:
  def __init__():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), 4875))
    self.server_socker = serversocket

  def run():
    clientsocket,addr = serversocket.accept()


if __name__ == '__main__':
  attacker = Attacker.new()
  attacker.run()
