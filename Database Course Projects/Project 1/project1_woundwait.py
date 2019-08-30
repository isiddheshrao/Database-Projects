transactionData = {}
locksData = {}
timeStamp = 1
priorityQ = []
priorityQ2 = []

counter = 0

f = open("schedule_1.txt", "r")
dbLogs = open("dblogs_schedule1.txt", 'w+')

# do the read operation
def doReadOperation(operation):
    global transactionData
    global locksData
    transactionID = int(operation[1])
    dataItem = operation[3]
    if dataItem not in locksData:
        locksData[dataItem] = {"status" : "read", "accessList": [transactionID]}
        transactionData[transactionID]["itemLocks"].append(dataItem) 
        dbLogs.write("Transaction "+ str(transactionID)+ " Reading "+dataItem+"\n\n")
    else:
        if locksData[dataItem]["status"] == "free":
            locksData[dataItem]["status"] = "read"
            locksData[dataItem]["accessList"].append(transactionID) 
            if dataItem not in transactionData[transactionID]["itemLocks"]:
                transactionData[transactionID]["itemLocks"].append(dataItem)
            dbLogs.write("Transaction "+ str(transactionID)+ " Reading "+dataItem+"\n\n")
        else: 
            if locksData[dataItem]["status"] == "read":
                if transactionID not in locksData[dataItem]["accessList"]:
                    locksData[dataItem]["accessList"].append(transactionID)
                if dataItem not in transactionData[transactionID]["itemLocks"]:
                    transactionData[transactionID]["itemLocks"].append(dataItem)
                    dbLogs.write("Transaction "+ str(transactionID)+ " is added to the access list for "+dataItem+"\n\n")
                dbLogs.write("Transaction "+ str(transactionID)+ " Reading "+dataItem+"\n\n")
            elif locksData[dataItem]["status"] == "write":
                holdingDataItems = locksData[dataItem]["accessList"]
                oldestTransaction = getOldestTransation(holdingDataItems, transactionID)
                conflict(transactionID, oldestTransaction, dataItem," Reading ", operation) 
                    


#do write operation
def doWriteOperation(operation):
    global transactionData
    global locksData
    global priorityQ
    transactionID = int(operation[1])
    dataItem = operation[3]
    if dataItem not in locksData:
        locksData[dataItem] = {"status" : "write", "accessList": [transactionID]}
        transactionData[transactionID]["itemLocks"].append(dataItem) 
        dbLogs.write("Transaction "+ str(transactionID)+ " Writing "+dataItem+"\n\n")
    else:
        if locksData[dataItem]["status"] == "free":
            locksData[dataItem]["status"] = "write"
            locksData[dataItem]["accessList"].append(transactionID)
            if dataItem not in transactionData[transactionID]["itemLocks"]:
                transactionData[transactionID]["itemLocks"].append(dataItem)
            dbLogs.write("Transaction "+ str(transactionID)+ " Writing "+dataItem+"\n\n")
        else:
            holdingTidList = locksData[dataItem]["accessList"]
            if len(holdingTidList) == 1 and holdingTidList[0] is transactionID:
                if locksData[dataItem]["status"] == "read":
                    locksData[dataItem]["status"] = "write"
                    dbLogs.write("Transaction "+ str(transactionID)+ " Upgrading Read Lock on "+dataItem+" to Write Lock\n\n")
                else:
                    dbLogs.write("Transaction "+ str(transactionID)+ " Writing "+dataItem+"\n\n")
            else:
                oldestTransaction = getOldestTransation(holdingTidList, transactionID)
                conflict(transactionID, oldestTransaction, dataItem, " Writing ", operation)
            


# r-w or w-r conflict
def conflict(transactionID, oldestTransaction, dataItem, opr, operation):
    if woundWait(transactionID, oldestTransaction):
        dbLogs.write("Transaction "+ str(oldestTransaction)+ " releasing all data item locks" +str(transactionData[oldestTransaction]["itemLocks"])+"\n\n")
        dbLogs.write("Transaction "+ str(oldestTransaction)+ " Aborting \n\n")
        abortOrCommit(oldestTransaction, False)
        if transactionID not in locksData[dataItem]["accessList"]:
            locksData[dataItem]["accessList"].append(transactionID)
        if dataItem not in transactionData[transactionID]["itemLocks"]:
            transactionData[transactionID]["itemLocks"].append(dataItem)
        dbLogs.write("Transaction "+ str(transactionID)+ opr +dataItem+"\n\n")

        if len(priorityQ) > 0:
            runPriorityQoperation(transactionData, locksData)
    else:
        transactionWait(transactionID, dataItem)
        if operation not in priorityQ:
            priorityQ.append(operation)
            dbLogs.write("Operation "+ operation+ " Added to priority queue \n\n")


