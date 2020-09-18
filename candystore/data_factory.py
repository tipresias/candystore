"""For generating fake fixture data."""

from typing import Tuple, Union, List, Optional
from datetime import date, datetime, timedelta
from itertools import chain
import math
from functools import partial

from faker import Faker
from mypy_extensions import TypedDict
import numpy as np
import pandas as pd


SeasonRange = Tuple[int, int]

MatchData = TypedDict(
    "MatchData",
    {
        "date": str,
        "season": int,
        "round": int,
        "home_team": str,
        "away_team": str,
        "venue": str,
    },
)

FixtureData = TypedDict(
    "FixtureData",
    {
        "date": str,
        "season": int,
        "season_game": int,
        "round": int,
        "home_team": str,
        "away_team": str,
        "venue": str,
    },
)

BettingData = TypedDict(
    "BettingData",
    {
        "date": datetime,
        "season": int,
        "round_number": int,
        "round": str,
        "home_team": str,
        "away_team": str,
        "home_score": int,
        "away_score": int,
        "home_margin": int,
        "away_margin": int,
        "home_win_odds": float,
        "away_win_odds": float,
        "home_win_paid": float,
        "away_win_paid": float,
        "home_line_odds": float,
        "away_line_odds": float,
        "home_line_paid": float,
        "away_line_paid": float,
        "venue": str,
    },
)

BaseMatchData = TypedDict(
    "BaseMatchData",
    {
        "date": str,
        "season": int,
        "round": int,
        "home_team": str,
        "away_team": str,
        "venue": str,
    },
)
DateRange = TypedDict(
    "DateRange", {"datetime_start": datetime, "datetime_end": datetime}
)


FAKE = Faker()

FIRST_AFL_SEASON = 1897
MAR = 3
FIFTEENTH = 15
SEP = 9
THIRTIETH = 30
WEDNESDAY = 2
# About as early as matches ever start
MIN_MATCH_HOUR = 12
# About as late as matches ever start
MAX_MATCH_HOUR = 20

WEEK_IN_DAYS = 7
DAY_IN_HOURS = 24

# Score and margin ranges are two standard deviations plus/minus from the means
# for all recorded AFL matches
REASONABLE_SCORE_RANGE = (23, 147)
REASONABLE_MARGIN_RANGE = (0, 88)
# Roughly the payout when win odds are even
BASELINE_BET_PAYOUT = 1.92
# Hand-wavy math to get vaguely realistic win odds
WIN_ODDS_MULTIPLIER = 0.8

NON_BRISBANE_TEAMS = [
    "Richmond",
    "Carlton",
    "Melbourne",
    "Greater Western Sydney",
    "Essendon",
    "Sydney",
    "Collingwood",
    "North Melbourne",
    "Western Bulldogs",
    "Fremantle",
    "Port Adelaide",
    "St Kilda",
    "Hawthorn",
    "Adelaide",
    "Gold Coast",
    "Geelong",
    "West Coast",
    "Fitzroy",
    "University",
]
BRISBANE_TEAMS = [
    "Brisbane Bears",
    "Brisbane Lions",
]

VENUES = [
    # AFL Tables venues
    "Football Park",
    "S.C.G.",
    "Windy Hill",
    "Subiaco",
    "Moorabbin Oval",
    "M.C.G.",
    "Kardinia Park",
    "Victoria Park",
    "Waverley Park",
    "Princes Park",
    "Western Oval",
    "W.A.C.A.",
    "Carrara",
    "Gabba",
    "Docklands",
    "York Park",
    "Manuka Oval",
    "Sydney Showground",
    "Adelaide Oval",
    "Bellerive Oval",
    "Marrara Oval",
    "Traeger Park",
    "Perth Stadium",
    "Stadium Australia",
    "Wellington",
    "Lake Oval",
    "East Melbourne",
    "Corio Oval",
    "Junction Oval",
    "Brunswick St",
    "Punt Rd",
    "Glenferrie Oval",
    "Arden St",
    "Olympic Park",
    "Yarraville Oval",
    "Toorak Park",
    "Euroa",
    "Coburg Oval",
    "Brisbane Exhibition",
    "North Hobart",
    "Bruce Stadium",
    "Yallourn",
    "Cazaly's Stadium",
    "Eureka Stadium",
    "Blacktown",
    "Jiangwan Stadium",
    "Albury",
    "Riverway Stadium",
    # Footywire venues
    "AAMI Stadium",
    "ANZ Stadium",
    "UTAS Stadium",
    "Blacktown International",
    "Blundstone Arena",
    "Domain Stadium",
    "Etihad Stadium",
    "GMHBA Stadium",
    "MCG",
    "Mars Stadium",
    "Metricon Stadium",
    "Optus Stadium",
    "SCG",
    "Spotless Stadium",
    "TIO Stadium",
    "Westpac Stadium",
    "Marvel Stadium",
    "Canberra Oval",
    # Correct spelling is 'Traeger', but footywire.com is spelling it 'Traegar' in its
    # fixtures
    "TIO Traegar Park",
]


