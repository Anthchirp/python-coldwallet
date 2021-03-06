#!/bin/bash
set -e

python -c "import sys; assert sys.hexversion >= 0x02070000, 'python too old'"
python -c "import wheel" || python -m pip install wheel
python setup.py check -s --restructuredtext
export NUMBER=$(python -c "import coldwallet; print(coldwallet.__version__)")
git tag -a v${NUMBER} -m v${NUMBER}
git push origin v${NUMBER}
python setup.py clean --all
python setup.py sdist bdist_wheel upload
python setup.py clean --all
