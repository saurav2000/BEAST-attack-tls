import socket
from crypto import CryptoHelper
from crypto import BLOCK_SIZE
from crypto import ALPHANUMERIC


class Victim:
  def __init__(self):
    """
      Constructor with sockets and parts of the request
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((socket.gethostname(), 4875))
    self.sock = sock
    self.byte_shifting_part = "POST /bogus/malicious_filler"
    self.request_part = " HTTP/1.1 \r\nHost:www.goodbank.com\r\nCookie: Session="
    self.cookie = CryptoHelper.random_cookie(8)
    print('I am the victim. My Cookie is', self.cookie, "\n")

  def request(self, step):
    """
      Construct the plain text after modifying it

      step: no of bytes to be shifted to guess the next letter
    """
    s = self.byte_shifting_part if step == 0 else self.byte_shifting_part[:-step]
    return s + self.request_part + self.cookie

  def block_print(self, string, pr=True):
    """
      Function to print the malicious requests in formatted blocks
    """
    string = CryptoHelper.pad(string)
    l = [string[i:i+BLOCK_SIZE] for i in range(0, len(string), BLOCK_SIZE)]
    l = [repr(s)[2:-1] if isinstance(s, bytes) else repr(s)[1:-1] for s in l]
    if pr:
      print('The malicious request is')
    print("{: <65} {: <20} {: <20} {: <20} {: <20} {: <20}".format(*l), end="\n\n")

  def modify(self, string, char, iv, prev_cipher):
    """
      Function to modify the plaintext of the request
      to the XOR of the 3 blocks (cyan, yellow and orange in the report)

      char: the character to which the last letter is changed to
      iv: the cyan block in the report
      prev_cipher: the yellow block in the report
      string: the plaintext request after shifting the bytes 
        but before modifying the 1st block
    """
    bs = BLOCK_SIZE
    # Change the last character
    guess = string[4*bs:5*bs][:-1] + char
    print('The guess is ', repr(guess))
    # Taking the xor of the 3 blocks
    b1 = CryptoHelper.block_xor(guess.encode(), iv, prev_cipher)
    return b1 + string[bs:].encode()

  def run(self):
    """
      Main running loop of the Victim
    """
    iv = None
    print('The primary request is', repr(self.request(0))[1:-1], end="\n\n")
    for i in range(8):
      request = self.request(i)
      print('The shifted request is')
      self.block_print(request, False)
      # This is the main request being sent to 
      encoded = CryptoHelper.encrypt(request, iv)
      iv = encoded[-BLOCK_SIZE:]
      prev_cipher = encoded[4*BLOCK_SIZE:5*BLOCK_SIZE]
      self.sock.send(encoded)
      # Loop to go through all the guesses and send each guess
      for j in ALPHANUMERIC:
        modified_req = self.modify(request, j, iv, prev_cipher)
        encoded = CryptoHelper.encrypt(modified_req, iv)
        self.block_print(modified_req)
        # Sending the encoded guess
        self.sock.send(encoded)
        iv = encoded[-BLOCK_SIZE:]
      print("\n\n")
    print('I AM THE VICTIM.\nMY COOKIE IS', self.cookie)
    self.sock.close()


if __name__ == '__main__':
  Victim().run()
