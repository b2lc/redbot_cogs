"""Package for nexcloud_agent cog."""
import json
from pathlib import Path

from redbot.core.bot import Red

from .nexcloud_agent import Nexcloud_agent

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


def setup(bot: Red) -> None:
    """Loaded nexcloud_agent cog."""
    cog = Nexcloud_agent(bot)
    bot.add_cog(cog)
