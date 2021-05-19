"""Nexcloud_agent cog for Red-DiscordBot by Minipen."""
import asyncio
import re

from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import error, question
from redbot.core.utils.predicates import MessagePredicate

#from nextcloud import NextCloud

from .pcx_lib import SettingDisplay, checkmark

__author__ = "Minipen"

class Nexcloud_agent(commands.Cog):

    def __init__(self, bot):
        """Set up the cog."""
        super().__init__()
        self.bot = bot
        #self.config = Config.get_conf(                                                                                                                                                  
        #    self, identifier=9224364860, force_registration=True                                                                                                                        #)                                                                                                                                                                      #self.config.register_global(**self.default_global_settings) 
        
    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.command()
    async def nexcloud_hello(self, ctx):
        """Hello Nexcloud !"""
        # Your code will go here                                                                                                                                                         
        await ctx.send("Hi Carl !")

