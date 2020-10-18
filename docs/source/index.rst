Welcome to CandyStore's documentation!
======================================

.. toctree::
  :maxdepth: 2
  :caption: Contents:

  api/classes


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

Factories for randomised AFL data sets, selling candy to your unit tests.

The shape and content of the data is based on what's returned by the R package
`fitzRoy <https://github.com/jimmyday12/fitzRoy>`_, which gets most of its data from the sites
`Footywire <https://www.footywire.com/>`_ and `AFLTables <https://afltables.com/afl/afl_index.html>`_.
The column names are converted to :code:`snake_case` for convenience.

Features
--------

- Randomised values for the following AFL data sets:

  - :code:`fixtures`: Minimal AFL match data from the season schedule.
  - :code:`match_results`: Full match data, including results.
  - :code:`betting_odds`: Minimal match data with pre-game odds for the final result.
  - :code:`players`: Full set of player stats for each match.

- Some limitations on the randomness of the data to make data sets realistic:

  - Team names are all real, using the naming conventions of AFLTables.
  - Venues are all real, using the naming conventions of AFLTables.
  - Seasons can range from 1897 to the current year (inclusive).
  - Matches take place from 15th March to 30th September (inclusive),
    starting no earlier than 12pm and no later than 8pm.
  - There's one round per week, and it lasts from Wednesday to Tuesday (inclusive).
  - Each team only plays once per round.
  - Only one Brisbane team (Brisbane Lions or Bisbane Bears) plays per round
    to avoid conflicts. This permits more flexibility for users to use
    whatever naming conventions they see fit.

Installation
------------

.. code-block:: bash

  pip3 install candystore

Usage
-----

::

  from candystore import CandyStore

  candy = CandyStore()
  # Generates random AFL fixture data
  candy.fixtures()

Contribute
----------

- Issue Tracker: github.com/tipresias/candystore/issues
- Source Code: github.com/tipresias/candystore

License
-------

The project is licensed under the MIT license.