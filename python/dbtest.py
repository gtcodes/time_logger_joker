import sys
import dbConnection

def compareDbResults(fieldName, expectedValue, dbValue):
    if(expectedValue != dbValue):
        print ("expected " + fieldName + " to be: " + expectedValue
        + " but it was " + dbValue)

data = dbConnection.getVersion()
print "Database version : %s " % data

testUserFirstName = "firstname"
testUserLastName = "lastname"
testUserClass = "testclass"
cardId = 1623232524;

userString =" (" + str(cardId) + ",'" + testUserFirstName + "', '" + testUserLastName \
+ "', '" + testUserClass + "');"

dbConnection.insertUser(userString)
data = dbConnection.selectUserByName(testUserFirstName, testUserLastName)
print "fetched a user by name : " + data[1]
compareDbResults('first name', testUserFirstName, data[1])
compareDbResults('last name', testUserLastName, data[2])
compareDbResults('class name', testUserClass, data[3])
dbConnection.deleteUser(data[0])
dbConnection.startTime(str(data[0]))
dbConnection.close()
