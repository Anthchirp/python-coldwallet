from __future__ import absolute_import, division

def test_generate_checksums_for_35_bit_codes():

  # 35 random bits generated with print "".join(str(random.randrange(2)) for x in range(35))
  bitstring = '01101011111011111010000000001001100'
  number = int(bitstring, 2)
  assert number == 14486929484

  # Generate and verify checksum
  import coldwallet.keyentry
  checksum = coldwallet.keyentry.generate_entry_block_checksum(number)
  assert checksum == 25

  # Flip each bit in turn and verify that checksum is different
  for position in range(len(bitstring)):
    fakestring = bitstring[:position] + \
                 ('1' if bitstring[position] == '0' else '0') + \
                 bitstring[position+1:]
    fakenumber = int(fakestring, 2)
    assert fakenumber != 14486929484
    fakesum = coldwallet.keyentry.generate_entry_block_checksum(fakenumber)

    # As there are 35 bits to flip and only 32 possible checksums some
    # collisions are expected. Ignore these.
    if position not in (14, 26):
      assert fakesum != checksum, "can fake string at position %d with %d != %d" % (position, fakenumber, number)
