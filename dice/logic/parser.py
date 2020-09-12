import re
from random import randint

class BaseComponent:
    def evaluate(self):
        pass

class RollComponent(BaseComponent):
    
    def __init__(self):
        self.count = "" 
        self.die = ""

    def evaluate(self):
        total = 0
        rolls = []
        countInt = int(self.count)
        dieInt = int(self.die)
        for i in range(0, countInt):
            roll = randint(1, dieInt)
            total += roll
            rolls.append(roll)
        return total, rolls

class ConstantComponent(BaseComponent):

    def __init__(self):
        self.count = ""

    def evaluate(self):
        countInt = int(self.count)
        return countInt, [countInt]

SUB_PLUS = r"\s*\+\s*"
SUB_MINUS = r"\s*\-\s*"
SEPARATE_COMPONENTS = r"[^\+\-]+|\+|\-"
SIMPLE_COMPONENT_MATCH = r"\b([0-9]+d[0-9]+|[0-9]+)\b" 
COMPLEX_COMPONENT_MATCH = r"([0-9]+d[0-9]+|[0-9]+|\+|\-)"

def parseSingle(rollString) -> "BaseComponent":
    rollString = rollString.lower().replace(" ", "")
    if "d" in rollString:
        roll = RollComponent()
    else:
        roll = ConstantComponent()
    buildCount = True
    for c in rollString:
        if c == "d":
            buildCount = False
            continue
        if buildCount:
            roll.count += c
        else:
            roll.die += c
    return roll

def mapNameToBaseRolls(rollString, mapNameToRoll):
    components = re.sub(SUB_PLUS, "+", rollString)
    components = re.sub(SUB_MINUS, "-", components)
    components = re.findall(SEPARATE_COMPONENTS, components)
    decipheredComponents = []
    for component in components:
        if component == "+" or component == "-" or re.fullmatch(SIMPLE_COMPONENT_MATCH, component):
            decipheredComponents += [component]
        else:
            decipheredComponents += mapNameToBaseRolls(mapNameToRoll(component), mapNameToRoll)
    return decipheredComponents

def parse(rollString, mapNameToRoll): 
    rolls = []
    ops = []
    components = mapNameToBaseRolls(rollString, mapNameToRoll)
    for component in components:
        if component == "+" or component == "-":
            ops.append(component)
        else:
            rolls.append(parseSingle(component))
    if len(rolls) != len(ops) + 1:
        print(len(rolls) + " " + len(ops))
        raise ValueError("Wrong number of args")
    first = rolls.pop(0)
    total, individuals = first.evaluate()
    for i in range(0, len(rolls)):
        op = ops[i]
        roll = rolls[i]
        nextRoll, nextIndividuals = roll.evaluate()
        if op == "+":
            total += nextRoll
            individuals.extend(nextIndividuals)
        else:
            total -= nextRoll
            nextIndividuals = map(lambda r : r * -1, nextIndividuals)
            individuals.extend(nextIndividuals)
    return total, individuals 
