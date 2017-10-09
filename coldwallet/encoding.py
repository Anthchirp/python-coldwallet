# helper functions for shuffling bits around various formats

from __future__ import absolute_import, division

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58index = { k: n for n, k in enumerate(__b58chars) }
__b58base = len(__b58chars)

def base58_decode(b58):
  '''Take a base58 encoded string and return the represented value as an integer.'''
  value = 0
  for c in b58:
    value = value * 58 + __b58index[c]
  return value

def base58_encode(value):
  '''Take an integer and return the shortest base58 encoded string representation.'''
  b58 = ''
  while value > 0:
    b58 = __b58chars[value % 58] + b58
    value = value // 58
  return b58
