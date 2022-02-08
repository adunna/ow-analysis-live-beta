import datetime
import time
#from pynput.keyboard import Key, Controller

# Given a chunk of a log file, extract relevant portions for stats

STAT_MAP = {
    2: ('Hero', str),
    3: ('Hero Damage Dealt', float),
    4: ('Barrier Damage Dealt', float),
    5: ('Damage Blocked', float),
    6: ('Damage Taken', float),
    7: ('Deaths', float),
    8: ('Eliminations', float),
    9: ('Final Blows', float),
    10: ('Environmental Deaths', float),
    11: ('Environmental Kills', float),
    12: ('Healing Dealt', float),
    13: ('Objective Kills', float),
    14: ('Solo Kills', float),
    15: ('Ultimates Earned', float),
    16: ('Ultimates Used', float),
    17: ('Healing Received', float),
    18: ('Ultimate Charge', float)
}  # index: (name, type)

ROLE_MAP = ['MT', 'OT', 'HSDPS', 'FDPS', 'MS', 'FS']


class PlayerStat:

    def __init__(self, PlayerName, PlayerSlot, PlayerRole, TeamNumber,
                 TeamName):
        self.PlayerName = PlayerName
        self.PlayerSlot = PlayerSlot
        self.PlayerRole = PlayerRole
        self.TeamNumber = TeamNumber
        self.TeamName = TeamName
        self.Stats = {}


