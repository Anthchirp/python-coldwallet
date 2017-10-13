from __future__ import absolute_import, division

import sys

import pytest

def test_get_command_line_help(capsys):
  import coldwallet.command_line
  sys.argv = [ 'coldwallet', '--help' ]

  with pytest.raises(SystemExit) as exc_info:
    coldwallet.command_line.main()

  assert exc_info.value.code == 0
  out, err = capsys.readouterr()
  assert err == ''
  assert 'optional' in out

def test_reject_invalid_parameters(capsys):
  import coldwallet.command_line
  sys.argv = [ 'coldwallet', '--bork' ]

  with pytest.raises(SystemExit) as exc_info:
    coldwallet.command_line.main()

  assert exc_info.value.code == 2
  out, err = capsys.readouterr()
  assert 'unrecognized' in err and 'bork' in err

def test_show_version(capsys):
  import coldwallet.command_line
  sys.argv = [ 'coldwallet', '--version' ]

  with pytest.raises(SystemExit) as exc_info:
    coldwallet.command_line.main()

  assert exc_info.value.code == 0
  out, err = capsys.readouterr()
  assert err == ''
  assert coldwallet.__version__ in out

def test_reject_too_few_codes(capsys):
  import coldwallet.command_line
  sys.argv = [ 'coldwallet', '--codes', '1' ]

  with pytest.raises(SystemExit) as exc_info:
    coldwallet.command_line.main()

  assert exc_info.value.code == 1
  out, err = capsys.readouterr()
  assert 'minimum number of code blocks' in err
  assert out == ''

def test_create_example_keys(capsys, tmpdir):
  import coldwallet.command_line
  sys.argv = [ 'coldwallet', '--disable-randomness', '--scrypt-N', '4' ]

  coldwallet.command_line.main()

  out, err = capsys.readouterr()
  err = err.split('\n')
  assert len(err) == 4
  assert 'random number generation disabled' in err[1]
