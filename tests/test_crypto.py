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
  assert ord(rand[4]) & 0x0F == 0

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
