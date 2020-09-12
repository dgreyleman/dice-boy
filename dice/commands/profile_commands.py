from dice.logic.profiles import getProfileSet, addProfileSet, writeToJson 
from dice.utils.command_utils import validatePrivateContext, getObjAndArgs, getArgsByOpts

def setCommand(ctx, command):
    validatePrivateContext(ctx)
    profileSet = getOrMakeProfileSet(ctx)
    obj, args = getObjAndArgs(command)
    if obj == "profile":
        profileSet.setProfile(args)
        return args + " is now the active profile!"
    elif obj == "default":
        profileSet.setDefaultProfile(args)
        return args + " is now the default profile!"
    else:
        return "You cannot set " + obj

def addCommand(ctx, command):
    validatePrivateContext(ctx)
    profileSet = getOrMakeProfileSet(ctx)    
    obj, args = getObjAndArgs(command)
    if obj == "roll":
        optsAndArgs = getArgsByOpts(["-n", "-r"], args)
        name = optsAndArgs["-n"]
        dice = optsAndArgs["-r"]
        profileSet.addRoll(name, dice)
        return "Added " + name + " as " + dice 
    elif obj == "profile":
        profileSet.addProfile(args)
        return "Added a new profile named " + args
    else:
        return "You cannot add " + obj

def getRoll(ctx, rollString):
    profileSet = getOrMakeProfileSet(ctx)
    return profileSet.getRoll(rollString)["roll"]

def listCommand(ctx, command):
    validatePrivateContext(ctx)
    profileSet = getOrMakeProfileSet(ctx)
    if command == "profile" or command == "profiles":
        profiles = profileSet.getAllProfiles()
        currentProfile = profileSet.getCurrentProfile()
        result = "\n".join(list(map(lambda p : mapProfileId(p, currentProfile), profiles)))
    elif command == "roll" or command == "rolls":
        rolls = profileSet.getAllRolls()
        result = "\n".join(list(map(lambda r : r["id"] + " = " + r["roll"], rolls)))
    else:
        return "You cannot list " + command
    if result == "":
        return "No results found." 
    else:
        return result

def mapProfileId(profile, currentProfile):
    profileId = profile["id"]
    if profileId == currentProfile["id"]:
        profileId += " *"
    return profileId

def renameCommand(ctx, command):
    validatePrivateContext(ctx)
    profileSet = getOrMakeProfileSet(ctx)

def deleteCommand(ctx, command):
    validatePrivateContext(ctx)
    profileSet = getOrMakeProfileSet(ctx)

def saveCommand():
    writeToJson()

def getOrMakeProfileSet(ctx):
    try:
        return getProfileSet(ctx.message.author.name)
    except:
        addProfileSet(ctx.message.author.name)
        return getProfileSet(ctx.message.author.name)

