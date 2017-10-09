# helper functions relating to bitcoin addresses

from __future__ import absolute_import, division

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58index = { k: n for n, k in enumerate(__b58chars) }

def decode_base58_address(b58):
  '''Takes a base58 encoded address and returns the address represented as an integer.'''
  n = 0
  for c in b58:
    n = n * 58 + __b58index[c]
  return n

