import dbConnection as db
from datetime import datetime
import sys
import time
import getpass

ADMIN_PASS = "joker"

def login():
    while(1):
        cardID = getpass.getpass("Card id: ")
        try: 
            (_,_,_,_,admin) = db.selectUserById(int(cardID))
            if (admin and getpass.getpass("Password: ") == ADMIN_PASS): #LAZY POWAAA
                readId()
        except TypeError:
            print "Please try again"

def readId():
    while(1):
        cmd = raw_input("What would you like to do?\n"+
                    " t - Log time\n" + 
                    " r - Register a new user\n" +
                    " e - Edit a user\n" +
                    " q - Quit\n")
    
        if (cmd == 't'):
            logTime()
        elif (cmd == 'r'):
            registerUser()
        #elif (cmd == 'e'):
        #    editUser()
        #elif (cmd == 's'):
        #    status()
        elif (cmd == 'q'):
            print "bye :)"
            time.sleep(0.5)
            sys.exit(0)
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
            (cardID, first_name, last_name, _, _) = db.selectUserById(uid)
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
            choice = raw_input("Would you like to register a new user? (y/n)")
            if (choice == "y"):
                registerUser()

if __name__ == "__main__":
    print "Joker time logger v0.1"
    login()
    #readId()