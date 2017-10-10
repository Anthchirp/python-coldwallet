from __future__ import absolute_import, division

import coldwallet.aes
import codecs
import os
import pytest

def test_encryption_function_validates_input():
  # Keys and data must be strings. Keys have 256 bits (32 bytes),
  # data must be a multiple of 128 bits (16 bytes).
  # IVs must be either None or a string of 128 bits (16 bytes).
  for invalid_data in (
        None, True, False, '', 'w'*31, 'z'*33
      ):
    if invalid_data != '':
      with pytest.raises(Exception, message='with data: %s' % repr(invalid_data)):
        coldwallet.aes.encrypt_block(invalid_data, 'x'*32)
    with pytest.raises(Exception, message='with key: %s' % repr(invalid_data)):
      coldwallet.aes.encrypt_block('x'*32, invalid_data)
  for invalid_iv in (
        True, False, '', 'w'*31, 'z'*33
      ):
    with pytest.raises(Exception, message='with IV: %s' % repr(invalid_iv)):
      coldwallet.aes.encrypt_block('x'*16, 'x'*32, iv=invalid_iv)

def test_encryption_function_uses_changing_ivs():
  data = os.urandom(32)
  key = os.urandom(32)
  variant1 = coldwallet.aes.encrypt_block(data, key)
  variant2 = coldwallet.aes.encrypt_block(data, key)
  assert variant1 != variant2, \
      "block: %s, key: %s" % (codecs.encode(data, 'hex_codec').decode('utf-8'), \
                              codecs.encode(key, 'hex_codec').decode('utf-8'))

def test_some_specific_AES_encryption_is_working():
  plaintext = b"0123456789abcdefghijklmnopqrstuv"
  key = b"the best keys have 32 characters"
  iv = b"the-best-iv-ever"
  expected_ciphertext = iv + \
      codecs.decode("0c364ed8785a280c870ce0734bc3942d5449aeee77df252d754fa02cfa64db19",
                    "hex_codec")

  ciphertext = coldwallet.aes.encrypt_block(plaintext, key, iv=iv)

  assert ciphertext[:16] == iv, 'Ciphertext does not contain IV'
  assert ciphertext == expected_ciphertext, 'AES encryption failure'

  decoded_plaintext = coldwallet.aes.decrypt_block(ciphertext, key)

  assert decoded_plaintext == plaintext, 'AES decryption failure'
