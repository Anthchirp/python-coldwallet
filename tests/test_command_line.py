from __future__ import absolute_import, division

import pytest
import sys

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
