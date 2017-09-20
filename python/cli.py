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
        registerUser()
    #elif (cmd == 'e'):
    #    editUser()
    #elif (cmd == 's'):
    #    status()
    else:
        print "\nCommand not recognized, please try again\n\n"

def registerUser():
    cardID = raw_input("Enter cardID/scan card:") 
    firstName = raw_input("Enter first name:")
    lastName = raw_input("Enter last name:")
    className = raw_input("Enter class:")
    
    db.insertUser(cardID, firstName, lastName, className)

def logTime():
    while(1):
        uid = raw_input("Enter a user ID to log time or q to quit:")
        
        if uid == 'q':
            break
        
        uid = int(uid)
        try:
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
        except TypeError as e: 
            print e.message
            print "No user with that card ID"

if __name__ == "__main__":
    print "Joker time logger v0.1"
    while(1):
        readId()