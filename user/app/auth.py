import bcrypt
from configuration.contstants import AppConstants
from app.dbUtil import DbConnect


# Class to authenticate user
class Authenticate:

    # Method to authenticate user
    def authenticate(self, username, password):

        # Class to create Database Connection
        dbConnect = DbConnect()

        # Connect to Database
        dbConnect.createConnection()

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("login")

        # Columns to be fetched from table
        columnList = ["username", "password", "patient_id"]

        # Defining the Primary Key for condition
        primaryKey = columnList[0]

        # Defining the Primary Key Value
        pkValue = username

        # Fetch Data from Database
        sqlData = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        # Close the Connection
        dbConnect.closeConnection()

        if sqlData is None or len(sqlData) == 0:
            return (False, 0, "The user doesn't exist.")

        hashedPassword = bytes(sqlData[1])

        if not bcrypt.checkpw(password.encode("utf-8"), hashedPassword):
            return (False, 0, "Invalid Password")

        patient_id = sqlData[2]

        return (True, patient_id, "Authentication Successful")

    
    # Method to check if user exists
    def checkIfUserExist(self, username):
        
        # Class for Project Constants
        const = AppConstants()

        # Class to create Database Connection
        dbConnect = DbConnect()

        # Connect to Database
        dbConnect.createConnection()

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("login")

        # Retrieve table columns from Constants File
        columnList = const.login_TableColumns()

        # Defining the Primary Key for condition
        primaryKey = "username"

        # Defining the Primary Key Value
        pkValue = username

        # Fetch Data from Database
        sqlData = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        # Close the Connection
        dbConnect.closeConnection()

        if sqlData is None or len(sqlData) == 0:
            print("\nNo Records Found...\n")
            return False
        else:
            print("\nMatching Records Found...\n")
            return True


    # Method to check if email exists
    def checkIfEmailExists(self, emailId):

        # Class for Project Constants
        const = AppConstants()

        # Class to create Database Connection
        dbConnect = DbConnect()

        # Connect to Database
        dbConnect.createConnection()

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("patient")

        # Retrieve table columns from Constants File
        columnList = const.patient_TableColumns()

        # Defining the Primary Key for condition
        primaryKey = "email"

        # Defining the Primary Key Value
        pkValue = emailId

        # Fetch Data from Database
        sqlData = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        # Close the Connection
        dbConnect.closeConnection()

        if sqlData is None or len(sqlData) == 0:
            print("\nNo Records Found...\n")
            return False
        else:
            print("\nMatching Records Found...\n")
            return True


    # Method to check if phone number exists
    def checkIfPhoneNumberExist(self, phoneNumber):

        # Class for Project Constants
        const = AppConstants()

        # Class to create Database Connection
        dbConnect = DbConnect()

        # Connect to Database
        dbConnect.createConnection()

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("patient")

        # Retrieve table columns from Constants File
        columnList = const.patient_TableColumns()

        # Defining the Primary Key for condition
        primaryKey = "phone_number"

        # Defining the Primary Key Value
        pkValue = phoneNumber

        # Fetch Data from Database
        sqlData = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        # Close the Connection
        dbConnect.closeConnection()

        if sqlData is None or len(sqlData) == 0:
            print("\nNo Records Found...\n")
            return False
        else:
            print("\nMatching Records Found...\n")
            return True

    pass
