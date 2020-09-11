from datetime import date

from faker import Faker
import numpy as np
import pandas as pd
import pytest

from candystore import fixtures


FIXTURE_COLUMNS = {
    "date",
    "season",
    "season_game",
    "round",
    "home_team",
    "away_team",
    "venue",
}


@pytest.fixture
def int_seasons():
    return np.random.randint(1, 10)


@pytest.fixture
def tuple_seasons():
    current_year = date.today().year
    seasons = np.random.randint(fixtures.FIRST_AFL_SEASON, current_year + 1, size=2)

    return tuple(np.sort(seasons))


@pytest.fixture(params=[int, tuple])
def data(request):
    if request.param == int:
        seasons = np.random.randint(1, 10)
    elif request.param == tuple:
        current_year = date.today().year
        years = np.random.randint(fixtures.FIRST_AFL_SEASON, current_year + 1, size=2)
        seasons = tuple(np.sort(years))
    else:
        raise TypeError

    return fixtures.generate(seasons=seasons)


def test_non_postive_seasons():
    # When seasons is <= 0, it raises an exception
    seasons = np.random.randint(-10, 1)
    with pytest.raises(AssertionError, match=r"at least one season"):
        fixtures.generate(seasons=seasons)


def test_too_long_tuple_seasons(tuple_seasons):
    current_year = date.today().year
    # When more than two seasons are given, it raises an exception
    seasons = tuple(
        sorted(
            tuple_seasons
            + (np.random.randint(fixtures.FIRST_AFL_SEASON, current_year + 1),)
        )
    )
    with pytest.raises(AssertionError, match=r"provide two seasons"):
        fixtures.generate(seasons=seasons)


def test_seasons_out_of_range():
    current_year = date.today().year
    # When more than two seasons are given, it raises an exception
    seasons = (fixtures.FIRST_AFL_SEASON, current_year + 1)

    with pytest.raises(AssertionError, match=r"seasons must be in the range"):
        fixtures.generate(seasons=(seasons[0] - 1, seasons[1]))

    with pytest.raises(AssertionError, match=r"seasons must be in the range"):
        fixtures.generate(seasons=(seasons[0], seasons[1] + 1))


def test_seasons_out_of_order(tuple_seasons):
    seasons = tuple(reversed(tuple_seasons))
    with pytest.raises(AssertionError, match=r"First season must be less"):
        fixtures.generate(seasons=seasons)


def test_unknown_seasons_format(tuple_seasons):
    seasons = list(tuple_seasons)
    with pytest.raises(TypeError, match=r"seasons argument must be"):
        fixtures.generate(seasons=seasons)


def test_int_season_count(int_seasons):
    data = fixtures.generate(seasons=int_seasons)
    df = pd.DataFrame(data)

    # It generates one season per requested season count
    assert len(df["season"].drop_duplicates()) == int_seasons


def test_tuple_season_count(tuple_seasons):
    data = fixtures.generate(seasons=tuple_seasons)
    df = pd.DataFrame(data)

    first_season, last_season = tuple_seasons

    # It generates seasons across the given season range
    assert len(df["season"].drop_duplicates()) == last_season - first_season


def test_data_structure(data):
    # It returns a list of fixture dictionaries
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    data_columns = set(data[0].keys())
    assert FIXTURE_COLUMNS & data_columns == FIXTURE_COLUMNS


def test_no_duplicate_teams(data):
    df = pd.DataFrame(data)

    # It doesn't have teams play more than once per round
    round_groups = df.groupby(["season", "round"])
    for _, season_round_df in round_groups:
        teams = season_round_df[["home_team", "away_team"]].to_numpy().flatten()
        assert len(teams) == len(np.unique(teams))


def test_date_round_compatibility(data):
    df = pd.DataFrame(data)

    # It has rounds that increment with match dates
    season_groups = df.groupby("season")
    for _, season_df in season_groups:
        date_sorted_rounds = season_df.sort_values("date")["round"].to_numpy()
        sorted_rounds = season_df["round"].sort_values().to_numpy()
        assert (date_sorted_rounds == sorted_rounds).all()