class Analyzer:

    # teams: [Team1Name, Team2Name] (must match in lobby)
    # players: [[MT, OT, HSDPS, FDPS, MS, FS], [MT, OT, HSDPS, FDPS, MS, FS]]
    def __init__(self, teams, players):
        self.Teams = teams
        self.MapName = 'UNKNOWN'
        self.PlayerStats = []
        self.PerTen = False
        self.MinDuration = 999999
        self.MaxDuration = 0
        self.StartTime = int(time.time())
        for teamNumber in range(0, 2):
            teamPlayerStats = []
            for playerSlot in range(0, 6):
                teamPlayerStats.append(
                    PlayerStat(players[teamNumber][playerSlot], playerSlot,
                               ROLE_MAP[playerSlot], teamNumber,
                               teams[teamNumber]))
            self.PlayerStats.append(teamPlayerStats)
        self.PrevImpactScores = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        self.ImpactScores = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        self.ImpactDataPoints = []
        self.ImpactUpdateIndx = 0
        self.ImpactUpdateInterval = 2
        #self.keyboard = Controller()
        #self.prevToPressVal = None

    def processLine(self, line):
        line = line[11:].strip().split(',')
        if len(line) == 4:  # map data
            self.MapName = line[0]
        elif len(line) >= 15:  # player data
            self.MinDuration = min(self.MinDuration, float(line[0]))
            self.MaxDuration = max(self.MaxDuration, float(line[0]))
            playerSlot = int(line[-1])
            teamNumber = 0 if self.Teams[0] in line else 1
            for statNumber in STAT_MAP:
                try:
                    self.PlayerStats[teamNumber][playerSlot].Stats[
                        STAT_MAP[statNumber][0]] = STAT_MAP[statNumber][1](
                            line[statNumber])
                except Exception as e:
                    # could not update number for some reason
                    print("ENCOUNTERED BUT CONTINUING: " + str(e))
                    pass
            if 'Hero Damage Dealt' in self.PlayerStats[teamNumber][
                    playerSlot].Stats and 'Barrier Damage Dealt' in self.PlayerStats[
                        teamNumber][playerSlot].Stats and 'Eliminations' in self.PlayerStats[
                            teamNumber][playerSlot].Stats and 'Deaths' in self.PlayerStats[
                                teamNumber][
                                    playerSlot].Stats and 'Healing Dealt' in self.PlayerStats[
                                        teamNumber][playerSlot].Stats:
                self.PlayerStats[teamNumber][playerSlot].Stats[
                    'Impact Score'] = (self.PlayerStats[teamNumber][
                        playerSlot].Stats['Hero Damage Dealt'] * 0.001) + (
                            self.PlayerStats[teamNumber]
                            [playerSlot].Stats['Barrier Damage Dealt'] * 0.001
                        ) + (self.PlayerStats[teamNumber]
                             [playerSlot].Stats['Healing Dealt'] *
                             0.001) + (self.PlayerStats[teamNumber]
                                       [playerSlot].Stats['Eliminations']) - (
                                           self.PlayerStats[teamNumber]
                                           [playerSlot].Stats['Deaths'])
                self.ImpactScores[teamNumber][playerSlot] = self.PlayerStats[
                    teamNumber][playerSlot].Stats['Impact Score']

    def togglePerTen(self):
        self.PerTen = not self.PerTen
        return self.PerTen

    def dump(self):
        playerStatsDump = {0: [], 1: []}
        for team in range(0, 2):
            for player in range(0, 6):
                playerStatsDump[team].append({
                    'Name': self.PlayerStats[team][player].PlayerName,
                    'Role': self.PlayerStats[team][player].PlayerRole,
                    'Stats': self.PlayerStats[team][player].Stats
                })
        durationInSec = int(
            self.MaxDuration -
            self.MinDuration) if self.MinDuration < self.MaxDuration else 0
        return {
            'Map':
                self.MapName,
            'DurationInSeconds':
                durationInSec,
            'Duration':
                str(datetime.timedelta(seconds=durationInSec)),
            'StatsMode':
                'Per 10 min' if self.PerTen else 'Cumulative',
            'Teams':
                self.Teams,
            'PlayerStats':
                playerStatsDump,
            'ImpactScoreChartFormat': [[{
                'x': (self.StartTime + durationInSec) * 1000,
                'y':
                    self.PlayerStats[team][player].Stats['Impact Score']
                    if 'Impact Score' in self.PlayerStats[team][player].Stats
                    else 0
            } for player in range(0, 6)] for team in range(0, 2)]
        }

    def dumpTable(self, team):
        dataPoints = []
        for player in range(0, 6):

            dataPoint = {
                'Name': self.PlayerStats[team][player].PlayerName,
                'Role': self.PlayerStats[team][player].PlayerRole
            }

            for stat in self.PlayerStats[team][player].Stats:
                pt = self.PlayerStats[team][player].Stats[stat]
                if self.PerTen and type(pt) == float:
                    if self.MinDuration < self.MaxDuration:
                        pt = (pt /
                              (self.MaxDuration - self.MinDuration)) * 10 * 60
                    else:
                        pt = 0
                if stat == 'Impact Score':
                    dataPoint[stat] = round(pt, 2)
                else:
                    dataPoint[stat] = int(pt) if type(pt) == float else pt

            if 'Ultimates Used' in self.PlayerStats[team][
                    player].Stats and 'Ultimates Earned' in self.PlayerStats[
                        team][player].Stats:
                dataPoint['Ultimates Used / Ultimates Earned'] = "%s / %s" % (
                    dataPoint['Ultimates Used'], dataPoint['Ultimates Earned'])
            else:
                dataPoint['Ultimates Used / Ultimates Earned'] = '0 / 0'

            dataPoints.append(dataPoint)
        return dataPoints

    def dumpTableDelta(self):
        if (self.ImpactUpdateIndx == 0):
            for team in range(0, 2):
                for player in range(0, 6):
                    self.PrevImpactScores[team][player] = self.ImpactScores[
                        team][player]
        if (self.ImpactUpdateIndx != self.ImpactUpdateInterval):
            self.ImpactUpdateIndx += 1
            return self.ImpactDataPoints
        self.ImpactUpdateIndx = 0
        playerImpactScoreDeltas = []
        for team in range(0, 2):
            for player in range(0, 6):
                playerImpactScoreDeltas.append(
                    (team, player, self.ImpactScores[team][player] -
                     self.PrevImpactScores[team][player]))
        playerImpactScoreDeltas.sort(key=lambda v: -v[2])
        dataPoints = []
        for i in range(0, 3):
            dataPoints.append({
                'Player':
                    self.PlayerStats[playerImpactScoreDeltas[i][0]]
                    [playerImpactScoreDeltas[i][1]].PlayerName,
                'Team':
                    self.Teams[playerImpactScoreDeltas[i][0]],
                'DeltaImpactScore':
                    playerImpactScoreDeltas[i][2],
            })
        self.ImpactDataPoints = dataPoints
        #if playerImpactScoreDeltas[0][2] > 1:
        #    keyToPressVal = 'f' + str((playerImpactScoreDeltas[0][0]*6) + playerImpactScoreDeltas[0][1]+1)
        #    if self.MaxDuration > 1 and self.prevToPressVal != keyToPressVal:
        #        self.keyboard.press(getattr(Key, keyToPressVal))
        #        self.keyboard.release(getattr(Key, keyToPressVal))
        #        pass
        #    self.prevToPressVal = keyToPressVal
        return dataPoints