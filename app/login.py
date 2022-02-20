from app.auth import Authenticate
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

        patient_data["name"] = data[0]
        patient_data["email"] = data[1]
        patient_data["phone_number"] = data[2]
        patient_data["age"] = data[3]
        patient_data["address"] = data[4]
        patient_data["state"] = data[5]
        patient_data["pincode"] = data[6]

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
    pass
