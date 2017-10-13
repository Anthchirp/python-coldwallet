from __future__ import absolute_import, division

import random

import mock

_test_addresses = {
  '1111111111111111111111111111111111': {
      'value': 0,
  },
  '1111111112': {
      'value': 1,
  },
  '11111111121': {
      'value': 58,
  },

  '1111111111111111111114oLvT2': {
      'value': 2493516049,
  },
}

def test_base58_decoding():
  from coldwallet.encoding import base58_decode
  for address, info in _test_addresses.items():
    assert info['value'] == base58_decode(address)

def test_base58_encoding():
  from coldwallet.encoding import base58_encode
  for address, info in _test_addresses.items():
    assert address.lstrip('1') == base58_encode(info['value'])

def test_block7_encoding():
  from coldwallet.encoding import block7_encode
  assert block7_encode(0) == '111111N'

  maxvalue = 2 ** 36 - 1 # 68719476735
  assert block7_encode(maxvalue) == 'zmM9z3t'

def test_block7_decoding():
  from coldwallet.encoding import block7_decode
  assert block7_decode('1111111') == { 'value': 0, 'valid': False }
  assert block7_decode('111111M') == { 'value': 0, 'valid': False }
  assert block7_decode('111111N') == { 'value': 0, 'valid': True }
  assert block7_decode('111111P') == { 'value': 0, 'valid': False }
  assert block7_decode('111111o') == { 'value': 1, 'valid': False }

  # Checksum should detect most - 31 out of 32 - typos:
  assert block7_decode('X11111N') == { 'value': mock.ANY, 'valid': False }
  assert block7_decode('1X1111N') == { 'value': mock.ANY, 'valid': False }
# assert block7_decode('11X111N') == { 'value': mock.ANY, 'valid': True } # undetected typo
  assert block7_decode('111X11N') == { 'value': mock.ANY, 'valid': False }
  assert block7_decode('1111X1N') == { 'value': mock.ANY, 'valid': False }
  assert block7_decode('11111XN') == { 'value': mock.ANY, 'valid': False }
  assert block7_decode('111111X') == { 'value': mock.ANY, 'valid': False }

  assert block7_decode('zmM9z3s') == { 'value': 2**36-1, 'valid': False }
  assert block7_decode('zmM9z3t') == { 'value': 2**36-1, 'valid': True }
  assert block7_decode('zmM9z3u') == { 'value': 2**36-1, 'valid': False }

  assert block7_decode('XmM9z3t') == { 'value': mock.ANY, 'valid': False }
# assert block7_decode('zXM9z3t') == { 'value': mock.ANY, 'valid': True } # undetected typo
  assert block7_decode('zmX9z3t') == { 'value': mock.ANY, 'valid': False }
  assert block7_decode('zmMXz3t') == { 'value': mock.ANY, 'valid': False }
# assert block7_decode('zmM9X3t') == { 'value': mock.ANY, 'valid': True } # undetected typo
  assert block7_decode('zmM9zXt') == { 'value': mock.ANY, 'valid': False }
  assert block7_decode('zmM9z3X') == { 'value': mock.ANY, 'valid': False }

def test_block7_encoding_roundtrip():
  from coldwallet.encoding import block7_decode, block7_encode
  for test in range(100):
    number = random.randrange(2 ** 36)
    retval = block7_decode(block7_encode(number))
    assert retval['value'] == number, 'value %d was altered to %d in block7 encoding!' % (number, retval['value'])
    assert retval['valid'], 'value %d could not be decoded successfully' % number

def test_splitting_data_into_block7s():
  from coldwallet.encoding import block7_split, block7_decode
  doubledata = b"\x14\x23\x99\xc1\xff\x1d\x31\x0a\x8b" # 9 bytes = 72 bit = 2x36 bit
  block7s = block7_split(doubledata)
  assert len(block7s) == 2
  assert block7_decode(block7s[0]) == { 'value': 0x142399c1f, 'valid': True }
  assert block7_decode(block7s[1]) == { 'value': 0xf1d310a8b, 'valid': True }

def test_merging_data_into_block7s():
  from coldwallet.encoding import block7_merge
  block7s = ['5YZpdK6', 'wZq33nn']
  assert block7_merge(block7s) == { 'key': b"\x14\x23\x99\xc1\xff\x1d\x31\x0a\x8b",
                                    'valid': True }

def test_crc8_returns_correct_values():
  from coldwallet.encoding import crc8
  assert crc8('1234567') == '9f'
  assert crc8('1234568') == '0e'
  assert crc8('1azZza1') == '95'
