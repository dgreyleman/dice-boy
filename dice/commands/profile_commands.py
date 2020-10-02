from dice.logic.profiles import getProfileSet, addProfileSet, writeToJson 
from dice.utils.command_utils import getObjAndArgs, getArgsByOpts
from dice.logic.templates import Template

def setCommand(name, command):
    profileSet = getOrMakeProfileSet(name)
    obj, args = getObjAndArgs(command)
    if obj == "profile":
        profileSet.setProfile(args)
        return args + " is now the active profile!"
    elif obj == "default":
        profileSet.setDefaultProfile(args)
        return args + " is now the default profile!"
    else:
        return "You cannot set " + obj

def addCommand(name, command):
    profileSet = getOrMakeProfileSet(name)    
    obj, args = getObjAndArgs(command)
    if obj == "roll":
        opts = getArgsByOpts(["-n", "-r"], args)
        name = opts["-n"]
        dice = opts["-r"]
        profileSet.addRoll(name, dice)
        return "Added " + name + " as " + dice 
    elif obj == "profile":
        profileSet.addProfile(args)
        return "Added a new profile named " + args
    else:
        return "You cannot add " + obj

def getRoll(name, rollString):
    profileSet = getOrMakeProfileSet(name)
    return profileSet.getRoll(rollString)["roll"]

def listCommand(name, command):
    profileSet = getOrMakeProfileSet(name)
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

def templateCommand(name, command):
    profileSet = getOrMakeProfileSet(name)
    obj, args = getObjAndArgs(command)
    if obj == "install":
        opts = getArgsByOpts(["-t", "-n", "-p"], args)
        profileSet.addAndSetProfile(opts["-n"])
        template = Template(opts["-t"])
        template.installToProfile(profileSet, opts["-p"])
        return template.template["tips"]
    elif obj == "action":
        opts = getArgsByOpts(["-t", "-a", "-p"], args)
        template = Template(opts["-t"]) 
        try:
            return [template.performAction(profileSet, opts["-a"], opts["-p"])]
        except Exception as err:
            return ["Cannot perform action " + opts["-a"] + ": " + str(err)]
    elif obj == "list":
#       opts = getArgsByOpts(["-t", "-p"], args)
#       template = Template(
        return ["This feature coming soon!"]
    elif obj == "detail":
        return ["This feature coming soon!"]
    else:
        return [f"You cannot {command} a template"]
        
def mapProfileId(profile, currentProfile):
    profileId = profile["id"]
    if profileId == currentProfile["id"]:
        profileId += " *"
    return profileId

def renameCommand(name, command):
    profileSet = getOrMakeProfileSet(name)

def deleteCommand(name, command):
    profileSet = getOrMakeProfileSet(name)

def saveCommand():
    writeToJson()

def getOrMakeProfileSet(name):
    try:
        #return getProfileSet(ctx.message.author.name)
        return getProfileSet(name)
    except:
        addProfileSet(name)
        return getProfileSet(name)

