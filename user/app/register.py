import bcrypt
from app.auth import Authenticate
from configuration.contstants import AppConstants
from app.dbUtil import DbConnect

# Class to register user to website
class RegisterUser:


    # Method to register patient details in database
    def registerPatientDetails(
        self,
        username,
        password,
        name,
        email,
        phone_number,
        dob,
        age,
        marital_status,
        address,
        state,
        country,
        pincode,
        security1,
        security2,
        security3,
    ):
        auth = Authenticate()
        if auth.checkIfUserExist(username):
            return (False, "Existing User")

        if auth.checkIfEmailExists(email):
            return (False, "Email already Exists")

        if auth.checkIfPhoneNumberExist(phone_number):
            return (False, "Phone Number already Exists")

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

        # Class for Project Constants
        const = AppConstants()

        # Retrieve table columns from Constants File
        columnList = const.login_TableColumns()
        columnList.remove("patient_id")

        isAdmin = False
        columnValues = [username, hashedPassword,
                        security1, security2, security3, isAdmin]
        dbConnect.insertRecord(columnList, columnValues)

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("patient")

        # Retrieve table columns from Constants File
        columnList = const.patient_TableColumns()
        columnValues = [name,
                        email,
                        phone_number,
                        dob,
                        age,
                        marital_status,
                        address,
                        state,
                        country,
                        pincode, ]

        dbConnect.insertRecord(columnList, columnValues)

        # Columns to be fetched from table
        columnList = ["id"]
        columnName = "email"
        columnValue = email

        # Fetch Data from Database
        sqlData = dbConnect.fetchOne(columnList, columnName, columnValue)
        id = int(sqlData[0])

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("login")
        dbConnect.updateRecord("patient_id", id, "username", username)

        # Close the Connection
        dbConnect.closeConnection()

        return (True, "User Details Successfully Persisted.")


    # Method to update user details into database
    def updateUserDetails(
        self,
        id,
        email,
        phone_number,
        dob,
        age,
        marital_status,
        address,
        state,
        country,
        pincode,

    ):  
        # Class for Project Constants
        const = AppConstants()

        # Retrieve table columns from Constants File
        updateColumnList = const.patient_TableColumns()
        updateColumnList.remove("name")

        # Class to create Database Connection
        dbConnect = DbConnect()

        # Connect to Database
        dbConnect.createConnection()

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("patient")

        updateValues = [email,
                        phone_number,
                        dob,
                        age,
                        marital_status,
                        address,
                        state,
                        country,
                        pincode, ]

        # Defining the Primary Key for condition
        primaryKey = "id"

        # Defining the Primary Key Value
        pkValue = id

        dbConnect.updateMultipleColumns(
            updateColumnList, updateValues, primaryKey, pkValue)

        # Close the Connection
        dbConnect.closeConnection()

        return (True, "User Details Successfully Updated.")


    # Method to return all user details from database
    def getAllUserDetails(
        self,
    ):
        # Columns to be fetched from table
        columnList = ["id", "name", "email", "phone_number", ]

        # Class to create Database Connection
        dbConnect = DbConnect()

        # Connect to Database
        dbConnect.createConnection()

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("patient")

        # Fetch Data from Database
        data_all = dbConnect.fetchAll(columnList)

        # Close the Connection
        dbConnect.closeConnection()

        patient_list = list()

        for data in data_all:
            patient = {}
            for i in range(len(columnList)):
                patient[columnList[i]] = data[i]
            patient_list.append(patient)

        return patient_list
    pass
