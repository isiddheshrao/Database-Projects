# Database-Projects
Consists of Personal projects done in databases and also in CSE 5331 Database Course at UTA
Database Course Projects has 2 Projects done as a part of coursework in CSE 5331. Project 1 is based on Wound-Wait Protocol.
Schedules are run as text file and checked based on wound-wait 2pl  locking Protocol.

Project done in Python 3 (Project1_woundwait.py)
Input files are as per the given schedules. (Named: “Schedule_1”… “Schedule_7”.txt)
Transaction Schedule Logs are Stored as Output files (Named: “dblogs_schedule_1”…”7”.txt)
To run different files. Please change following lines in the code:
• Line 9: f = open("Your Input file Name.txt", "r")
• Line 10: dbLogs = open("Your Output File Name.txt", 'w+')
The code uses the following functions:
1. doReadOperation: To Process Read Operations
2. doWriteOperation: To Process Write Operations
3. conflict: To process a transaction if there is a read-write or write-read conflict
4. woundWait: To Process Wound-Wait Protocol
5. transactionWait: Processing Waiting Transactions changing Transactions status to blocked and adding operation in Priority Queue
6. abortOrCommit: To process abort or commit the transactions states
7. initialOperationChecked: To Check for blocked or aborted Transaction Status before every operation.
8. runPriorityQoperation: To process the operations in the priority Queue.
9. clearPriorityQ: Remove all the operations associated with the transaction which are either committed or aborted
10. executeOperation: execute the provided operation
11. getOldestTransation: of a given list get the oldest transaction id based on the timestamp

Project 2 is based on MongoDB

Project is coded in Python 3
• The files are named Project2_Part2_1.py & Project2_Part2_2.py
• Python to MongoDB Connection is done in the code itself. (Please change the Database name and Collection name as per the naming
convention in your system for proper connectivity) (Changes if needed are on lines: 7-13 in both the files)
• Output for Project2_Part2_1.py will be stored as TEAM_SCORES Collection inside the MongoDB Database with all requested data.
• Output for Project2_Part2_2.py will be stored as PLAYER_DATA Collection inside the MongoDB Database with all requested data.
• Design and Implementation method used for Complex Nested Documents:
o Used PyMongo Python Module to Manage Connection to MongoDB Database and retrieve data.
o Made use of loops and operations to iterate through every object inside the JSON Array
o Made use of find operation of MongoDB to filter through required set of data in Stadiums, Teams, Schedule Results and Goals Collections.
o Once Final Output is ready, A new collection of the output list is made and uploaded back to MongoDB using the Insertmany Command.
