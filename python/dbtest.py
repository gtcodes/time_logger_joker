import sys
import dbConnection

def compareDbResults(fieldName, expectedValue, dbValue):
    if(expectedValue != dbValue):
        print ("expected " + fieldName + " to be: " + expectedValue
        + " but it was " + dbValue)

data = dbConnection.getVersion()
print "Database version : %s " % data

testUserFirstName = "firstname"
testUserNewFirstName = "kevin"
testUserLastName = "lastname"
testUserClass = "testclass"
cardId = 16232


userString =" (" + str(cardId) + ",'" + testUserFirstName + "', '" + testUserLastName \
+ "', '" + testUserClass + "');"

dbConnection.insertUser(str(cardId), testUserFirstName, testUserLastName, testUserClass)

data = dbConnection.selectUserByName(testUserFirstName, testUserLastName)
print "fetched a user by name : " + data[1]
compareDbResults('first name', testUserFirstName, data[1])
compareDbResults('last name', testUserLastName, data[2])
compareDbResults('class name', testUserClass, data[3])

dbConnection.updateUser(cardId, testUserNewFirstName, testUserLastName, testUserClass, 0)
data = dbConnection.selectUserById(cardId)
compareDbResults('first name', testUserNewFirstName, data[1])

dbConnection.startTime(str(data[0]))
log = dbConnection.selectTimeLog(str(cardId))
dbConnection.updateTimeLog(str(log[0]))

dbConnection.deleteOldTimeLogs(1)
dbConnection.deleteUser(data[0])
dbConnection.close()
