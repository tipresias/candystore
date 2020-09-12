# candystore

Factories for randomised AFL data sets, selling candy to your unit tests.

The shape and content of the data is based on what's returned by the R package `fitzRoy`, which gets most of its data from the sites [Footywire](https://www.footywire.com/) and [AFLTables](https://afltables.com/afl/afl_index.html). The column names are converted to `snake_case` for convenience.

Data is randomised as much as is reasonably possible, with the following exceptions intended to make the data realistic:

- Teams are all real, using the naming conventions of AFLTables.
- Venues are all real, using the naming conventions of AFLTables.
- Seasons can range from 1897 to the current year (inclusive).
- Matches take place from 15th March to 30th September (inclusive), starting no earlier than 12pm and no later than 8pm.
- There's one round per week, and it lasts from Wednesday to Tuesday (inclusive).
- Each team only plays once per round.

## Installation

```bash
pip3 install candystore
```

```python
import candystore
```

## Usage

All functions for generating data accept a `seasons` argument for defining which years to use.

- An integer indicates the number of seasons to build, but permits them to start in any valid year (all seasons will still be sequential).
- A tuple of two integers indicates the specific range of years for which to build seasons.

### Fixtures

```python

candystore.generate_fixtures(seasons=1)

[
    {
        'date': '1967-03-16 12:37:19',
        'season': 1967,
        'season_game': 1,
        'round': 1,
        'home_team': 'Melbourne',
        'away_team': 'Brisbane Lions',
        'venue': 'Sydney Showground'
    },
    ...
    {
        'date': '1967-09-26 18:06:32',
        'season': 1967,
        'season_game': 280,
        'round': 28,
        'home_team': 'University',
        'away_team': 'Brisbane Lions',
        'venue': 'Brunswick St'
    }
]
```
