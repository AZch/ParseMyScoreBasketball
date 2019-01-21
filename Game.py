import datetime
from LastGame import LastGame

class Game():
    def __init__(self, timeMin, teams, lstHome, lstAway, elemBase):
        self.__timeMin = timeMin
        self.teams = teams
        self.lstHome = lstHome
        self.lstAway = lstAway
        self.elemBase = elemBase

    def checkTime(self, timePrint = 15, minNow = datetime.datetime.now().hour * 60 + datetime.datetime.now().minute):
        if self.__timeMin - minNow <= timePrint:
            return True
        else:
            return False

    def checkGame(self, kfHome, kfAway, kfMin = 1.4):
        countCleanHome = 0
        countCleanAway = 0
        if (kfHome >= kfMin and kfHome < kfAway):
            for homeGame in self.lstHome:
                if homeGame.isCleanScore(isFirstTeam=True):
                    countCleanHome += 1
                    return False
                    break
            for awayGame in self.lstAway:
                if awayGame.isCleanScore(isFirstTeam=True):
                    countCleanAway += 1
                    return False
                    break
        elif (kfAway >= kfMin and kfAway < kfHome):
            for homeGame in self.lstHome:
                if homeGame.isCleanScore(isFirstTeam=False):
                    countCleanHome += 1
                    return False
                    break
            for awayGame in self.lstAway:
                if awayGame.isCleanScore(isFirstTeam=False):
                    countCleanAway += 1
                    return False
                    break
        else:
            return False
        if countCleanAway + countCleanHome >= 1:
            return False
        return True