class CandyStore:
    """Data factory for different data sets related to AFL matches."""

    def __init__(self, seasons: Union[int, SeasonRange] = 1):
        """
        Instantiate the data generator.

        Params:
        -------
        seasons: The seasons to generate data for.
            If an integer, will start from a random year for which AFL data exists
            and increment for the given number of years.
            If a tuple of integers, will generate fixtures for the given range of years
            (same rules as Python's `range`).
        """
        self.seasons = seasons
        self._matches = pd.DataFrame(self._generate_seasons())

    def fixtures(
        self, to_dict: Optional[str] = "records"
    ) -> Union[pd.DataFrame, List[FixtureData]]:
        """
        Generate fixture data for the given seasons.

        Returns:
        --------
        List of fixture dictionaries that replicate fitzRoy's `get_fixture` function,
            but with Pythonic conventions (e.g. snake_case keys)
        """
        fixtures_data_frame = self._matches.pipe(self._convert_to_fixtures)

        return (
            fixtures_data_frame
            if to_dict is None
            else fixtures_data_frame.to_dict(to_dict)
        )

    def betting_odds(
        self, to_dict: Optional[str] = "records"
    ) -> Union[pd.DataFrame, List[BettingData]]:
        """
        Generate betting odds data for the given seasons.

        Returns:
        --------
        List of betting odds dictionaries that replicate fitzRoy's
            `get_footywire_betting_odds` function, but with Pythonic conventions
            (e.g. snake_case keys)
        """
        betting_odds_data_frame = self._matches.pipe(self._convert_to_betting_odds)

        return (
            betting_odds_data_frame
            if to_dict is None
            else betting_odds_data_frame.to_dict(to_dict)
        )

    @staticmethod
    def _convert_to_fixtures(match_data_frame: pd.DataFrame) -> List[FixtureData]:
        return match_data_frame.assign(
            season_game=lambda df: df.groupby("season").cumcount()
        )

    @staticmethod
    def _convert_to_betting_odds(match_data_frame: pd.DataFrame) -> List[BettingData]:
        home_score, away_score = (
            np.random.randint(*REASONABLE_SCORE_RANGE),
            np.random.randint(*REASONABLE_SCORE_RANGE),
        )
        home_line_odds = np.random.randint(*REASONABLE_MARGIN_RANGE)
        win_odds_diff = round((np.random.rand() * WIN_ODDS_MULTIPLIER), 2)
        home_win_odds_diff = win_odds_diff if home_line_odds > 0 else -1 * win_odds_diff
        home_win_odds = BASELINE_BET_PAYOUT + home_win_odds_diff
        away_win_odds = BASELINE_BET_PAYOUT - home_win_odds_diff

        return match_data_frame.assign(
            round_number=lambda df: df["round"],
            round=lambda df: "Round " + df["round"].astype(str),
            home_score=home_score,
            away_score=away_score,
            home_margin=home_score - away_score,
            away_margin=away_score - home_score,
            home_win_odds=home_win_odds,
            away_win_odds=away_win_odds,
            home_win_paid=home_win_odds * int(home_score > away_score),
            away_win_paid=away_win_odds * int(away_score > home_score),
            home_line_odds=home_line_odds,
            away_line_odds=-1 * home_line_odds,
            home_line_paid=BASELINE_BET_PAYOUT * int(home_score > away_score),
            away_line_paid=BASELINE_BET_PAYOUT * int(away_score > home_score),
        )

    def _generate_seasons(self) -> List[MatchData]:
        return list(
            chain.from_iterable(
                [self._generate_season(season) for season in self._season_range]
            )
        )

    def _generate_season(self, season: int) -> List[MatchData]:
        # Seasons have typically started in mid-to-late March since the 70s
        start_date = datetime(season, MAR, FIFTEENTH)
        # Typically, rounds start on Thursday or Friday and end on Sunday,
        # but can range from Wednesday to Tuesday, with a few exceptions.
        difference_from_wed = WEDNESDAY - start_date.weekday()
        season_start = start_date + timedelta(days=difference_from_wed)

        # Seasons typically end somewhere between mid September and mid October,
        # so we split the difference.
        season_end = datetime(season, SEP, THIRTIETH)
        week_count = math.floor((season_end - season_start).days / WEEK_IN_DAYS)

        return list(
            chain.from_iterable(
                [self._generate_round(season_start, week) for week in range(week_count)]
            )
        )

    def _generate_round(self, season_start: datetime, week: int) -> List[MatchData]:
        round_start = season_start + timedelta(days=(WEEK_IN_DAYS * week))
        round_number = week + 1

        team_count = len(NON_BRISBANE_TEAMS) + 1
        match_count = math.floor(team_count / 2)
        min_match_number = (week * match_count) + 1
        max_match_number = min_match_number + match_count

        teams = self._generate_teams()
        venues = (venue for venue in np.random.permutation(VENUES))

        match_data_func = partial(
            self._generate_match,
            round_number,
            round_start,
        )

        return [
            match_data_func(teams=(next(teams), next(teams)), venue=next(venues))
            for _ in range(min_match_number, max_match_number)
        ]

    def _generate_match(
        self,
        round_number: int,
        round_start_date: datetime,
        teams: Tuple[str, str],
        venue: str,
    ) -> MatchData:
        match_date_time = self._match_date_time(round_start_date)
        home_team, away_team = teams

        return {
            "date": str(match_date_time),
            "season": match_date_time.year,
            "round": round_number,
            "home_team": home_team,
            "away_team": away_team,
            "venue": venue,
        }

    @staticmethod
    def _match_date_time(round_start_date: datetime) -> datetime:
        raw_match_date_time = FAKE.date_time_between_dates(
            datetime_start=round_start_date,
            datetime_end=(round_start_date + timedelta(days=WEEK_IN_DAYS)),
        )
        # We need to generate the time separately to make sure we have
        # a realistic start time for the match on the randomly-generated day.
        raw_match_time = FAKE.date_time_between_dates(
            datetime_start=raw_match_date_time.replace(
                hour=MIN_MATCH_HOUR, minute=0, second=0
            ),
            datetime_end=raw_match_date_time.replace(
                hour=MAX_MATCH_HOUR, minute=0, second=0
            ),
        ).time()

        return raw_match_date_time.replace(
            hour=raw_match_time.hour,
            minute=raw_match_time.minute,
            second=raw_match_time.second,
        )

    @staticmethod
    def _generate_teams():
        # We only want one Brisbane team per round, because depending on how team names
        # are normalised we can end up with duplicate teams, which is invalid.
        # It seems that there's more consensus on how to handle other teams that moved
        # or folded.
        valid_teams = NON_BRISBANE_TEAMS + [np.random.choice(BRISBANE_TEAMS)]
        return (team for team in np.random.permutation(valid_teams))

    @property
    def _season_range(self) -> range:
        current_year = date.today().year

        if isinstance(self.seasons, int):
            return self._int_season_range(self.seasons, current_year)

        if isinstance(self.seasons, tuple):
            return self._tuple_season_range(self.seasons, current_year)

        raise TypeError(
            "seasons argument must be either an integer or a tuple of two integers"
        )

    @staticmethod
    def _int_season_range(seasons: int, current_year: int) -> range:
        assert seasons > 0, "Must generate fixture data for at least one season."

        # We add 2, because we are open to the possibility of including matches
        # from the current year in the data.
        max_start_season = current_year - seasons + 2
        start_season = np.random.choice(np.arange(FIRST_AFL_SEASON, max_start_season))
        end_season = start_season + seasons

        return range(start_season, end_season)

    @staticmethod
    def _tuple_season_range(seasons: Tuple[int, int], current_year: int) -> range:
        assert (
            len(seasons) == 2
        ), f"Must provide two seasons to have a valid range, but {seasons} was given."

        assert min(seasons) >= FIRST_AFL_SEASON and max(seasons) <= current_year + 1, (
            f"Provided seasons must be in the range of {FIRST_AFL_SEASON} to "
            f"{current_year + 1} (inclusive) to generate valid data."
        )

        assert (
            seasons[0] < seasons[1]
        ), "First season must be less than second to create a valid range."

        return range(*seasons)
