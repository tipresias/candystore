# candystore

![tests](https://github.com/tipresias/candystore/workflows/tests/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/candystore/badge/?version=latest)](https://candystore.readthedocs.io/en/latest/?badge=latest)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md)

Factories for randomised AFL data sets, selling candy to your unit tests.

The shape and content of the data is based on what's returned by the R package `fitzRoy`, which gets most of its data from the sites [Footywire](https://www.footywire.com/) and [AFLTables](https://afltables.com/afl/afl_index.html). The column names are converted to `snake_case` for convenience.

Data is randomised as much as is reasonably possible, with the following exceptions intended to make the data realistic:

- Teams are all real, using the naming conventions of AFLTables.
- Venues are all real, using the naming conventions of AFLTables.
- Seasons can range from 1897 to the current year (inclusive).
- Matches take place from 15th March to 30th September (inclusive), starting no earlier than 12pm and no later than 8pm.
- There's one round per week, and it lasts from Wednesday to Tuesday (inclusive).
- Each team only plays once per round.
- Only one Brisbane team (Brisbane Lions or Bisbane Bears) plays per round to avoid conflicts. This permits more flexibility for users to use whatever naming conventions they see fit.

## Installation

```bash
pip3 install candystore
```

```python
from candystore import CandyStore

candy = CandyStore()
candy.fixtures()
```

## Usage

All functions for generating data accept a `seasons` argument for defining which years to use.

- An integer indicates the number of seasons to build, but permits them to start in any valid year (all seasons will still be sequential). Default value is `1`
- A tuple of two integers indicates the specific range of years for which to build seasons.
- Methods for generating specific data sets (e.g. `fixtures()`) accept a `to_dict` param that gets passed directly to the `pandas.DataFrame` method `to_dict`. Passing `None` returns a data frame. Defaults to `'records'`.

### Fixtures

```python
candy.fixtures()

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
]
```

### Betting Odds

```python
candy.betting_odds()

[
    {
        'date': '1967-03-21 18:40:59',
        'season': 1967,
        'round': 'Round 1',
        'home_team': 'Sydney',
        'away_team': 'Fremantle',
        'venue': 'Wellington',
        'round_number': 1,
        'home_score': 26,
        'away_score': 89,
        'home_margin': -63,
        'away_margin': 63,
        'home_win_odds': 2.71,
        'away_win_odds': 1.13,
        'home_win_paid': 0.0,
        'away_win_paid': 1.13,
        'home_line_odds': 33,
        'away_line_odds': -33,
        'home_line_paid': 0.0,
        'away_line_paid': 1.92
    },
    ...
]
```

## Match results

```python
candy.match_results()

[
    {
        'date': '1933-03-18',
        'season': 1933,
        'round': 'R1',
        'home_team': 'Gold Coast',
        'away_team': 'Adelaide',
        'venue': 'Princes Park',
        'game': 0,
        'round_number': 1,
        'round_type': 'Regular',
        'home_goals': 2,
        'home_behinds': 11,
        'home_points': 23,
        'away_goals': 21,
        'away_behinds': 17,
        'away_points': 143,
        'margin': -120
    },
    ...
]
```

## Player stats

```python
candy.players()

[
    {
        'date': '1933-03-18',
        'season': 1933,
        'round': 1,
        'home_team': 'Gold Coast',
        'away_team': 'Adelaide',
        'venue': 'Princes Park',
        'local_start_time': 1437,
        'attendance': 42853,
        'hq1g': 3,
        'hq1b': 3,
        'hq2g': 2,
        'hq2b': 1,
        'hq3g': 1,
        'hq3b': 5,
        'hq4g': 3,
        'hq4b': 4,
        'home_score': 67,
        'aw1g': 1,
        'aw1b': 2,
        'aw2g': 5,
        'aw2b': 1,
        'aw3g': 0,
        'aw3b': 1,
        'aw4g': 2,
        'aw4b': 1,
        'away_score': 67,
        'umpire_1': 'William Mayo',
        'umpire_2': 'Justin Washington',
        'umpire_3': 'Brian Nicholson',
        'umpire_4': 'Barbara Lamb',
        'group_id': 353,
        'first_name': 'Elizabeth',
        'surname': 'Lewis',
        'id': 0,
        'jumper_no': 18,
        'playing_for': 'Gold Coast',
        'kicks': 6,
        'marks': 8,
        'handballs': 10,
        'goals': 1,
        'behinds': 0,
        'hit_outs': 10,
        'tackles': 3,
        'rebounds': 4,
        'inside_50s': 4,
        'clearances': 2,
        'clangers': 0,
        'frees_for': 3,
        'frees_against': 4,
        'brownlow_votes': 1,
        'contested_possessions': 2,
        'uncontested_possessions': 6,
        'contested_marks': 2,
        'marks_inside_50': 1,
        'one_percenters': 3,
        'bounces': 2,
        'goal_assists': 0,
        'time_on_ground': 14,
        'substitute': 1
    },
    ...
]
```
