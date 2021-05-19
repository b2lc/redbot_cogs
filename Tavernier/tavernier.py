"""Tavernier cog for Red-DiscordBot by Minipen."""
import asyncio
import pyhedrals
import re

from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import error, question
from redbot.core.utils.predicates import MessagePredicate

from .pcx_lib import SettingDisplay, checkmark

__author__ = "Minipen"

class Tavernier(commands.Cog):

    MAX_DICE = 100
    MAX_SIDES = 100
    DROPPED_EXPLODED_RE = re.compile(r"-\*(\d+)\*-")
    EXPLODED_RE = re.compile(r"\*(\d+)\*")
    DROPPED_RE = re.compile(r"-(\d+)-")

    def __init__(self, bot):
        """Set up the cog."""
        super().__init__()
        self.bot = bot
        #self.config = Config.get_conf(                                                                                                                                                  
        #    self, identifier=9224364860, force_registration=True                                                                                                                        #)                                                                                                                                                                      #self.config.register_global(**self.default_global_settings) 
        
    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def fuResult(self, result: int):
        resultTable = ["Non, et...", "Non", "Non, mais...", "Oui, mais...", "Oui", "Oui, et..."]
        return resultTable[result-1]

    @commands.command()
    async def hi(self, ctx):
        """This does stuff!"""
        # Your code will go here                                                                                                                                                         
        await ctx.send("Hi Carl !")

    @commands.command()
    async def lance(self, ctx: commands.Context, *, roll: str):
        """Lance quelques dés et vous donne le résultat !                                                                                                                      
        The [PyHedrals](https://github.com/StarlitGhost/pyhedrals) library is used for dice formula parsing.                                                                             
        Use the link above to learn the notation allowed. Below are a few examples:                                                              
        `2d20kh` - Roll 2d20, keep highest die (e.g. initiative advantage)                                                                                                               
        `4d4!+2` - Roll 4d4, explode on any 4s, add 2 to result                                                                                                                          
        `4d6rdl` - Roll 4d6, reroll all 1s, then drop the lowest die                                                                                                                     
        `6d6c>4` - Roll 6d6, count all dice greater than 4 as successes                                                                                                                  
        `10d10r<=2kh6` - Roll 10d10, reroll all dice less than or equal to 2, then keep the highest 6 dice                                                                               
        """
        try:
            dr = pyhedrals.DiceRoller(
                maxDice = self.MAX_DICE,
                maxSides = self.MAX_SIDES )
            result = dr.parse(roll)
            roll_message = f"\N{GAME DIE} {ctx.message.author.mention} a lancé {roll}. Résultat : **{result.result}**"
            if len(roll_message) > 2000:
                raise ValueError("La longueur du message de résultat dépasse le maximum autorisé par Discord :(")
            roll_log = "\n".join(result.strings())
            roll_log = self.DROPPED_EXPLODED_RE.sub(r"~~**\1!**~~", roll_log)
            roll_log = self.EXPLODED_RE.sub(r"**\1!**", roll_log)
            roll_log = self.DROPPED_RE.sub(r"~~\1~~", roll_log)
            roll_log = roll_log.replace(",", ", ")
            if len(roll_message) + len(roll_log) > 2000:
                roll_log = "*(Trop de dés a afficher...)*"
            await ctx.send(f"{roll_message}\n{roll_log}")
        except (
            ValueError,
            NotImplementedError,
            pyhedrals.InvalidOperandsException,
            pyhedrals.SyntaxErrorException,
            pyhedrals.UnknownCharacterException,
        ) as exception:
            await ctx.send(
                error(
                    f"{ctx.message.author.mention}, Je n'ai pas compris votre demande :\n`{str(exception)}`"
                )
            )

    @commands.command()
    async def fu(self, ctx: commands.Context, *, args: str):
        """Resoud une action de jeu en lancant des dés à six faces et vous donne le résultat de votre action façon FU !    
        Exemples :
        - jet simple : [p]fu Lancer une pierre                                                                                                                                          
         - jet avec 4 dés de bonus : [p]fu bonus 4 Escalader la falaise                                                                                                                  
         - jet avec 2 dés de malus : [p]fu malus 2 Esquiver le coup d'épée
         
        Il est possible d'abréger "bonus" en "b" et "malus" en "m". Exemple                                                                                                             
         - [p]fu b 1 Sauter                                                                                                                                                              
       """
        try:
            dr = pyhedrals.DiceRoller(
                maxDice = self.MAX_DICE,
                maxSides = self.MAX_SIDES )
            nbd = 1
            action = args
            roll = "1d6kh1"
            modeStr = args.split(' ')[0]
            supDices = 0
            if( len(args.split(' '))>2 ):
                supDices = args.split(' ')[1]
            modifiers = ""
            if (modeStr == "bonus") or (modeStr == "b"):
                nbd = nbd + int(supDices)
                modifiers = "(avec " + supDices + " dé(s) de bonus)"
                action =args.split(' ', 2)[2]
                roll = str(nbd)+"d6kh1"
         else:
                if (modeStr == "malus") or (modeStr == "m"):
                    nbd = nbd + int(supDices)
                    modifiers = "(avec " + supDices + " dé(s) de malus)"
                    action = args.split(' ', 2)[2]
                    roll = str(nbd)+"d6kl1"
            #await ctx.send(f"DEBUG: roll={roll}")                                                                                                                                       
            result = dr.parse(roll)
            strresult = self.fuResult(result.result)
            roll_message = f"{ctx.message.author.mention} a tenté : {action} {modifiers}\nC'est réussi ?  **{strresult}**  "
            if len(roll_message) > 2000:
                raise ValueError("La longueur du message de résultat dépasse le maximum autorisé par Discord :(")
            roll_log = "\n".join(result.strings())
            roll_log = self.DROPPED_EXPLODED_RE.sub(r"~~**\1!**~~", roll_log)
            roll_log = self.EXPLODED_RE.sub(r"**\1!**", roll_log)
            roll_log = self.DROPPED_RE.sub(r"~~\1~~", roll_log)
            roll_log = roll_log.replace(",", ", ")
            if len(roll_message) + len(roll_log) > 2000:
                roll_log = "*(Trop de dés a afficher...)*"
            await ctx.send(f"{roll_message} \N{GAME DIE} {roll_log}")
        except (
            ValueError,
            NotImplementedError,
            pyhedrals.InvalidOperandsException,
            pyhedrals.SyntaxErrorException,
            pyhedrals.UnknownCharacterException,
        ) as exception:
            await ctx.send(
                error(
                    f"{ctx.message.author.mention}, Je n'ai pas compris votre demande :\n`{str(exception)}`"
                )
            )

