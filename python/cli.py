import dbConnection as db
from datetime import datetime

def readId():
    cmd = raw_input("What would you like to do?\n"+
                " t - Log time\n" + 
                " r - Register a new user\n" +
                " e - Edit a user\n")
   
    if (cmd == 't'):
        logTime()
    elif (cmd == 'r'):
        register()
    elif (cmd == 'e'):
        edit()
    else:
        print "\nCommand not recognized, please try again\n\n"

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