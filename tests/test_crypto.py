from __future__ import absolute_import, division

def test_disabling_random_number_generation_must_cause_a_warning_to_be_printed(capsys):
  import coldwallet.crypto

  coldwallet.crypto.disable_randomness()

  out, err = capsys.readouterr()
  assert 'random number generation disabled' in err

def test_random_string_generation():
  import coldwallet.crypto

  # String length is number of bits divided by 8
  rand = coldwallet.crypto.generate_random_string(bits=72)
  assert len(rand) == 72/8

  rand = coldwallet.crypto.generate_random_string(bits=36*8)
  assert len(rand) == 36

  # Strings must be unique
  rand2 = coldwallet.crypto.generate_random_string(bits=36*8)
  assert len(rand2) == 36
  assert rand != rand2

  # If number of bits is not divisble by 8 then the remaining bits must be 0
  rand = coldwallet.crypto.generate_random_string(bits=36)
  assert len(rand) == 5
  assert bytearray(rand)[4] & 0x0F == 0

def test_random_string_padding():
  import coldwallet.crypto

  # This is a test relying on a randomized algorithm. To avoid it failing by
  # chance disable random number generation instead.
  coldwallet.crypto.disable_randomness()

  # Test the zero bit padding function more rigorously:
  # Unpadded bits must sometimes be 1, padded bits must always be 0.
  for length, mask in ((1, 0x80), (2, 0xC0), (3, 0xE0), (4, 0xF0), (5, 0xF8), (6, 0xFC), (7, 0xFE), (8, 0xFF)):
    seen_mask = 0
    for n in range(5):
      rand = coldwallet.crypto.generate_random_string(bits=length)
      assert len(rand) == 1
      seen_mask = seen_mask | ord(rand)
    assert seen_mask == mask

def test_encoding_and_decoding_secret_key():
  import coldwallet.bitcoin
  import coldwallet.crypto

  # This is a test relying on a randomized algorithm. To avoid it failing by
  # chance disable random number generation instead.
  coldwallet.crypto.disable_randomness()

  # Generate a bitcoin address
  private_key = coldwallet.crypto.generate_random_string(bits=256)
  public_address = coldwallet.bitcoin.generate_public_address(private_key)
  assert public_address == "1DR2Dp74CqtqXhU9MznV2r4qTuZBGYagP"

  # Generate a coldwallet key
  coldkey = coldwallet.crypto.generate_random_string(bits=36*8)

  # Use weaker scrypt parameter setting to speed up testing
  N = 2**8 # default: 2**14

  # Encrypt one with the other
  code = coldwallet.crypto.encrypt_secret_key(private_key, coldkey, public_address, scrypt_N=N)
  assert code == "I06olv7sBr0mZ0DOV5qR8RyvXPWt8yGjFbuhlj1vDO+clw/KLpS3mhEerUyRKgft"

  # Encrypt one with the other again
  code = coldwallet.crypto.encrypt_secret_key(private_key, coldkey, public_address, scrypt_N=N)
  # A new initialization vector is used, so the resulting code changes
  assert code == "70vfOobHgodn7ICiLPWlbPAlhoCCCt5enrC9fM/Ml0uyM7gqGuiGZPPyAa5kRpK4"

  # Decrypt the private key again
  verify_key = coldwallet.crypto.decrypt_secret_key(code, coldkey, public_address, scrypt_N=N)
  assert verify_key == private_key

  # Attempt decryption with wrong public address
  public_address = "3DR2Dp74CqtqXhU9MznV2r4qTuZBGYagP"
  verify_key = coldwallet.crypto.decrypt_secret_key(code, coldkey, public_address, scrypt_N=N)
  assert verify_key != private_key

  # Attempt decryption with wrong coldwallet key
  public_address = "1DR2Dp74CqtqXhU9MznV2r4qTuZBGYagP"
  coldkey = coldwallet.crypto.generate_random_string(bits=36*8)
  verify_key = coldwallet.crypto.decrypt_secret_key(code, coldkey, public_address, scrypt_N=N)
  assert verify_key != private_key
