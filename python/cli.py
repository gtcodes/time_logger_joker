import dbConnection as db
from datetime import datetime
import sys
import time
import getpass
import hashlib

#ADMIN_PASS = "8f1f2c12ad57b0c88cb9b35251c6fce053ae711a3ec518cb80dd6c922819e029"
ADMIN_PASS = "7bc738ff692641c00b8a9d013b42f23e1c1b794927d12c6d0941c1306d57960e"

def login():
    while(1):
        cardID = getpass.getpass("Card id: ")
        cardID = pruneCardIdInput(CardID)
        try: 
            (_,_,_,_,admin) = db.selectUserById(cardID)
            passWord = getpass.getpass("Password: ")
            byteEncodedPass = passWord.encode()
            passWordHash = hashlib.sha256(byteEncodedPass).hexdigest()
            if (admin and passWordHash == ADMIN_PASS): #LAZY POWAAA
                readId()
        except TypeError:
            print ("could not use card " + cardID)
            print ("Please try again")

def readId():
    while(1):
        cmd = input("What would you like to do?\n"+
                    " t - Log time\n" + 
                    " r - Register a new user\n" +
                    " e - Edit a user\n" +
                    " q - Quit\n")
    
        if (cmd == 't'):
            timeLoggingLoop()
        elif (cmd == 'r'):
            registerUser()
        elif (cmd == 'e'):
            editUser()
        #elif (cmd == 's'):
        #    status()
        elif (cmd == 'q'):
            print ("bye :)")
            time.sleep(0.5)
            sys.exit(0)
        else:
            print ("\nCommand not recognized, please try again\n\n")

def editUser():
    cardID = input("Enter cardID for the user to edit:")
    print(cardID)
    try:
        (cardID, first_name, last_name, class_name, is_admin) = db.selectUserById(int(cardID))
        fninp = input("First name(" + first_name + "): ")
        lninp = input("Last name(" + last_name + "): ")
        cninp = input("Class name(" + class_name + "): ")
        adinp = input("Admin (" + str(bool(is_admin)) + "): ")
        first_name = fninp if fninp != '' else first_name
        last_name = lninp if lninp != '' else last_name
        class_name = cninp if cninp != '' else class_name
        is_admin = adinp if adinp != '' else is_admin

        print (first_name, last_name, class_name, is_admin)
        db.updateUser(int(cardID), first_name, last_name, class_name, int(is_admin))

        print("User updated with the following information")
        print("    CardID: " + str(cardID))
        print("      Name: " + first_name)
        print("  LastName: " + last_name)
        print("     Class: " + class_name)
        print("     Admin: " + str(is_admin))
    except TypeError as e:
        print(e.message)
        print("User not found")

def registerUserWithCardID(cardID):
    firstName = input("Enter first name:")
    lastName = input("Enter last name:")
    className = input("Enter class:")
    cleanedCardID = pruneCardIdInput(cardID)
    db.insertUser(cleanedCardID, firstName, lastName, className)

def registerUser():
    registerUserWithCardID(input("Enter cardID/scan card:"))

def pruneCardIdInput(number):
    number = toDecimalNumber(number)
    numberLength = len(number)
    if(numberLength > 9):
        numberLength = 9;
    number = number[0:numberLength]
    return number

def timeLoggingLoop():
    while(1):
        uid = input("Enter a user ID to log time or q to quit:")
        
        if uid == 'q':
            break
        
        uid = pruneCardIdInput(uid)
        try:
            logTime(uid)
        except TypeError as e: 
            #print (e.message)
            print ("No user with that card ID")
            choice = input("Would you like to register a new user? (y/n)")
            if (choice == "y"):
                registerUserWithCardID(uid)
                logTime(uid)

def logTime(uid):
    print("we are trying to logtime with " + uid)
    (cardID, first_name, last_name, _, _) = db.selectUserById(uid)
    timelog = db.selectTimeLog(cardID)
    if (timelog is not None):
        (logID, _, starttime, endtime) = timelog
        if (endtime is None):
            # does not allow time logs of 1 second or less
            # to stop users accidentally signing off
            if((datetime.now()-starttime).seconds > 1):
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

def toDecimalNumber(number):
    if(number.isdigit()):
        return number;
    return str(int(number,16))

if __name__ == "__main__":
    print ("Joker time logger v0.1")
    #login()
    readId()
