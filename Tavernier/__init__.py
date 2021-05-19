"""Package for tavernier cog."""
import json
from pathlib import Path

from redbot.core.bot import Red

from .tavernier import Tavernier

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


def setup(bot: Red) -> None:
    """Loaded Tavernier cog."""
    cog = Tavernier(bot)
    bot.add_cog(cog)
