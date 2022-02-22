import bcrypt
from app.auth import Authenticate
from app.configUtil import ConfigConnect
from app.dbUtil import DbConnect
from configuration.contstants import AppConstants


class LoginUser:

    def userLogin(
        self,
        username,
        password,
    ):
        auth = Authenticate()

        result = auth.authenticate(username, password)

        return (result[0], result[1], result[2])

    def getUserDetails(
        self,
        patient_id,
    ):
        const = AppConstants()
        dbConnect = DbConnect()
        dbConnect.createConnection()
        dbConnect.setSchema("mca")
        dbConnect.setTableName("patient")

        primaryKey = "id"
        pkValue = patient_id
        patient_data = {}

        columnList = const.patient_TableColumns()
        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)
        dbConnect.closeConnection()

        for i in range(len(columnList)):
            patient_data[columnList[i]] = data[i]

        return patient_data

    def getUsername(
        self,
        patient_id,
    ):
        dbConnect = DbConnect()
        dbConnect.createConnection()
        dbConnect.setSchema("mca")
        dbConnect.setTableName("login")

        primaryKey = "patient_id"
        pkValue = patient_id

        columnList = ["username"]
        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)
        dbConnect.closeConnection()

        username = data[0]

        return username

    def isAdmin(
        self,
        patient_id,
    ):
        dbConnect = DbConnect()
        dbConnect.createConnection()
        dbConnect.setSchema("mca")
        dbConnect.setTableName("login")

        primaryKey = "patient_id"
        pkValue = patient_id

        columnList = ["isAdmin"]
        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)
        dbConnect.closeConnection()

        isAdmin = data[0]

        return isAdmin

    def setImpersonatingAsUser(
        self,
        isAdmin,
        username,
        id
    ):
        config = ConfigConnect()
        config.set_section_config(
            "admin", "isimpersonatingasuser", isAdmin)
        config.set_section_config(
            "admin", "admin_username", username)
        config.set_section_config(
            "admin", "admin_id", id)

    def isImpersonatingAsUser(
        self,
    ):
        config = ConfigConnect()
        isimpersonatingasuser = config.get_section_config(
            "admin")["isimpersonatingasuser"]

        if isimpersonatingasuser == "False":
            return False
        else:
            return True

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

        dbConnect = DbConnect()
        dbConnect.createConnection()
        dbConnect.setSchema("mca")
        dbConnect.setTableName("login")

        primaryKey = "username"
        pkValue = username

        columnList = ["security1", "security2", "security3"]
        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        dbConnect.closeConnection()

        if security1.lower() == data[0].lower() and security2.lower() == data[1].lower() and security3.lower() == data[2].lower():
            return (True, "Please Proceed with Password Reset.")

        return (False, "Security answer didn't match. Please try again.")

    def changePassword(
        self,
        username,
        password,
    ):
        auth = Authenticate()
        if not auth.checkIfUserExist(username):
            return (False, "No such user found")

        dbConnect = DbConnect()
        dbConnect.createConnection()

        dbConnect.setSchema("mca")
        dbConnect.setTableName("login")

        hashedPassword = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt())

        const = AppConstants()

        columnList = const.login_TableColumns()[:2]

        columnValues = [username, hashedPassword]
        updateColumn = "password"
        updateValue = hashedPassword
        primaryKey = "username"
        pkValue = username
        dbConnect.updateRecord(updateColumn, updateValue, primaryKey, pkValue)

        return (True, "Password Reset Successful. Please login with new password.")

    pass
