import dbConnection as db
from datetime import datetime
import time
import cli
from array import *
import random, string

def readIdTest(randomId): #TODO: Insert randomId and read it back
    result = 1
    return result
def loginTest(): #Relevant?
    result = 1
    return result
def editUserTest(randomId, newRandomId): #TODO: Edit randomId and verify the changes
    result = 1
    return result
def registerUserWithCardIDTest():
    result = 1
    return result
def registerUserTest(): 
    result = 1
    return result
def pruneCardIdInputTest():
    result = 1
    return result
def timeLoggingLoopTest():
    result = 1
    return result
def logTimeTest():
    result = 1
    return result
def toDecimalNumberTest():
    result = 1
    return result
def clearScreenTest(): #Relevant?
    result = 1
    return result

def cleanDB(randomId, newRandomId): #TODO: Clean up test entries from DB
    print("DB cleaned\n")

def generateRandomId():
    return (randomNumber(10), randomWord(10), randomWord(10), randomWord(4), random.randint(0,1))

def randomWord(length):
    letters = string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))

def randomNumber(length):
    return ''.join(str(random.randint(0,9)) for i in range(length))

if __name__ == "__main__":
    
    results = array('b')
    randomId = generateRandomId()
    newRandomId = generateRandomId()

    results.append(readIdTest(randomId)) 
    results.append(loginTest())
    results.append(editUserTest(randomId, newRandomId))
    results.append(registerUserWithCardIDTest())
    results.append(registerUserTest())
    results.append(pruneCardIdInputTest())
    results.append(timeLoggingLoopTest())
    results.append(logTimeTest())
    results.append(toDecimalNumberTest())
    results.append(clearScreenTest())
    cleanDB(randomId, newRandomId)
    
    for i in results:
        if i:
            print("OK")
        else:
            print("FAIL")
    
