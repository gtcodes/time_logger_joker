import MySQLdb
import settings
#from user import User

# assumes there excists a USER table with fields
# id (auto increment), firstname, lastname, class name

settings.init()

db = MySQLdb.connect(settings.host,settings.userName,settings.password,settings.dbName)
cursor = db.cursor()
DEBUG = False

def getVersion():
    cursor.execute("SELECT VERSION()")
    return(cursor.fetchone())

#' values should be comma seperated
def insertUser(cardID, firstName, lastName, className):
    insertQuery = "INSERT INTO USER(CARD_ID, FIRST_NAME, "+ \
                "LAST_NAME, CLASS, IS_ADMIN) VALUES(" + \
                 cardID + "," + \
                 "\"" + firstName + "\","+ \
                 "\"" + lastName + "\","+ \
                 "\"" + className + "\"," +\
                 "0)"
    if(DEBUG):
        print(insertQuery)
    commit(insertQuery)

def startTime(cardId):
    insertQuery = "INSERT INTO TIMELOG(CARD_ID, START_TIME) " +\
            "VALUES (" + cardId + ", NOW());"
    commit(insertQuery)

def selectUserById(cardID):
    selectQuery = "SELECT * FROM USER WHERE CARD_ID = " + cardID
    doQuery(selectQuery)
    # Return all the rows in a list of lists.
    result = cursor.fetchone()
    return(result)

def selectTimeLog(cardId):
    selectQuery = "SELECT * FROM TIMELOG WHERE CARD_ID = "\
            + str(cardId) + " ORDER BY START_TIME DESC;"
    if(DEBUG):
        print(selectQuery)
    doQuery(selectQuery)
    result = cursor.fetchone()
    return(result)

def updateTimeLog(logId):
    updateQuery = "update TIMELOG set END_TIME = NOW() where ID = "\
            + logId + ";"
    commit(updateQuery)

def updateUser(userID, first_name, last_name, class_name, is_admin):
    updateQuery = "update USER set FIRST_NAME='%s', LAST_NAME='%s', CLASS='%s',\
         IS_ADMIN=%d where CARD_ID=%d" % (first_name, last_name, class_name, is_admin, userID)
    commit(updateQuery)

def commit(query):
    try:
        doQuery(query)
        db.commit()
    except:
        #might want rollback on some failues?
        #TODO handle errors better
        print ("Error: we failed to commit query " + query)

def doQuery(query):
    triedReconnect = 0
    if(DEBUG):
        print("Sending query: " + query)
    while (1):
        try:
            # Execute the SQL command
            cursor.execute(query)
            return 1
        except: # Probably timed-out connection to DB
            if(triedReconnect < 1):
                if DEBUG: print("Failed initial query, trying to reconnect to db...")
                reconnect()
                triedReconnect += 1
            else:
                print("Error: Failed to send query. Is the database running?")
                return 0

def reconnect():
    # Update globals, do not make locals
    global db
    global cursor
    db = MySQLdb.connect(settings.host,settings.userName,settings.password,settings.dbName)
    cursor = db.cursor()

def close():
    db.close()
