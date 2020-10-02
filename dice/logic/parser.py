import re
from random import randint

class BaseComponent:
    def evaluate(self):
        pass

class RollComponent(BaseComponent):
    
    def __init__(self, count, die, minus):
        self.count = count 
        self.die = die
        self.minus = minus

    def evaluate(self):
        total = 0
        rolls = []
        countInt = int(self.count)
        dieInt = int(self.die)
        minusMod = -1 if self.minus else 1
        for i in range(0, countInt):
            roll = randint(1, dieInt) * minusMod
            total += roll
            rolls.append(roll)
        return total, rolls

class ConstantComponent(BaseComponent):

    def __init__(self, count):
        self.count = count

    def evaluate(self):
        countInt = int(self.count)
        return countInt, [countInt]

SUB_PLUS = r"\s*\+\s*"
SUB_MINUS = r"\s*\-\s*"
REPEAT_PLUS_MATCH = r"\+\++"
SEPARATE_COMPONENTS = r"[^\+]+|\+"
SIMPLE_COMPONENT_MATCH = r"^([0-9]+d[0-9]+|[0-9]+)$" 

def parseSingle(rollString, minus):
    if rollString.isdigit():
        minusMod = "-" if minus else ""
        return ConstantComponent(minusMod + rollString)
    rollComponents = rollString.lower().split("d")
    if len(rollComponents) != 2 or not (rollComponents[0].isdigit() and rollComponents[1].isdigit()):
        raise ValueError("Invalid roll string")
    return RollComponent(rollComponents[0], rollComponents[1], minus)

def splitRollString(rollString):
    components = re.sub(SUB_PLUS, "+", rollString)
    components = re.sub(SUB_MINUS, "-", components)
    components = components.replace("--", "+")
    components = components.replace("-", "+-")
    components = re.sub(REPEAT_PLUS_MATCH, "+", components)
    return re.findall(SEPARATE_COMPONENTS, components)

def mapRollNameToBaseRolls(rollString, invert, rollStack, rollLookup):
    components = splitRollString(rollString)
    mappedComponents = []
    for component in components:
        if component == "+":
            continue
        minus = component.startswith("-")
        component = component[1:] if minus else component
        if re.match(SIMPLE_COMPONENT_MATCH, component) is not None:
            mappedComponents.append(parseSingle(component, invert != minus))
        else:
            resolvedName = rollLookup(component)
            if resolvedName in rollStack:
                raise ValueError("Roll cannot be defined by itself") 
            c = mapRollNameToBaseRolls(resolvedName, invert != minus, rollStack + [resolvedName], rollLookup)
            mappedComponents.extend(c)
    return mappedComponents

def parse(rollString, rollLookup): 
    rolls = mapRollNameToBaseRolls(rollString, False, [], rollLookup)
    total = 0
    individuals = []
    for roll in rolls:
        nextRoll, nextIndividuals = roll.evaluate()
        total += nextRoll
        individuals.extend(nextIndividuals)
    return total, individuals

