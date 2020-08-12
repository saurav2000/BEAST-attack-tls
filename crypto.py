from Crypto.Cipher import AES
from Crypto import Random
import string
import random

BLOCK_SIZE = AES.block_size
ALPHANUMERIC = string.digits + string.ascii_letters

class CryptoHelper:
  """
    Contains the helper methods
    i.e. encrypt which is used by
    the victim and a function to
    generate a cookie to see that it
    isn't hardcoded and xor of blocks
  """
  AES_KEY = 'Uh280ch5295ycGDW'

  @staticmethod
  def random_cookie(length):
    return ''.join((random.choice(ALPHANUMERIC) for i in range(length)))

  @staticmethod
  def pad(msg, bs=BLOCK_SIZE):
    pad_l = bs - len(msg) % bs
    if isinstance(msg, str):
      return msg + chr(97 + pad_l) * pad_l
    else:
      return msg + bytes(chr(97 + pad_l) * pad_l, "ascii")

  @staticmethod
  def encrypt(msg, iv=None):
    if not iv:
      iv = Random.new().read(BLOCK_SIZE)
    cipher = AES.new(CryptoHelper.AES_KEY, AES.MODE_CBC, iv)
    # print(raw, len(raw.encode()), sep="\n")
    return cipher.encrypt(CryptoHelper.pad(msg))

  @staticmethod
  def block_xor(b1, b2, b3):
    s = b''
    for c1, c2, c3 in zip(b1, b2, b3):
      # print(c1, c2, c3, c1^c2^c3)
      s += bytes([c1 ^ c2 ^ c3])
    # print(len(s.decode('cp437')), len(s))
    return s
