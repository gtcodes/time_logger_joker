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

class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def login():
    while(1):
        print("tidsstämpling avstängt. En lärare måste låsa upp systemet")
        if(isAdmin()):
            readId()

def isAdmin():
    cardId = readCardNumber("Kort nummer: ")
    if(cardId != -1):
        try: 
            (_,_,_,_,admin) = db.selectUserById(cardId)
            passWord = getpass.getpass("Lösenord: ")
            byteEncodedPass = passWord.encode()
            passWordHash = hashlib.sha256(byteEncodedPass).hexdigest()
            if (admin and passWordHash == ADMIN_PASS): #LAZY POWAAA
                clearScreen()
                return(True)
            else:
                print ("Det gick tyvärr inte.")
                time.sleep(1.5)
        except TypeError:
            print ("Kortnummret " + cardId + " kunde inte användas")
            print ("Försök igen")
            time.sleep(1.5)
        clearScreen()
    else:
        print("Ogiltigt kortnummer")
    return(False)

def readId():
    while(1):
        cmd = input("Vad vill du göra?\n" +
                    " t - Tidsstämpla\n" + 
                    " r - Registrera en ny användare\n" +
                    #" e - Edit a user\n" +
                    " d - Stäng av tidsstämpling\n"
                    " q - Avsluta \n")
    
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
            os.system("echo 'Hejdå!' | cowsay -d" )
            time.sleep(1.0)
            sys.exit(0)
        else:
            print (colors.FAIL + "\nKände inte igen instruktionen, försök igen\n\n" + colors.ENDC)

def editUser():
    cardID = readCardNumber("Skanna kort för användaren som skall ändras: ")
    print(cardID)
    try:
        (cardID, first_name, last_name, class_name, is_admin) = db.selectUserById(str(cardID))
        fninp = input("Förnamn("   + first_name + "): ")
        lninp = input("Efternamn(" + last_name + "): ")
        cninp = input("Klass("     + class_name + "): ")
        adinp = input("Administratör? (" + str(bool(is_admin)) + "): ")
        first_name = fninp if fninp != '' else first_name
        last_name = lninp if lninp != '' else last_name
        class_name = cninp if cninp != '' else class_name
        is_admin = adinp if adinp != '' else is_admin

        print (first_name, last_name, class_name, is_admin)
        db.updateUser(int(cardID), first_name, last_name, class_name, int(is_admin))

        print("Användaren uppdaterades med följande information")
        print("    KortNummer: " + str(cardID))
        print("       Förnamn: " + first_name)
        print("     Efternamn: " + last_name)
        print("         Klass: " + class_name)
        print(" Administratör: " + str(is_admin))
    
    except TypeError as e:
        print(e)
        print("Användare fanns inte i systemet")
    input("Tryck på [enter] för att fortsätta")
    clearScreen()

def readCardNumber(message):
    cardId = input(message)
    if (cardId == 'q'): return 'q'
    try:
        cleanedCardId = pruneCardIdInput(cardId)
        numberLong = toDecimalNumber(cleanedCardId)
        #second prune to make sure all ids are 9 decimal digits for mysql
        number = pruneCardIdInput(numberLong)       
        print(number)
    except ValueError:
        return -1
    clearScreen()
    os.system("echo 'Tack! Jag skall leta efter: " + str(cardId) + "\'" + "| cowsay" )
    time.sleep(3)
    tcflush(sys.stdin, TCIFLUSH)
    clearScreen()
    return number

def registerUserWithCardID(cardID):
    if(db.userExists(cardID)):
        print("Det finns redan en användare med det kortet.\n")
    else:
        firstName = input("  Förnamn: ")
        lastName =  input("Efternamn: ")
        className = input("    Klass: ")
        db.insertUser(cardID, firstName, lastName, className)

def registerUser():
    cardID = -1
    while (cardID != 'q'):
        cardID = readCardNumber("Visa kort: ") 
        if (cardID == -1):
            print("Ogiltigt kortnummer")
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
        uid = readCardNumber("Visa kort för att tidsregistrera eller tryck Q för att avsluta: ")
        
        if uid == 'q' or uid == 'Q':
            break
        elif uid != -1:
            try:
                logTime(uid)
            except TypeError as e: 
                #print (e)
                print (colors.WARNING + "Ingen användare med det kortnummret" + colors.ENDC)
                choice = input("Vill du registrera en ny användare med det nummret? (Y/n)")
                if (choice.lower() == "y" or choice == ""):
                    registerUserWithCardID(uid)
                    logTime(uid)
                else:
                    continue
        else:
            print(colors.FAIL + "Ogiltigt kortnummer\n" + colors.ENDC)
        
        input("Tryck enter för att fortsätta")

def logTime(uid):
    (cardID, first_name, last_name, _, _) = db.selectUserById(uid)
    timelog = db.selectTimeLog(cardID)
    if (timelog is not None):
        (logID, _, starttime, endtime) = timelog
        if (endtime is None):
            # does not allow time logs of 1 second or less
            # to stop users accidentally signing off
            if((datetime.now()-starttime).seconds < 30):
                if(input(colors.WARNING + "Är du säker på att du vill logga ut? y/N" + colors.ENDC) != 'y'):
                    return
            db.updateTimeLog(str(logID))
            print(colors.BLUE + first_name + " " + last_name + " stämplade ut"\
                    + colors.BOLD + "\nDu var här i: " + str(datetime.now()-starttime).split('.')[0] + colors.ENDC)
        else: 
            db.startTime(str(cardID))
            print(colors.GREEN + first_name + " " + last_name + " stämplade in"\
                    + colors.BOLD + " klockan " + datetime.now().strftime('%H:%M:%S') + colors.ENDC)
    else: 
        db.startTime(str(cardID))
        print(colors.GREEN + first_name + " " + last_name + " stämplade in"\
                + colors.BOLD + " klockan " + datetime.now().strftime('%H:%M:%S') + colors.ENDC)

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
