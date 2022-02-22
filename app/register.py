import bcrypt
from app.auth import Authenticate
from configuration.contstants import AppConstants
from app.dbUtil import DbConnect


class RegisterUser:

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

        dbConnect = DbConnect()
        dbConnect.createConnection()

        dbConnect.setSchema("mca")
        dbConnect.setTableName("login")

        hashedPassword = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt())

        const = AppConstants()

        columnList = const.login_TableColumns()
        columnList.remove("patient_id")

        isAdmin = False
        columnValues = [username, hashedPassword,
                        security1, security2, security3, isAdmin]
        dbConnect.insertRecord(columnList, columnValues)

        dbConnect.setSchema("mca")
        dbConnect.setTableName("patient")

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

        columnList = ["id"]
        columnName = "email"
        columnValue = email
        sqlData = dbConnect.fetchOne(columnList, columnName, columnValue)
        id = int(sqlData[0])

        dbConnect.setSchema("mca")
        dbConnect.setTableName("login")
        dbConnect.updateRecord("patient_id", id, "username", username)

        dbConnect.closeConnection()

        return (True, "User Details Successfully Persisted.")

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
        const = AppConstants()

        updateColumnList = const.patient_TableColumns()
        updateColumnList.remove("name")

        dbConnect = DbConnect()
        dbConnect.createConnection()

        dbConnect.setSchema("mca")
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
        primaryKey = "id"
        pkValue = id

        dbConnect.updateMultipleColumns(
            updateColumnList, updateValues, primaryKey, pkValue)

        dbConnect.closeConnection()

        return (True, "User Details Successfully Updated.")

    def getAllUserDetails(
        self,
    ):
        columnList = ["id", "name", "email", "phone_number", ]

        dbConnect = DbConnect()
        dbConnect.createConnection()

        dbConnect.setSchema("mca")
        dbConnect.setTableName("patient")

        data_all = dbConnect.fetchAll(columnList)

        dbConnect.closeConnection()

        patient_list = list()

        for data in data_all:
            patient = {}
            for i in range(len(columnList)):
                patient[columnList[i]] = data[i]
            patient_list.append(patient)

        return patient_list
    pass
