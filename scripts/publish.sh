#!/bin/bash

./scripts/build.sh
python3 -m twine upload dist/*.whl dist/*.tar.gz
