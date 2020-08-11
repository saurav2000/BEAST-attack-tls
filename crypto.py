from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = AES.block_size
AES_KEY = 'Uh280ch5295ycGDW'

class CryptoVictim:
  """
    Contains the helper methods
    i.e. encrypt which is used by
    the victim
  """
  @staticmethod
  def pad(msg, bs=BLOCK_SIZE):
    pad_l = bs - len(msg) % bs
    return msg + chr(97 + pad_l) * pad_l

  @staticmethod
  def encrypt(msg, iv=None):
    if not iv:
      iv = Random.new().read(BLOCK_SIZE)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    return cipher.encrypt(CryptoHelper.pad(msg))


class CryptoAttacker:
  """
    Contains the helper methods
    i.e. xor of blocks which is used by
    the attacker to guess the string
  """
  @staticmethod
  def block_xor(b1, b2, b3=None):
    s = ""
    for c1, c2 in zip(b1, b2):
      s += chr(ord(c1) ^ ord(c2))
    if b3:
      return CryptoHelper.block_xor(s, b3)
    else:
      return s
