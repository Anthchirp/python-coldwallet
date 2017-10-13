# Coldwallet encryption related functions. This is the heart of coldwallet.

from __future__ import absolute_import, division

import math
import os

def disable_randomness():
  '''Make the random number generator produce deterministic (ie. non-random)
     output. This is used for internal testing only, and must never be used
     otherwise! A warning is printed.
  '''
  import random
  import sys
  sys.stderr.write('\n-- coldwallet running in test mode - random number generation disabled --\n\n')
  def fakerandom(b):
    return "".join(chr(random.randrange(256)) for x in range(b))
  random.seed(0)
  os.urandom = fakerandom

def generate_random_string(bits):
  '''Generate a random string with a given number of bits. If the number of bits is
     not divisible by 8 then pad with 0s.
  '''
  assert bits >= 1, "Cannot create 0 bit random strings"

  stringbytes = int(math.ceil(bits / 8))
  rand_string = os.urandom(stringbytes)

  zero_padding = stringbytes * 8 - bits
  if zero_padding:
    mask = 0x100 - (2 ** zero_padding)
    rand_string = rand_string[:-1] + chr(ord(rand_string[-1]) & mask)

  return rand_string
