from __future__ import absolute_import, division

import codecs

import coldwallet.bitcoin

# These exponents are guaranteed to be secret:
secret_exponents = [ codecs.decode(exponent, "hex_codec") for exponent in (
    "d8c26b428267c84d7a95e88148c19e40e8fbcfe64fbae6af78196f9ce9f77add",
    "48418fc9489d531a651389fc057b38f46c98636f1548d973b748cea1fd533c40",
  ) ]

# Best not use this Bitcoin address though :)
private_keys = [
    "5KTkQmuGTbNubzuNKBbLvnV2kFDtdXMm23nGWXfANyKahhcY5xS",
    "5JN7GR8v2X3woWexcGgY1HCkyDm6QrGMGugaSugxWPUJA9hBXq7",
  ]
public_addresses = [
    "1DR2Dp74CqtqXhU9MznV2r4qTuZBGYagP",
    "113geRau4zNQFpRJxEJf1J9cQsXkXGUHrN",
  ]

def test_create_bitcoin_address_from_secret_exponent():
  for exponent, key, address in zip(secret_exponents, private_keys, public_addresses):
    assert key == coldwallet.bitcoin.generate_private_key(exponent)
    assert address == coldwallet.bitcoin.generate_public_address(exponent)
