from dice.logic.parser import parse
from dice.commands.profile_commands import getRoll
from random import randrange

def parseRollString(ctx, rollString):
    try:
        total, rolls = parse(rollString, lambda r : getRoll(ctx.message.author.name, r))
    except:
        return "Sorry, that is not a valid roll!"
    firstRoll = rolls.pop(0)
    result = str(total) + " (" + str(firstRoll)
    for roll in rolls:
        if roll < 0:
            result += " - " + str(roll * -1)
        else:
            result += " + " + str(roll)
    result += ")"
    return f"{ctx.message.author.display_name} => {result}"

