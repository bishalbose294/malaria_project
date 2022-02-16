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
        age,
        address,
        state,
        pincode,
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

        hashedPassword = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        const = AppConstants()

        columnList = const.login_TableColumns()[:2]

        columnValues = [username, hashedPassword]
        dbConnect.insertRecord(columnList, columnValues)

        dbConnect.setSchema("mca")
        dbConnect.setTableName("patient")

        columnList = const.patient_TableColumns()
        columnValues = [name, email, phone_number, age, address, state, pincode]

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

    pass
