from datetime import datetime
from app.configUtil import ConfigConnect
from app.dbUtil import DbConnect
from configuration.contstants import AppConstants
import os


class Results:
    def saveImageToFolder(
        self,
    ):
        pass

    def persistDataToDB(
        self,
        patient_id,
        name_of_image,
        infected,
        number_of_rbc,
        trophozoite,
        unidentified,
        ring,
        schizont,
        gametocyte,
        leukocyte,
    ):
        const = AppConstants()
        columnList = const.cell_microscopy_result_TableColumns()
        recordCreationTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        total_infection = (
            trophozoite + unidentified + ring + schizont + gametocyte + leukocyte
        )

        columnValues = [
            patient_id,
            name_of_image,
            infected,
            number_of_rbc,
            trophozoite,
            unidentified,
            ring,
            schizont,
            gametocyte,
            leukocyte,
            total_infection,
            recordCreationTime,
        ]

        dbConnect = DbConnect()

        dbConnect.createConnection()
        dbConnect.setSchema("mca")
        dbConnect.setTableName("cell_microscopy_result")

        dbConnect.insertRecord(columnList, columnValues)

        columnList = ["id"]
        conditions_dict = {"patient_id": patient_id, "name_of_image": name_of_image}
        id = dbConnect.fetchWithMultipleCondition(columnList, conditions_dict)[0]

        dbConnect.closeConnection()
        return (True, id[0], "Records Persisted.")

    def updateRecordToDB(
        self,
        image_id,
        infected,
        number_of_rbc,
        trophozoite,
        unidentified,
        ring,
        schizont,
        gametocyte,
        leukocyte,
    ):
        const = AppConstants()
        updateColumnList = const.cell_microscopy_result_TableColumns()[2:]
        recordUpdationTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        total_infection = (
            trophozoite + unidentified + ring + schizont + gametocyte + leukocyte
        )

        updateValues = [
            infected,
            number_of_rbc,
            trophozoite,
            unidentified,
            ring,
            schizont,
            gametocyte,
            leukocyte,
            total_infection,
            recordUpdationTime,
        ]

        dbConnect = DbConnect()

        dbConnect.createConnection()
        dbConnect.setSchema("mca")
        dbConnect.setTableName("cell_microscopy_result")

        primaryKey = "id"

        dbConnect.updateMultipleColumns(
            updateColumnList, updateValues, primaryKey, image_id
        )

        dbConnect.closeConnection()
        return (True, "Records Updated.")

    def getResult(
        self,
        cell_microscopy_result_id,
    ):
        const = AppConstants()
        dbConnect = DbConnect()
        dbConnect.createConnection()
        dbConnect.setSchema("mca")
        dbConnect.setTableName("cell_microscopy_result")

        columnList = const.cell_microscopy_result_TableColumns()
        primaryKey = "id"
        pkValue = cell_microscopy_result_id

        data_all = {}
        patient_data = {}
        result_data = {}

        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        result_data["patient_id"] = data[0]
        result_data["name_of_image"] = data[1]
        result_data["infection_status"] = data[2]
        result_data["number_of_rbc"] = data[3]
        result_data["trophozoite"] = data[4]
        result_data["unidentified"] = data[5]
        result_data["ring"] = data[6]
        result_data["schizont"] = data[7]
        result_data["gametocyte"] = data[8]
        result_data["leukocyte"] = data[9]
        result_data["total_infection"] = data[10]
        result_data["result_date"] = data[11]

        dbConnect.setSchema("mca")
        dbConnect.setTableName("patient")

        columnList = const.patient_TableColumns()
        primaryKey = "id"
        pkValue = result_data["patient_id"]

        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        patient_data["name"] = data[0]
        patient_data["email"] = data[1]
        patient_data["phone_number"] = data[2]
        patient_data["age"] = data[3]
        patient_data["address"] = data[4]
        patient_data["state"] = data[5]
        patient_data["pincode"] = data[6]

        dbConnect.closeConnection()

        data_all["patient_data"] = patient_data
        data_all["result_data"] = result_data
        return data_all
    
    def getAllResult(
        self,
        patient_id,
    ):
        const = AppConstants()
        dbConnect = DbConnect()
        dbConnect.createConnection()
        dbConnect.setSchema("mca")
        dbConnect.setTableName("cell_microscopy_result")

        columnList = const.cell_microscopy_result_TableColumns()
        columnList.insert(0,"id")
        primaryKey = "patient_id"
        pkValue = patient_id

        data_all = {}
        result_data = {}

        data_all = dbConnect.fetchMultiple(columnList, primaryKey, pkValue)

        for data in data_all:
            curr_data = {}
            curr_data["patient_id"] = data[1]
            curr_data["name_of_image"] = data[2]
            curr_data["infection_status"] = data[3]
            curr_data["number_of_rbc"] = data[4]
            curr_data["trophozoite"] = data[5]
            curr_data["unidentified"] = data[6]
            curr_data["ring"] = data[7]
            curr_data["schizont"] = data[8]
            curr_data["gametocyte"] = data[9]
            curr_data["leukocyte"] = data[10]
            curr_data["total_infection"] = data[11]
            curr_data["result_date"] = data[12]
            result_data[data[0]] = curr_data

        dbConnect.closeConnection()

        return result_data
    
    pass
