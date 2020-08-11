import socket
from crypto import CryptoVictim

class Victim:
  def __init__():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((socket.gethostname(), 4875))
    self.sock = sock

  def run():
    pass

if __name__ == '__main__':
  victim = Victim.new()
  victim.run()

