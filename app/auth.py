import bcrypt
from configuration.contstants import AppConstants

from app.dbUtil import DbConnect


class Authenticate:
    def authenticate(self, username, password):
        dbConnect = DbConnect()
        dbConnect.createConnection()
        dbConnect.setSchema("mca")
        dbConnect.setTableName("login")

        columnList = ["username", "password", "patient_id"]
        primaryKey = columnList[0]
        pkValue = username

        sqlData = dbConnect.fetchOne(columnList, primaryKey, pkValue)
        dbConnect.closeConnection()

        if sqlData is None or len(sqlData) == 0:
            return (False, 0, "The user doesn't exist.")

        hashedPassword = bytes(sqlData[1])
        # print(hashedPassword)

        if not bcrypt.checkpw(password.encode("utf-8"), hashedPassword):
            return (False, 0, "Invalid Password")
        
        patient_id = sqlData[2]

        return (True, patient_id, "Authentication Successful")

    def checkIfUserExist(self, username):
        constant = AppConstants()

        dbConnect = DbConnect()
        dbConnect.createConnection()

        dbConnect.setSchema("mca")
        dbConnect.setTableName("login")

        columnList = constant.login_TableColumns()
        primaryKey = "username"
        pkValue = username
        sqlData = dbConnect.fetchOne(columnList, primaryKey, pkValue)
        dbConnect.closeConnection()

        if sqlData is None or len(sqlData) == 0:
            print("\nNo Records Found...\n")
            return False
        else:
            print("\nMatching Records Found...\n")
            return True

    def checkIfEmailExists(self, emailId):
        constant = AppConstants()

        dbConnect = DbConnect()
        dbConnect.createConnection()

        dbConnect.setSchema("mca")
        dbConnect.setTableName("patient")

        columnList = constant.patient_TableColumns()
        primaryKey = "email"
        pkValue = emailId
        sqlData = dbConnect.fetchOne(columnList, primaryKey, pkValue)
        dbConnect.closeConnection()

        if sqlData is None or len(sqlData) == 0:
            print("\nNo Records Found...\n")
            return False
        else:
            print("\nMatching Records Found...\n")
            return True

    def checkIfPhoneNumberExist(self, phoneNumber):
        constant = AppConstants()

        dbConnect = DbConnect()
        dbConnect.createConnection()

        dbConnect.setSchema("mca")
        dbConnect.setTableName("patient")

        columnList = constant.patient_TableColumns()
        primaryKey = "phone_number"
        pkValue = phoneNumber
        sqlData = dbConnect.fetchOne(columnList, primaryKey, pkValue)
        dbConnect.closeConnection()

        if sqlData is None or len(sqlData) == 0:
            print("\nNo Records Found...\n")
            return False
        else:
            print("\nMatching Records Found...\n")
            return True

    pass
