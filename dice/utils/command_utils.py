from discord.abc import PrivateChannel

def validatePrivateContext(ctx):
    if not isinstance(ctx.message.channel, PrivateChannel):
        raise ValueError("That doesn't work here...")

def getObjAndArgs(command):
    try:
        return command.split(None, 1)
    except:
        raise ValueError("I can't understand " + command)

def getArgsByOpts(opts, command):
    components = command.split()
    builder = ""
    currentOpt = ""
    optsAndArgs = { }
    for component in components:
        if component in opts:
            if currentOpt:
                optsAndArgs[currentOpt] = builder
            currentOpt = component
            builder = ""
            continue
        if not currentOpt:
            raise ValueError("No option provided")
        if not builder:
            builder += component
        else:
            builder += " " + component
    optsAndArgs[currentOpt] = builder
    if len(optsAndArgs.keys()) != len(opts):
        raise ValueError("Not all options provided")
    return optsAndArgs
