from dice.logic.env import system, campaign 
from dice.utils.file_utils import openFile, writeToFile
from json import loads, dumps

class ProfileSet:

    def __init__(self, json):
        self.json = json
        self.currentProfile = json["default"]

    @classmethod
    def newProfile(cls, playerName):
        json = {
            "player": playerName.lower(),
            "default": "default",
            "profiles": []
        }
        profileSet = cls(json)
        profileSet.addProfile("default")
        return profileSet

    def __getProfile(self, profileId):
        try:
            return next(p for p in self.json["profiles"] if p["id"] == profileId.lower())
        except:
            raise ValueError("That profile doesn't exist!")

    def __hasRoll(self, rollId):
        return next((r for r in profile["rolls"] if r["id"] == rollId.lower()), None) is not None

    def __hasProfile(self, profileId):
        return next((p for p in self.json["profiles"] if p["id"] == profileId.lower()), None) is not None

    def getRoll(self, rollId):
        profile = self.getCurrentProfile()
        return next(r for r in profile["rolls"] if r["id"] == rollId.lower())

    def addRoll(self, rollId, rollString):
        try:
            roll = self.getRoll(rollId)
            roll["roll"] = rollString
        except:
            profile = self.getCurrentProfile()
            profile["rolls"].append({
                "id": rollId.lower(),
                "roll": rollString
            })

    def deleteRoll(self, rollId):
        roll = self.getRoll(rollId)
        profile = self.getCurrentProfile()
        profile["rolls"].remove(roll)

    def getAllRolls(self):
        profile = self.getCurrentProfile()
        return profile["rolls"]

    def getCurrentProfile(self):
        return self.__getProfile(self.currentProfile)
    
    def setProfile(self, profileId):
        if not self.__hasProfile(profileId):
            raise ValueError("That profile does not exist")
        self.currentProfile = profileId
        
    def addProfile(self, profileId):
        if self.__hasProfile(profileId):
            raise ValueError("That profile already exists")
        self.json["profiles"].append({
            "id": profileId.lower(),
            "metadata": {
                "system": system(),
                "version": 1.0,
                "campaign": campaign()
            },
            "rolls": []
        })

    def addAndSetProfile(self, profileId):
        if not self.__hasProfile(profileId):
            self.addProfile(profileId)
        self.setProfile(profileId) 

    def renameProfile(self, oldId, newId):
        if self.__hasProfile(newId):
            raise ValueError("That profile already exists")
        profile = self.__getProfile(oldId)
        profile["id"] = newId.lower()
        if self.currentProfile == oldId.lower():
            self.currentProfile = profile["id"]
        if self.json["default"] == oldId.lower():
            self.json["default"] = profile["id"]

    def setDefaultProfile(self, newId):
        profile = self.__getProfile(newId)
        self.json["default"] = profile["id"]

    def deleteProfile(self, profileId):
        profile = self.__getProfile(profileId)
        self.json["profiles"].remove(profile)
        if len(self.json["profiles"]) == 0:
            self.addProfile("default")
            self.setDefaultProfile("default")
            self.setCurrentProfile("default")
        else: 
            if self.json["default"] == profile["id"]:
                self.setDefaultProfile(self.json["profiles"][0]["id"])
            if self.currentProfile == profile["id"]:
                self.setCurrentProfile(self.json["default"])

    def getAllProfiles(self):
        return self.json["profiles"]

try:
    filepath = "data/player_profiles.json"
    json = loads(openFile(filepath))
    profileSets = list(map(ProfileSet, json))
except:
    profileSets = []

def hasProfileSet(playerName):
    return next((s for s in profileSets if s.json["player"] == playerName.lower()), None) is not None

def getProfileSet(playerName):
    return next(s for s in profileSets if s.json["player"] == playerName.lower())

def addProfileSet(playerName):
    if hasProfileSet(playerName):
        raise ValueError("player already has profile set")
    profileSets.append(ProfileSet.newProfile(playerName))

def writeToJson():
    jsonString = dumps(list(map(lambda p : p.json, profileSets)), sort_keys = True, indent = 4)
    writeToFile(filepath, jsonString)
