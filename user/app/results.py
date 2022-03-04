from datetime import datetime
from app.dbUtil import DbConnect
from configuration.contstants import AppConstants

# Class to generate results from predictions
class Results:

    # Method to save results into database
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
        # Class for Project Constants
        const = AppConstants()

        # Retrieve table columns from Constants File
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

        # Class to create Database Connection
        dbConnect = DbConnect()


        # Connect to Database
        dbConnect.createConnection()

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("cell_microscopy_result")

        dbConnect.insertRecord(columnList, columnValues)

        # Columns to be fetched from table
        columnList = ["id"]
        conditions_dict = {"patient_id": patient_id,
                           "name_of_image": name_of_image}
        
        # Fetch Data from Database
        id = dbConnect.fetchWithMultipleCondition(
            columnList, conditions_dict)[0]

        # Close the Connection
        dbConnect.closeConnection()
        return (True, id[0], "File Successfully Uploaded and Persisted.")


    # Method to update results into database
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
        # Class for Project Constants
        const = AppConstants()

        # Retrieve table columns from Constants File
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

        # Class to create Database Connection
        dbConnect = DbConnect()

        # Connect to Database
        dbConnect.createConnection()

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("cell_microscopy_result")

        # Defining the Primary Key for condition
        primaryKey = "id"

        dbConnect.updateMultipleColumns(
            updateColumnList, updateValues, primaryKey, cell_microscopy_result_id
        )

        # Close the Connection
        dbConnect.closeConnection()
        return (True, "Records Updated.")


    # Method to retrieve the result form database
    def getResult(
        self,
        cell_microscopy_result_id,
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
        dbConnect.setTableName("cell_microscopy_result")

        # Retrieve table columns from Constants File
        columnList = const.cell_microscopy_result_TableColumns()
        primaryKey = "id"

        # Defining the Primary Key Value
        pkValue = cell_microscopy_result_id

        data_all = {}
        patient_data = {}
        result_data = {}

        # Fetch Data from Database
        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        for i in range(len(columnList)):
            result_data[columnList[i]] = data[i]

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("patient")

        # Retrieve table columns from Constants File
        columnList = const.patient_TableColumns()

        # Defining the Primary Key for condition
        primaryKey = "id"

        # Defining the Primary Key Value
        pkValue = result_data["patient_id"]

        # Fetch Data from Database
        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        for i in range(len(columnList)):
            patient_data[columnList[i]] = data[i]

        # Close the Connection
        dbConnect.closeConnection()

        data_all["patient_data"] = patient_data
        data_all["result_data"] = result_data
        return data_all


    # Method to get all results for a user from database
    def getAllResult(
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
        dbConnect.setTableName("cell_microscopy_result")

        # Columns to be fetched from table
        columnList = ["id", "upload_date"]

        # Defining the Primary Key for condition
        primaryKey = "patient_id"

        # Defining the Primary Key Value
        pkValue = patient_id

        data_all = {}
        result_data = {}

        # Fetch Data from Database
        data_all = dbConnect.fetchMultiple(
            columnList, primaryKey, pkValue, "id")

        for data in data_all:
            result_data[data[0]] = data[1]

        # Close the Connection
        dbConnect.closeConnection()

        return result_data

    # Method to verfify if a sample is processed
    def isProcessed(
        self,
        cell_microscopy_result_id,
    ):

        # Class to create Database Connection
        dbConnect = DbConnect()

        # Connect to Database
        dbConnect.createConnection()

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("cell_microscopy_result")

        # Columns to be fetched from table
        columnList = ["processed"]

        # Defining the Primary Key for condition
        primaryKey = "id"

        # Defining the Primary Key Value
        pkValue = cell_microscopy_result_id

        # Fetch Data from Database
        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        # Close the Connection
        dbConnect.closeConnection()

        return data[0]


    # Method to retrieve the name of an image
    def getNameOfImage(
        self,
        cell_microscopy_result_id,
    ):
        # Class to create Database Connection
        dbConnect = DbConnect()

        # Connect to Database
        dbConnect.createConnection()

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("cell_microscopy_result")

        # Columns to be fetched from table
        columnList = ["name_of_image"]

        # Defining the Primary Key for condition
        primaryKey = "id"

        # Defining the Primary Key Value
        pkValue = cell_microscopy_result_id

        # Fetch Data from Database
        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        # Close the Connection
        dbConnect.closeConnection()

        return data[0]
    pass
