# bitcoin address related functions:
# generating private keys, generating and verifying addresses

from __future__ import absolute_import, division

import codecs
import ecdsa
import hashlib
import struct

import coldwallet.encoding

class Network():
  BITCOIN = { 'private': 128, 'public': 0 }
  BITCOINTESTNET = { 'private': 239, 'public': 111 }

def base58CheckEncode(version, payload):
  '''A common encoding function for bitcoin addresses. The address includes a
     version field, a 4 byte SHA256 checksum, a compression scheme and is
     encoded in base 58.
     The payload is a byte string of arbitrary length.
     For more details see https://en.bitcoin.it/wiki/Base58Check_encoding
  '''
  # Prefix 1 byte version field
  versioned_payload = bytearray((version,)) + payload

  # Create and append 4 checksum bytes
  checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[0:4]
  checked_payload = versioned_payload + checksum

  # Count leading chr(0) bytes
  leadingZeros = len(checked_payload) - len(checked_payload.lstrip(bytearray((0,))))

  # base58 encode string, leading chr(0) bytes are dropped
  b58 = coldwallet.encoding.base58_encode(
          int(codecs.encode(checked_payload, 'hex_codec'), 16)
        )

  # Add leading '1' for every dropped chr(0) byte
  return ('1' * leadingZeros) + b58

def generate_private_key(exponent, version=Network.BITCOIN):
  '''Generate a private Bitcoin key from a secret exponent. The exponent
     is given as a 256 bit (32 byte) string. The key is returned in
     human-typable form.
     Different version fields can be specified to generate addresses on
     various bitcoin networks. The default is the BTC Bitcoin network.
  '''
  return base58CheckEncode(version['private'], exponent)

def generate_public_address(exponent, version=Network.BITCOIN):
  '''Generate the public Bitcoin address relating to a private key in the form
     of a secret exponent. The address is returned in human-typable form.
     Different version fields can be specified to generate addresses on
     various bitcoin networks. The default is the BTC Bitcoin network.
  '''

  assert exponent, 'No private key specified'

  # generate ECDSA public key (65 bytes, 1 byte 0x04,
  # 32 bytes corresponding to X coordinate, 32 bytes corresponding to Y coordinate)
  sk = ecdsa.SigningKey.from_string(exponent, curve=ecdsa.SECP256k1)
  ecdsapubkey = b'\04' + sk.verifying_key.to_string()

  # Apply RIPEMD160(SHA256( public key ))
  ripemd160 = hashlib.new('ripemd160')
  ripemd160.update(hashlib.sha256(ecdsapubkey).digest())

  # Encode result with network version as base58 string
  return base58CheckEncode(version['public'], ripemd160.digest())
