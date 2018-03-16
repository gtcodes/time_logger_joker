import dbConnection as db
from datetime import datetime
import sys
import time
import getpass
import hashlib
import os
from termios import tcflush, TCIFLUSH

#ADMIN_PASS = "7bc738ff692641c00b8a9d013b42f23e1c1b794927d12c6d0941c1306d57960e"
ADMIN_PASS = "ac7e43315375cea929bac587054782f379b535a479ca84635fdb4790cea39c7e"

def login():
    while(1):
        print("Logging disabled, admin login required")
        if(isAdmin()):
            readId()

def isAdmin():
    cardId = readCardNumber("Card id: ")
    if(cardId != -1):
        try: 
            (_,_,_,_,admin) = db.selectUserById(cardId)
            passWord = getpass.getpass("Password: ")
            byteEncodedPass = passWord.encode()
            passWordHash = hashlib.sha256(byteEncodedPass).hexdigest()
            if (admin and passWordHash == ADMIN_PASS): #LAZY POWAAA
                clearScreen()
                return(True)
            else:
                print ("Sorry, that did not work.")
                time.sleep(1.5)
        except TypeError:
            print ("could not use card " + cardId)
            print ("Please try again")
            time.sleep(1.5)
        clearScreen()
    else:
        print("Invalid card number")
    return(False)

def readId():
    while(1):
        cmd = input("What would you like to do?\n"+
                    " t - Log time\n" + 
                    " r - Register a new user\n" +
                    #" e - Edit a user\n" +
                    " d - Disable logging\n"
                    " q - Quit\n")
    
        if (cmd == 't'):
            timeLoggingLoop()
        elif (cmd == 'r'):
            registerUser()
        #elif (cmd == 'e'):
        #    editUser()
        #elif (cmd == 's'):
        #    status()
        elif (cmd == 'd' and isAdmin()):
            return 0
        elif (cmd == 'q'):
            os.system("echo 'Bye!' | cowsay -d" )
            time.sleep(1.0)
            sys.exit(0)
        else:
            print ("\nCommand not recognized, please try again\n\n")

def editUser():
    cardID = readCardNumber("Enter cardID for the user to edit:")
    print(cardID)
    try:
        (cardID, first_name, last_name, class_name, is_admin) = db.selectUserById(str(cardID))
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
        print(e)
        print("User not found")
    input("Press enter to continue")
    clearScreen()

def readCardNumber(message):
    cardId = input(message)
    if (cardId == 'q'): return 'q'
    try:
        number = toDecimalNumber(cardId)
    except ValueError:
        return -1
    clearScreen()
    os.system("echo 'Thanks! I will go and look for card id: " + str(cardId) + "\'" + "| cowsay" )
    time.sleep(3)
    tcflush(sys.stdin, TCIFLUSH)
    clearScreen()
    cleanedCardId = pruneCardIdInput(number)
    return cleanedCardId

def registerUserWithCardID(cardID):
    if(db.userExists(cardID)):
        print("User with that cardID already exists, aborting \n")
    else:
        firstName = input("Enter first name:")
        lastName = input("Enter last name:")
        className = input("Enter class:")
        db.insertUser(cardID, firstName, lastName, className)

def registerUser():
    cardID = -1
    while (cardID != 'q'):
        cardID = readCardNumber("Enter cardID/scan card:")
        if (cardID == -1):
            print("Invalid cardID")
        elif (cardID != 'q'):
            registerUserWithCardID(cardID)
            return 1
    clearScreen()

def pruneCardIdInput(number):
    numberLength = len(number)
    if(numberLength > 9):
        numberLength = 9
    number = number[0:numberLength]
    return number

def timeLoggingLoop():
    while(1):
        clearScreen()
        uid = readCardNumber("Enter a user ID to log time or q to quit:")
        
        if uid == 'q':
            break
        elif uid != -1:
            try:
                logTime(uid)
            except TypeError as e: 
                #print (e)
                print ("No user with that card ID")
                choice = input("Would you like to register a new user? (Y/n)")
                if (choice.lower() == "y" or choice == ""):
                    registerUserWithCardID(uid)
                    logTime(uid)
                else:
                    continue
        else:
            print("Invalid card ID\n")
        
        input("Press enter to continue")

def logTime(uid):
    (cardID, first_name, last_name, _, _) = db.selectUserById(uid)
    timelog = db.selectTimeLog(cardID)
    if (timelog is not None):
        (logID, _, starttime, endtime) = timelog
        if (endtime is None):
            # does not allow time logs of 1 second or less
            # to stop users accidentally signing off
            if((datetime.now()-starttime).seconds < 30):
                if(input("Are you sure you wish to logout? y/N") != 'y'):
                    return
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
        return number
    return str(int(number,16))

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear') #for cross-platform goodness

if __name__ == "__main__":
    clearScreen()
    print ("Joker time logger v1.0")
    # Login is borked for now
    #login()
    readId()
