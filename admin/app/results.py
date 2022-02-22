from datetime import datetime
from app.dbUtil import DbConnect
from configuration.contstants import AppConstants


class Results:
    def saveImageToFolder(
        self,
    ):
        pass

    def persistDataToDB(
        self,
        patient_id,
        name_of_image,
        processed,
        infection_status,
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
        retrain = False

        columnList.remove("processing_date")

        total_infection = (
            trophozoite + unidentified + ring + schizont + gametocyte + leukocyte
        )

        columnValues = [
            patient_id,
            name_of_image,
            processed,
            infection_status,
            number_of_rbc,
            trophozoite,
            unidentified,
            ring,
            schizont,
            gametocyte,
            leukocyte,
            total_infection,
            recordCreationTime,
            retrain,
        ]

        dbConnect = DbConnect()

        dbConnect.createConnection()
        dbConnect.setSchema("mca")
        dbConnect.setTableName("cell_microscopy_result")

        dbConnect.insertRecord(columnList, columnValues)

        columnList = ["id"]
        conditions_dict = {"patient_id": patient_id,
                           "name_of_image": name_of_image}
        id = dbConnect.fetchWithMultipleCondition(
            columnList, conditions_dict)[0]

        dbConnect.closeConnection()
        return (True, id[0], "File Successfully Uploaded and Persisted.")

    def updateRecordToDB(
        self,
        cell_microscopy_result_id,
        infection_status,
        number_of_rbc,
        trophozoite,
        unidentified,
        ring,
        schizont,
        gametocyte,
        leukocyte,
    ):
        const = AppConstants()
        updateColumnList = const.cell_microscopy_result_TableColumns()
        recordUpdationTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        updateColumnList.remove("patient_id")
        updateColumnList.remove("name_of_image")
        updateColumnList.remove("upload_date")
        updateColumnList.remove("retrain")

        processed = True

        total_infection = (
            trophozoite + unidentified + ring + schizont + gametocyte + leukocyte
        )

        updateValues = [
            processed,
            infection_status,
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
            updateColumnList, updateValues, primaryKey, cell_microscopy_result_id
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

        for i in range(len(columnList)):
            result_data[columnList[i]] = data[i]

        dbConnect.setSchema("mca")
        dbConnect.setTableName("patient")

        columnList = const.patient_TableColumns()
        primaryKey = "id"
        pkValue = result_data["patient_id"]

        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        for i in range(len(columnList)):
            patient_data[columnList[i]] = data[i]

        dbConnect.closeConnection()

        data_all["patient_data"] = patient_data
        data_all["result_data"] = result_data
        return data_all

    def getAllResult(
        self,
        patient_id,
    ):
        dbConnect = DbConnect()
        dbConnect.createConnection()
        dbConnect.setSchema("mca")
        dbConnect.setTableName("cell_microscopy_result")

        columnList = ["id", "upload_date"]
        primaryKey = "patient_id"
        pkValue = patient_id

        data_all = {}
        result_data = {}

        data_all = dbConnect.fetchMultiple(
            columnList, primaryKey, pkValue, "id")

        for data in data_all:
            result_data[data[0]] = data[1]

        dbConnect.closeConnection()

        return result_data

    def isProcessed(
        self,
        cell_microscopy_result_id,
    ):
        dbConnect = DbConnect()

        dbConnect.createConnection()
        dbConnect.setSchema("mca")
        dbConnect.setTableName("cell_microscopy_result")

        columnList = ["processed"]
        primaryKey = "id"
        pkValue = cell_microscopy_result_id

        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        dbConnect.closeConnection()

        return data[0]

    def getNameOfImage(
        self,
        cell_microscopy_result_id,
    ):
        dbConnect = DbConnect()
        dbConnect.createConnection()
        dbConnect.setSchema("mca")
        dbConnect.setTableName("cell_microscopy_result")

        columnList = ["name_of_image"]
        primaryKey = "id"
        pkValue = cell_microscopy_result_id

        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        dbConnect.closeConnection()

        return data[0]
    pass
