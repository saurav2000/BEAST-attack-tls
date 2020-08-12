import socket
from crypto import CryptoHelper
from crypto import BLOCK_SIZE
from crypto import ALPHANUMERIC

class Victim:
  def __init__(self):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((socket.gethostname(), 4875))
    self.sock = sock
    self.controllable = "POST /bogus/malicious_filler"
    self.request_str = " HTTP/1.1 \r\nHost:www.goodbank.com\r\nCookie: Session="
    self.cookie = CryptoHelper.random_cookie(8)
    print('I am the victim. My Cookie is', self.cookie)

  def request(self, step):
    s = self.controllable if step == 0 else self.controllable[:-step]
    return s + self.request_str + self.cookie

  def modify(self, string, char, iv, prev_cipher):
    bs = BLOCK_SIZE
    guess = string[4*bs:5*bs][:-1] + char
    b1 = CryptoHelper.block_xor(guess.encode(), iv, prev_cipher)
    # print(len(b1), len(string[bs:]))
    return b1 + string[bs:].encode()

  def run(self):
    iv = None
    for i in range(8):
      request = self.request(i)
      # print(request, end="\n\n")
      encoded = CryptoHelper.encrypt(request, iv)
      iv = encoded[-BLOCK_SIZE:]
      prev_cipher = encoded[3*BLOCK_SIZE:4*BLOCK_SIZE]
      self.sock.send(encoded)
      for j in ALPHANUMERIC:
        modified_req = self.modify(request, j, iv, prev_cipher)
        # print(modified_req, end="\n\n")
        encoded = CryptoHelper.encrypt(modified_req, iv)
        self.sock.send(encoded)
        iv = encoded[-BLOCK_SIZE:]
    self.sock.close()

if __name__ == '__main__':
  victim = Victim()
  victim.run()
