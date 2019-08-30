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
resultCollection = mydb["TEAM_SCORES"]
finalResult = []
teamDict = {}
list = []



def getTeamName(teamId):
    teamQuery = {"TeamID" : teamId}
    if teamId in teamDict:
      return teamDict[teamId]
    else:
      if teamId is not None:
        team = teamsData.find(teamQuery)
        teamDict[teamId] = team[0]["Team"]
        return teamDict[teamId]



def getAllResult(resultInfo, teamName):
    for result in resultInfo:  
        data = {}      
        data["MatchDate"] = result["MatchDate"]
        stadiumsId = result["SID"]
        stadiumQuery = {"SID" : stadiumsId}
        stadiumInfo = stadiumsData.find(stadiumQuery)
        data["SCity"] = stadiumInfo[0]["SCity"]
        data["SName"] = stadiumInfo[0]["SName"]
        
        data["TeamID1"] = getTeamName(result["TeamID1"])
        data["Team1_Score"] = result["Team1_Score"]
        data["TeamID2"] = getTeamName(result["TeamID2"])
        data["Team2_Score"] = result["Team2_Score"]
        
        finalResult.append(data)
    return finalResult.copy()




def part2_1():
  for team in teamsData.find():
      if len(team["TeamID"]) > 1:
        finalDict = {}
        getResultQuery = {"TeamID1": team["TeamID"]}
        getResultQuery = { "$or": [ { "TeamID1": team["TeamID"] }, { "TeamID2":  team["TeamID"]  } ] } 
        resultInfo = resultsData.find(getResultQuery)
        finalDict["Team"] = team["Team"]
        finalDict["matches"] = getAllResult(resultInfo, team["Team"])
        finalResult.clear()
        list.append(finalDict)


part2_1()
resultCollection.insert_many(list)