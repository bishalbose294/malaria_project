import bcrypt
from app.auth import Authenticate
from app.configUtil import ConfigConnect
from app.dbUtil import DbConnect
from configuration.contstants import AppConstants

# Class to Login user into website
class LoginUser:

    # Method to authenticate and log in user to website
    def userLogin(
        self,
        username,
        password,
    ):
        auth = Authenticate()

        result = auth.authenticate(username, password)

        return (result[0], result[1], result[2])


    # Method to retrieve user details from database
    def getUserDetails(
        self,
        patient_id,
    ):
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

        # Defining the Primary Key for condition
        primaryKey = "id"

        # Defining the Primary Key Value
        pkValue = patient_id
        patient_data = {}

        # Retrieve table columns from Constants File
        columnList = const.patient_TableColumns()

        # Fetch Data from Database
        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        # Close the Connection
        dbConnect.closeConnection()

        for i in range(len(columnList)):
            patient_data[columnList[i]] = data[i]

        return patient_data


    # Method to retrieve username from database
    def getUsername(
        self,
        patient_id,
    ):

        # Class to create Database Connection
        dbConnect = DbConnect()

        # Connect to Database
        dbConnect.createConnection()

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("login")

        # Defining the Primary Key for condition
        primaryKey = "patient_id"

        # Defining the Primary Key Value
        pkValue = patient_id

        # Columns to be fetched from table
        columnList = ["username"]

        # Fetch Data from Database
        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        # Close the Connection
        dbConnect.closeConnection()

        username = data[0]

        return username


    # Method to check if user is Admin
    def isAdmin(
        self,
        patient_id,
    ):
        # Class to create Database Connection
        dbConnect = DbConnect()

        # Connect to Database
        dbConnect.createConnection()

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("login")

        # Defining the Primary Key for condition
        primaryKey = "patient_id"

        # Defining the Primary Key Value
        pkValue = patient_id

        # Columns to be fetched from table
        columnList = ["isAdmin"]

        # Fetch Data from Database
        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        # Close the Connection
        dbConnect.closeConnection()

        isAdmin = data[0]

        return isAdmin


    # Method to set user as impersonating another user
    def setImpersonatingAsUser(
        self,
        isAdmin,
        username,
        id
    ):
    
        # Class to Connect to Config File
        config = ConfigConnect()

        # Setting configuration Data
        config.set_section_config(
            "admin", "isimpersonatingasuser", isAdmin)

        # Setting configuration Data
        config.set_section_config(
            "admin", "admin_username", username)
        
        # Setting configuration Data
        config.set_section_config(
            "admin", "admin_id", id)


    # Method to check if current user is impersonating another user
    def isImpersonatingAsUser(
        self,
    ):

        # Class to Connect to Config File
        config = ConfigConnect()

        # Fetching configuration Data
        isimpersonatingasuser = config.get_section_config(
            "admin")["isimpersonatingasuser"]

        if isimpersonatingasuser == "False":
            return False
        else:
            return True


    # Method to verify security details from Database
    def verifySecurityDetails(
        self,
        username,
        security1,
        security2,
        security3,
    ):

        auth = Authenticate()
        if not auth.checkIfUserExist(username):
            return (False, "No such user found")

        # Class to create Database Connection
        dbConnect = DbConnect()

        # Connect to Database
        dbConnect.createConnection()

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("login")

        # Defining the Primary Key for condition
        primaryKey = "username"

        # Defining the Primary Key Value
        pkValue = username

        # Columns to be fetched from table
        columnList = ["security1", "security2", "security3"]

        # Fetch Data from Database
        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        # Close the Connection
        dbConnect.closeConnection()

        if security1.lower() == data[0].lower() and security2.lower() == data[1].lower() and security3.lower() == data[2].lower():
            return (True, "Please Proceed with Password Reset.")

        return (False, "Security answer didn't match. Please try again.")


    # Method to change password of user
    def changePassword(
        self,
        username,
        password,
    ):
        auth = Authenticate()
        if not auth.checkIfUserExist(username):
            return (False, "No such user found")

        # Class to create Database Connection
        dbConnect = DbConnect()

        # Connect to Database
        dbConnect.createConnection()

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("login")

        hashedPassword = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt())
        
        updateColumn = "password"
        updateValue = hashedPassword

        # Defining the Primary Key for condition
        primaryKey = "username"

        # Defining the Primary Key Value
        pkValue = username
        dbConnect.updateRecord(updateColumn, updateValue, primaryKey, pkValue)

        return (True, "Password Reset Successful. Please login with new password.")

    pass
