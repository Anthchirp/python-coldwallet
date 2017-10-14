from __future__ import absolute_import, division

import coldwallet
import coldwallet.reader
import mock
import pytest

@mock.patch('coldwallet.reader')
def test_api_redirector(mockreader):
  retval = coldwallet.run(mock.sentinel.argument, mock.sentinel.second, api_version=1, keyword=mock.sentinel.keyword)

  assert len(mockreader.method_calls) == 1
  mockreader.api1.assert_called_with(mock.sentinel.argument, mock.sentinel.second, api_version=1, keyword=mock.sentinel.keyword)
  assert retval == mockreader.api1.return_value

@mock.patch('coldwallet.reader')
def test_api_redirector_rejects_unknown_versions(mockreader, capsys):
  with pytest.raises(SystemExit) as exc_info:
    coldwallet.run(mock.sentinel.argument, mock.sentinel.second, api_version=-1, keyword=mock.sentinel.keyword)

  assert len(mockreader.method_calls) == 0
  assert exc_info.value.code == 1
  out, err = capsys.readouterr()
  assert '--upgrade' in err
