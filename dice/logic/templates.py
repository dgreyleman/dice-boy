import re

from json import loads
from dice.utils.file_utils import openFile

REPEAT_MARKER = "{r}" 
FIND_PARAM = r"{[0-9]+}"
FIND_UNWRAPPED_PARAM = r"{\*[0-9]+}"

class Template:

    def __init__(self, templateName):
        self.template = loads(openFile(f"templates/{templateName}.json")) 

    def installToProfile(self, profileSet, params):
        splitParams = params.split(",")
        if len(splitParams) != len(self.template["required_params"]):
            raise ValueError("Incorrect param count")
        for i in range(0, len(splitParams)):
            param_name = self.template["required_params"][i]
            param_value = splitParams[i].strip()
            profileSet.addRoll(param_name, param_value)
        for install_set in self.template["install"]:
            for roll in self.template[install_set]:
                profileSet.addRoll(roll["name"], roll["roll"])

    def performAction(self, profileSet, actionName, actionParams):
        try:
            action = next(a for a in self.template["actions"] if a["name"] == actionName)
        except:
            return "Cannot perform action " + actionName
        params = actionParams.split(",")
        if REPEAT_MARKER in action["definition"]:
            return self.performRepeatAction(profileSet, action, params)
        else:
            return self.performSingleAction(profileSet, action, params)

    def performRepeatAction(self, profileSet, action, params):
        definitionReference = action["definition"][3:]

        varSet = list(set(re.findall(FIND_PARAM, definitionReference)))
        varInts = list(map(lambda v : int(v.strip("{}")) - 1, varSet))

        unwrappedVarSet = list(set(re.findall(FIND_UNWRAPPED_PARAM, definitionReference)))
        unwrappedVarInts = list(map(lambda v : int(v.strip("{*}")) - 1, unwrappedVarSet))

        varsPerIter = len(set(varInts + unwrappedVarInts))
        if len(params) % varsPerIter != 0:
            raise ValueError("Incorrect param count")

        for i in range(0, len(params), varsPerIter):
            iterParams = params[i:i+varsPerIter]
            definition = definitionReference 
            for i in range(0, len(varSet)):
                var = varSet[i]
                index = varInts[i]
                param = iterParams[index].strip()
                definition = definition.replace(var, param)
            for i in range(0, len(unwrappedVarSet)):
                var = unwrappedVarSet[i]
                index = unwrappedVarInts[i]
                param = profileSet.getRoll(iterParams[index].strip())["roll"]
                definition = definition.replace(var, param)
            components = definition.split("=")
            name = components[0].strip()
            roll = components[1].strip()
            profileSet.addRoll(name, roll)
        return f"Performed action {action['name']} {int(len(params) / varsPerIter)} times."
    
    def performSingleAction(self, profileSet, action, params):
        definition = action["definition"]
        for var in set(re.findall(FIND_PARAM, definition)):
            index = int(var.strip("{}")) - 1
            param = params[index].strip()
            definition = definition.replace(var, param)
        for var in set(re.findall(FIND_UNWRAPPED_PARAM, definition)):
            index = int(var.strip("{*}")) - 1
            param = profileSet.getRoll(params[index].strip())["roll"]
            definition = definition.replace(var, param)
        components = definition.split("=")
        name = components[0].strip()
        roll = components[1].strip()
        profileSet.addRoll(name, roll)
        return "Performed action " + action["name"]
    
