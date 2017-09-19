import dbConnection as db
from datetime import datetime

def readId():
    uid = input("Enter a user ID:")
    
    try:

        logTime(uid)

    except TypeError as e: 
        print e.message
        print "No user with that card ID"

def logTime(uid):
    (cardID, first_name, last_name, _) = db.selectUserById(uid)
    timelog = db.selectTimeLog(cardID)
    if (timelog is not None):
        logID, _, starttime, endtime = timelog
        if (endtime is None): 
            db.updateTimeLog(str(logID))
            print("Time finished for " + first_name + " " + last_name
                    + "\nTime gained: " + str(datetime.now()-starttime).split('.')[0])
        else: 
            db.startTime(str(cardID))
            print("Time started for " + first_name + " " + last_name 
                    + " at " + datetime.now().strftime('%H:%M:%S'))
    else: 
        db.startTime(str(cardID))
        print("Time started for " + first_name + " " + last_name
                + " at " + datetime.now().strftime('%H:%M:%S'))


if __name__ == "__main__":
    print "Joker time logger v0.1"
    while(1):
        readId()