from logging import basicConfig, INFO, info
from discord.ext import commands
from dice.logic.env import token
from dice.commands.roll_commands import parseRollString
from dice.commands.profile_commands import getRoll, setCommand, addCommand, listCommand, saveCommand
from dice.commands.voter_commands import voteCommand
from dice.commands.help_commands import helpCommand

basicConfig(level=INFO)

bot = commands.Bot(command_prefix='/')
bot.remove_command("help")

async def doRoll(ctx, roll):
    #try:
    #    rollString = getRoll(ctx, roll)
    #except Exception as err:
    #    rollString = roll
    await ctx.send(parseRollString(ctx, roll))

@bot.command(help_command = None)
async def roll(ctx, *, roll):
    await doRoll(ctx, roll)

@bot.command(help_command = None)
async def r(ctx, *, roll):
    await doRoll(ctx, roll)

@bot.command(help_command = None)
async def set(ctx, *, args):
    try:
        await ctx.send(setCommand(ctx, args))
    except Exception as err:
        await ctx.send(str(err))

@bot.command(help_command = None)
async def add(ctx, *, args):
    try:
        await ctx.send(addCommand(ctx, args))
    except Exception as err:
        await ctx.send(str(err))

@bot.command(help_command = None)
async def list(ctx, *, args):
    await ctx.send(listCommand(ctx, args))

@bot.command(help_command = None)
async def save(ctx):
    saveCommand()

@bot.command(help_command = None)
async def vote(ctx, *args): 
    await voteCommand(ctx, args)

@bot.command(help_command = None)
async def help(ctx, subject = None):
    await helpCommand(ctx, subject)

bot.run(token())