# check if wound or wait
def woundWait(reqTid, holdingTid):
    global transactionData
    if transactionData[reqTid]["timestamp"] < transactionData[holdingTid]["timestamp"]:
        return True
    return False


#make a transaction wait
def transactionWait(transactionWaitingID, dataItem):
    global transactionData
    transactionData[transactionWaitingID]["status"] = "blocked"
    dbLogs.write("Transaction "+ str(transactionWaitingID)+ " Waiting for "+dataItem+" to be release \n\n")


# check transaction status before processing 
def initialOperationChecked(transactionData, operation):
    global priorityQ
    if transactionData[int(operation[1])]["status"] == "blocked" and operation not in priorityQ:
            dbLogs.write("Operation "+ operation+ " Added to priority queue \n")
            priorityQ.append(operation)
           
    if transactionData[int(operation[1])]["status"] == "aborted":
        dbLogs.write("Transaction "+str(operation[1])+" is already Aborted \n")


# get the oldest running transaction from the list
def getOldestTransation(holdingIds, currID):
    global transactionData
    tempTS = 15
    for id in holdingIds:
        if currID is not id:
            if transactionData[id]["timestamp"] < tempTS:
                tempTS = transactionData[id]["timestamp"]
                oldestId = id
    return oldestId


#abort a transaction
def abortOrCommit(transactionID, isCommitted):
    global transactionData
    global locksData
    global priorityQ
    if isCommitted:
        transactionData[transactionID]["status"] = "committed" 
        dbLogs.write("Commit Transaction "+ str(transactionID)+"\n\n")
    else:
        transactionData[transactionID]["status"] = "aborted"
        dbLogs.write("Transaction "+ str(transactionID)+" Aborted\n\n")


    clearPriorityQ(transactionID)

    for i in range(0, len(transactionData[transactionID]["itemLocks"])):
        item = transactionData[transactionID]["itemLocks"][i]
        if transactionID in locksData[item]["accessList"]:
            locksData[item]["accessList"].remove(transactionID)
        if len(locksData[item]["accessList"]) == 0:
            locksData[item]["status"] = "free"
   
    transactionData[transactionID]["itemLocks"].clear()
    if isCommitted and len(priorityQ) > 0:
        runPriorityQoperation(transactionData, locksData)
     
        
#run the priority queue
def runPriorityQoperation(transactionData, locksData):
    global priorityQ
    dbLogs.write("Operation "+ priorityQ[0]+"running from priority queue \n\n")
    transactionData[int(priorityQ[0][1])]["status"] = "active"
    if len(priorityQ) == 1:
        executeOperation(priorityQ.pop(0), False)
    else:
        executeOperation(priorityQ.pop(0), True)


#clear the operation from the priortiy Q of a given transaction which may be either committed or aborted
def clearPriorityQ(trasactionId):
    global priorityQ
    for opr in priorityQ:
        if int(opr[1]) == trasactionId:
            priorityQ.remove(opr)




#execute the requested operation
def executeOperation(operation, pq):
    global timeStamp
    global priorityQ
    global counter
    dbLogs.write("Operation: "+ operation+"\n")
    tId = int(operation[1]) 
    if operation[0] is 'b':
        dbLogs.write("Begin Transaction "+ str(tId)+"\n\n")
        transactionData[tId] = {"status": "active", "timestamp": timeStamp, "itemLocks": []}
        timeStamp += 1
        if timeStamp is 10:
            timeStamp = 1
    
    if operation[0] is 'r':
        initialOperationChecked(transactionData, operation)
        if transactionData[tId]["status"] == "active":
            doReadOperation(operation)

    if operation[0] is 'w':
        initialOperationChecked(transactionData, operation)
        if transactionData[tId]["status"] == "active":
            doWriteOperation(operation)
                   
    if operation[0] is 'e':
        if transactionData[tId]["status"] == "aborted":
            dbLogs.write("Transaction " +str(tId)+ " is already Aborted \n\n")
        else:
            dbLogs.write("Transaction "+ str(tId)+ " releasing all data item locks" +str(transactionData[tId]["itemLocks"])+"\n\n")
            if transactionData[tId]["status"] == "blocked":
                abortOrCommit(tId, False)
            else:
                abortOrCommit(tId, True)

    if pq and len(priorityQ) > 0:
        runPriorityQoperation(transactionData, locksData)


allLine = f.readlines()
for line in allLine:
    operation = line.strip()
    operation = operation.replace(" ", "")
    executeOperation(operation, False)
    
   
f.close()
dbLogs.close()