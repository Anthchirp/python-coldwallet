from __future__ import absolute_import, division

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
