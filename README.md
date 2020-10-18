# candystore

![tests](https://github.com/tipresias/candystore/workflows/tests/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/candystore/badge/?version=latest)](https://candystore.readthedocs.io/en/latest/?badge=latest)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md)

Factories for randomised AFL data sets, selling candy to your unit tests.

The shape and content of the data is based on what's returned by the R package `fitzRoy`, which gets most of its data from the sites [Footywire](https://www.footywire.com/) and [AFLTables](https://afltables.com/afl/afl_index.html). The column names are converted to `snake_case` for convenience.

## Installation

```bash
pip3 install candystore
```

```python
from candystore import CandyStore

candy = CandyStore()
candy.fixtures()
```

## Documentation

More-detailed documentation can be found at https://candystore.readthedocs.io/en/latest/
