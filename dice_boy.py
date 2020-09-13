from logging import basicConfig, INFO, info
from discord.ext import commands
from discord.abc import PrivateChannel
from dice.logic.env import token
from dice.commands.roll_commands import parseRollString
from dice.commands.profile_commands import setCommand, addCommand, listCommand, saveCommand, templateCommand
from dice.commands.voter_commands import voteCommand
from dice.commands.help_commands import helpCommand

basicConfig(level=INFO)

bot = commands.Bot(command_prefix='/')
bot.remove_command("help")

async def doRoll(ctx, roll):
    await ctx.send(parseRollString(ctx, roll))

def validatePrivateContext(ctx):
    if not isinstance(ctx.message.channel, PrivateChannel):
        raise ValueError("That doesn't work here...")

@bot.command(help_command = None)
async def roll(ctx, *, roll):
    await doRoll(ctx, roll)

@bot.command(help_command = None)
async def r(ctx, *, roll):
    await doRoll(ctx, roll)

@bot.command(help_command = None)
async def set(ctx, *, args):
    try:
        validatePrivateContext(ctx)
        await ctx.send(setCommand(ctx.message.author.name, args))
    except Exception as err:
        await ctx.send(str(err))

@bot.command(help_command = None)
async def add(ctx, *, args):
    try:
        validatePrivateContext(ctx)
        await ctx.send(addCommand(ctx.message.author.name, args))
    except Exception as err:
        await ctx.send(str(err))

@bot.command(help_command = None)
async def list(ctx, *, args):
    try:
        validatePrivateContext(ctx)
        await ctx.send(listCommand(ctx.message.author.name, args))
    except Exception as err:
        await ctx.send(str(err))

@bot.command(help_command = None)
async def save(ctx):
    saveCommand()

@bot.command(help_command = None)
async def vote(ctx, *args): 
    await voteCommand(ctx, args)

@bot.command(help_command = None)
async def help(ctx, subject = None):
    try:
        validatePrivateContext(ctx)
        await helpCommand(ctx, subject)
    except Exception as err:
        await ctx.send(str(err))

@bot.command(help_command = None)
async def template(ctx, *, args):
    try:
        validatePrivateContext(ctx)
        for res in templateCommand(ctx.message.author.name, args):
            await ctx.send(res) 
    except Exception as err:
        await ctx.send(str(err))


bot.run(token())
