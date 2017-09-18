import dbConnection as db
from datetime import datetime

def readId():
    uid = input("Enter a user ID:")
    try:
        (cardID, first_name, last_name, _) = db.selectUserById(uid)
        #TODO: Get last timelog for this user

        #TODO: if an open timelog does not exist, start a new timeentry
        db.startTime(str(cardID))
        print "Time started for ", first_name, last_name , "at", datetime.now().strftime('%H:%M:%S')
        #TODO: else stop the timelog found

    except: 
        print "User not found\n"

if __name__ == "__main__":
    print "Joker time logger v0.1"
    while(1):
        readId()