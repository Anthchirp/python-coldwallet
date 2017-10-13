from __future__ import absolute_import, division, print_function

__version__ = "0.0.12"

def run(*args, **kwargs):
  '''Common entry point for all cold wallet files.
     Hop from here to the relevant reader code. This is so we will always
     support cold wallet files generated from older versions.
  '''
  import coldwallet.reader

  api_readers = {
    1: coldwallet.reader.api1,
  }

  if api_readers.get(kwargs.get('api_version')) is None:
    print("This cold wallet uses an API that is newer than the installed python module.")
    print("Please update the python module by running:")
    print("  pip install --upgrade coldwallet")
    import sys
    sys.exit(1)

  return api_readers[kwargs.get('api_version')](*args, **kwargs)
