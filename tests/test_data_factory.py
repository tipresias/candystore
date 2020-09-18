# pylint: disable=missing-module-docstring,missing-function-docstring,redefined-outer-name
from datetime import date

import numpy as np
import pandas as pd
import pytest

from candystore.data_factory import CandyStore, FIRST_AFL_SEASON


FIXTURE_COLUMNS = {
    "date",
    "season",
    "season_game",
    "round",
    "home_team",
    "away_team",
    "venue",
}

BETTING_COLUMNS = {
    "date",
    "season",
    "round_number",
    "round",
    "home_team",
    "away_team",
    "home_score",
    "away_score",
    "home_margin",
    "away_margin",
    "home_win_odds",
    "away_win_odds",
    "home_win_paid",
    "away_win_paid",
    "home_line_odds",
    "away_line_odds",
    "home_line_paid",
    "away_line_paid",
    "venue",
}


@pytest.fixture
def int_seasons():
    return np.random.randint(1, 10)


@pytest.fixture
def tuple_seasons():
    current_year = date.today().year
    seasons = np.random.randint(FIRST_AFL_SEASON, current_year + 1, size=2)

    return tuple(np.sort(seasons))


@pytest.fixture(params=[int, tuple])
def data_factory(request):
    if request.param == int:
        seasons = np.random.randint(1, 10)
    elif request.param == tuple:
        current_year = date.today().year
        first_year = np.random.randint(FIRST_AFL_SEASON, current_year)
        second_year = np.random.randint(first_year + 1, current_year + 1)
        seasons = tuple([first_year, second_year])
    else:
        raise TypeError

    return CandyStore(seasons=seasons)


def test_non_postive_seasons():
    # When seasons is <= 0, it raises an exception
    seasons = np.random.randint(-10, 1)
    with pytest.raises(AssertionError, match=r"at least one season"):
        CandyStore(seasons=seasons)


def test_too_long_tuple_seasons(tuple_seasons):
    current_year = date.today().year
    # When more than two seasons are given, it raises an exception
    seasons = tuple(
        sorted(tuple_seasons + (np.random.randint(FIRST_AFL_SEASON, current_year + 1),))
    )
    with pytest.raises(AssertionError, match=r"provide two seasons"):
        CandyStore(seasons=seasons)


def test_seasons_out_of_range():
    current_year = date.today().year
    # When more than two seasons are given, it raises an exception
    seasons = (FIRST_AFL_SEASON, current_year + 1)

    with pytest.raises(AssertionError, match=r"seasons must be in the range"):
        CandyStore(seasons=(seasons[0] - 1, seasons[1]))

    with pytest.raises(AssertionError, match=r"seasons must be in the range"):
        CandyStore(seasons=(seasons[0], seasons[1] + 1))


def test_seasons_out_of_order(tuple_seasons):
    seasons = tuple(reversed(tuple_seasons))
    with pytest.raises(AssertionError, match=r"First season must be less"):
        CandyStore(seasons=seasons)


def test_unknown_seasons_format(tuple_seasons):
    seasons = list(tuple_seasons)
    with pytest.raises(TypeError, match=r"seasons argument must be"):
        CandyStore(seasons=seasons)


def test_int_season_count(int_seasons):
    data = CandyStore(seasons=int_seasons).fixtures()
    data_frame = pd.DataFrame(data)

    # It generates one season per requested season count
    assert len(data_frame["season"].drop_duplicates()) == int_seasons


def test_tuple_season_count(tuple_seasons):
    data = CandyStore(seasons=tuple_seasons).fixtures()
    data_frame = pd.DataFrame(data)

    first_season, last_season = tuple_seasons

    # It generates seasons across the given season range
    assert len(data_frame["season"].drop_duplicates()) == last_season - first_season


@pytest.mark.parametrize(
    [
        "data_type",
        "expected_columns",
    ],
    [("fixtures", FIXTURE_COLUMNS), ("betting_odds", BETTING_COLUMNS)],
)
def test_data_structure(data_factory, data_type, expected_columns):
    data = getattr(data_factory, data_type)()

    # It returns a list of fixture dictionaries
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    data_columns = set(data[0].keys())
    assert expected_columns & data_columns == expected_columns

    # It returns a data frame
    data_frame = getattr(data_factory, data_type)(to_dict=None)
    assert isinstance(data_frame, pd.DataFrame)


@pytest.mark.parametrize(
    "data_type",
    ["fixtures", "betting_odds"],
)
def test_no_duplicate_teams(data_factory, data_type):
    data = getattr(data_factory, data_type)()
    data_frame = pd.DataFrame(data)

    # It doesn't have teams play more than once per round
    round_groups = data_frame.groupby(["season", "round"])
    for _, season_round_data_frame in round_groups:
        teams = season_round_data_frame[["home_team", "away_team"]].to_numpy().flatten()
        assert len(teams) == len(np.unique(teams))


@pytest.mark.parametrize(
    "data_type",
    ["fixtures", "betting_odds"],
)
def test_no_duplicate_brisbanes(data_factory, data_type):
    data = getattr(data_factory, data_type)()
    data_frame = pd.DataFrame(data)

    # It only has one Brisbane team per round
    round_groups = data_frame.groupby(["season", "round"])
    for _, season_round_data_frame in round_groups:
        teams = season_round_data_frame[["home_team", "away_team"]].to_numpy().flatten()
        brisbane_teams = np.char.find(teams.astype("U"), "Brisbane") >= 0
        assert len(teams[brisbane_teams]) == 1


@pytest.mark.parametrize(
    ["data_type", "round_label"],
    [("fixtures", "round"), ("betting_odds", "round_number")],
)
def test_date_round_compatibility(data_factory, data_type, round_label):
    data = getattr(data_factory, data_type)()
    data_frame = pd.DataFrame(data)

    # It has rounds that increment with match dates
    season_groups = data_frame.groupby("season")
    for _, season_data_frame in season_groups:
        date_sorted_rounds = season_data_frame.sort_values("date")[
            round_label
        ].to_numpy()
        sorted_rounds = season_data_frame[round_label].sort_values().to_numpy()

        assert (date_sorted_rounds == sorted_rounds).all()
