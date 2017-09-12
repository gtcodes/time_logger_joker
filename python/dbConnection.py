import MySQLdb
#from user import User

userName = "ExampleUser"
passWord = "yourPassword"
dbName = "DB_NAME"
location = "localhost"

# assumes there excists a USER table with fields
# id (auto increment), firstname, lastname, class name

db = MySQLdb.connect(location,userName,passWord,dbName)
cursor = db.cursor()

def getVersion():
    cursor.execute("SELECT VERSION()")
    return(cursor.fetchone())

#' values should be comma seperated
def insertUser(user):
    insertQuery = "INSERT INTO USER(FIRST_NAME,LAST_NAME, CLASS) VALUES"
    insertQuery = insertQuery + user
    commit(insertQuery)

#TODO refactor select to be less duplicated
def selectUserById(userID):
    selectQuery = "SELECT * FROM USER\
           WHERE ID = '%d'" % (userID)
    try:
       # Execute the SQL command
       cursor.execute(selectQuery)
       # Fetch all the rows in a list of lists.
       result = cursor.fetchone()
       return(result)
    except:
       print "Error: unable to fecth data"
    
def selectUserByName(firstName, lastName):
    selectQuery = "SELECT * FROM USER\
           WHERE FIRST_NAME = '%s' AND LAST_NAME = '%s'" % (firstName, lastName)
    try:
       # Execute the SQL command
       cursor.execute(selectQuery)
       # Fetch all the rows in a list of lists.
       result = cursor.fetchone()
       return(result)
    except:
       print "Error: unable to fecth data"

def update():
    raise NotImplementedError

def deleteClass(className):
    raise NotImplementedError
    
    #deleteQuery = "DELETE FROM USERS WHERE CLASS = '%d'" % (className)
    #commit(deleteQuery)

def deleteUser(userID):
    deleteQuery = "DELETE FROM USER WHERE ID = '%d'" % (userID)
    commit(deleteQuery)

def commit(query):
    try:
        cursor.execute(query)
        db.commit()
    except:
        #might want rollback on some failues?
        #TODO handle errors better
        print "Error: we failed to send query " + query

def close():
    db.close()
