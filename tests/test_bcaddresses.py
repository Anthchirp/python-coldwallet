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

def test_b58_address_decoding():
  import coldwallet.bcaddresses
  for address, info in _test_addresses.items():
    assert coldwallet.bcaddresses.decode_base58_address(address) \
        == info['value']

