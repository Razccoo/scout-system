"""A collection of tools to read and process soccer data from various sources."""

__version__ = "1.8.1"

__all__ = [
    "ClubElo",
    "ESPN",
    "FBref",
    "FiveThirtyEight",
    "FotMob",
    "MatchHistory",
    "Sofascore",
    "SoFIFA",
    "Understat",
    "WhoScored",
]


from .fotmob import FotMob
from .sofascore import Sofascore
