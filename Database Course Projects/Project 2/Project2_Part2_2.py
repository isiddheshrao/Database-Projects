from pymongo import MongoClient
import json
client = MongoClient()

client = MongoClient('localhost', 27017)

mydb = client["Project"]
teamsData = mydb["Teams"]
resultsData = mydb["Schedule Results"]
stadiumsData = mydb["Stadiums"]
playerData = mydb["Roasters"]
golasData = mydb["Goals"]
resultCollection = mydb["PLAYER_DATA"]

finalResult_2 = []
finalDict_2 = {}

teamDict = {}
def part2_2():
  for player in playerData.find():
      dict = {}
      # player data
      dict["FIFA Popular Name"] = player["FIFA Popular Name"]
      dict["PlayerID"] = player["PlayerID"]
      dict["Team"] = player["Team"]
      dict["Position"] = player["Position"]

      # matches played
      teamId = player["TeamID"]
      dict["matches_played"] = getMatchesPlayed(teamId)
      dict["goals"] = getGoalScored(teamId, player["PlayerID"])

      finalResult_2.append(dict)


def getMatchesPlayed(teamId):
    matchesList = []
    matchPlayedQuery = { "$or": [ {"TeamID1" : teamId}, {"TeamID2" : teamId} ] }
    matches = resultsData.find(matchPlayedQuery)
    for match in matches:
      matchesDist = {}
      matchesDist["MatchDate"] = match["MatchDate"]
      if match["TeamID1"] == teamId:
        matchesDist["OpponentTeam"] = getTeamName(match["TeamID2"])
      else:
        matchesDist["OpponentTeam"] = getTeamName(match["TeamID1"])

      stadiumsId = match["SID"]
      if stadiumsId is not None:
        stadiumQuery = {"SID" : stadiumsId}
        stadiumInfo = stadiumsData.find(stadiumQuery)
        matchesDist["SCity"] = stadiumInfo[0]["SCity"]
        matchesDist["SName"] = stadiumInfo[0]["SName"]
      matchesList.append(matchesDist)
    return matchesList


def getGoalScored(teamId, playerID):
  goalList = []
  getGoalsQuery = { "$and": [ { "TeamID": teamId }, { "PlayerID": playerID  } ] } 
  playersGoals = golasData.find(getGoalsQuery)
  for goal in playersGoals:
    goalDist ={}
    stadium ={}
    goalDist["Penalty"] = goal["Penalty"]
    goalDist["Time"] = goal["Time"]
    gameResultQuery = { "GameID" : goal["GameID"]}
    matchResult = resultsData.find(gameResultQuery)
    goalDist["MatchDate"] = matchResult[0]["MatchDate"]

    if teamId == matchResult[0]["TeamID1"]:
      goalDist["OpponentTeam"] = getTeamName(matchResult[0]["TeamID2"])
    else:
      goalDist["OpponentTeam"] = getTeamName(matchResult[0]["TeamID1"])
      
    stadiumsId = matchResult[0]["SID"]
    if stadiumsId is not None:
      if stadiumsId not in stadium:
        stadiumQuery = {"SID" : stadiumsId}
        stadiumInfo = stadiumsData.find(stadiumQuery)
        stadium[stadiumsId] = {"SCity":stadiumInfo[0]["SCity"], "SName": stadiumInfo[0]["SName"]}
      
      goalDist["SCity"] = stadium[stadiumsId]["SCity"]
      goalDist["SName"] = stadium[stadiumsId]["SName"]


    goalList.append(goalDist)

  return goalList


def getTeamName(teamId):
    teamQuery = {"TeamID" : teamId}
    if teamId in teamDict:
      return teamDict[teamId]
    else:
      if teamId is not None:
        team = teamsData.find(teamQuery)
        teamDict[teamId] = team[0]["Team"]
        return teamDict[teamId]



part2_2()
resultCollection.insert_many(finalResult_2)