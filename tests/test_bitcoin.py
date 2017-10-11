from __future__ import absolute_import, division

import codecs

import coldwallet.bitcoin
import pytest

# The exponents of the following keys are guaranteed to be secret.
# Best not to use them though :)

keys = [
  { 'secret_exponent': "d8c26b428267c84d7a95e88148c19e40e8fbcfe64fbae6af78196f9ce9f77add",
    'private_key':     "5KTkQmuGTbNubzuNKBbLvnV2kFDtdXMm23nGWXfANyKahhcY5xS",
    'public_address':  "1DR2Dp74CqtqXhU9MznV2r4qTuZBGYagP",
  },

  { 'secret_exponent': "48418fc9489d531a651389fc057b38f46c98636f1548d973b748cea1fd533c40",
    'private_key':     "5JN7GR8v2X3woWexcGgY1HCkyDm6QrGMGugaSugxWPUJA9hBXq7",
    'public_address':  "113geRau4zNQFpRJxEJf1J9cQsXkXGUHrN",
  },

  { 'secret_exponent': "0000000000000000000000000000000000000000000000000000000000000001",
    'private_key':     "5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf",
    'public_address':  "1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm",
  },

  { 'secret_exponent': "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140",
    'private_key':     "5Km2kuu7vtFDPpxywn4u3NLpbr5jKpTB3jsuDU2KYEqetqj84qw",
    'public_address':  "1JPbzbsAx1HyaDQoLMapWGoqf9pD5uha5m",
  },
]

for key in keys:
  key['raw_exponent'] = codecs.decode(key['secret_exponent'], "hex_codec")

def test_create_bitcoin_address_from_secret_exponent():
  for key in keys:
    assert key['public_address'] == \
           coldwallet.bitcoin.generate_public_address(key['secret_exponent'])
    assert key['public_address'] == \
           coldwallet.bitcoin.generate_public_address(key['raw_exponent'])

def test_create_private_key_from_secret_exponent():
  for key in keys:
    assert key['private_key'] == \
           coldwallet.bitcoin.generate_private_key(key['secret_exponent'])
    assert key['private_key'] == \
           coldwallet.bitcoin.generate_private_key(key['raw_exponent'])

def test_create_secret_exponent_from_private_key():
  for key in keys:
    pack = coldwallet.bitcoin.unpack_private_key(key['private_key'])

    assert pack['secret_exponent'] == key['raw_exponent']
    assert pack['valid_checksum'], "Checksum error unpacking %s" % key['private_key']
    assert pack['version'] == coldwallet.bitcoin.Network.BITCOIN['private'], \
           "Version error unpacking %s" % key['private_key']

def test_that_we_do_not_generate_invalid_keys():
  # This exponent is smaller than the minimum allowed exponent (1)
  secret_exponent = "0000000000000000000000000000000000000000000000000000000000000000"
  private_key = coldwallet.bitcoin.generate_private_key(secret_exponent)
  assert "5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAbuatmU" == private_key
  with pytest.raises(Exception):
    public_address = coldwallet.bitcoin.generate_public_address(secret_exponent)

  # This exponent is larger than the maximum allowed exponent (this number - 1)
  secret_exponent = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141"
  private_key = coldwallet.bitcoin.generate_private_key(secret_exponent)
  assert "5Km2kuu7vtFDPpxywn4u3NLpbr5jKpTB3jsuDU2KYEqetwr388P" == private_key
  with pytest.raises(Exception):
    public_address = coldwallet.bitcoin.generate_public_address(secret_exponent)

  # This exponent is much larger than the maximum allowed exponent
  secret_exponent = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
  private_key = coldwallet.bitcoin.generate_private_key(secret_exponent)
  assert "5Km2kuu7vtFDPpxywn4u3NLu8iSdrqhxWT8tUKjeEXs2f9yxoWz" == private_key
  with pytest.raises(Exception):
    public_address = coldwallet.bitcoin.generate_public_address(secret_exponent)
