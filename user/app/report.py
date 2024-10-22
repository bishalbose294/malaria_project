import pdfkit
from app.dbUtil import DbConnect
from app.results import Results
from app.configUtil import ConfigConnect
import os
from datetime import datetime
from configuration.contstants import AppConstants

# Class to generate Reports
class Report:

    # Method to check if report is generated
    def isReportGenerated(
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
        dbConnect.setTableName("report")

        columnName = "cell_microscopy_result_id"
        columnValue = cell_microscopy_result_id
        existance = dbConnect.chechExistance(columnName, columnValue)

        # Close the Connection
        dbConnect.closeConnection()
        return existance

    # Method to save report to database
    def __save_report_to_db(
        self,
        cell_microscopy_result_id,
        filename,
    ):
        # Class for Project Constants
        const = AppConstants()
        recordCreationTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Retrieve table columns from Constants File
        columnList = const.report_TableColumns()
        columnValues = [cell_microscopy_result_id,
                        filename, recordCreationTime]

        # Class to create Database Connection
        dbConnect = DbConnect()

        # Connect to Database
        dbConnect.createConnection()

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("report")
        dbConnect.insertRecord(columnList, columnValues)

        # Close the Connection
        dbConnect.closeConnection()


    # Method to retrieve report name
    def getReportName(
        self,
        cell_microscopy_result_id,
    ):

        # Columns to be fetched from table
        columnList = ["report_filename"]

        # Defining the Primary Key for condition
        primaryKey = "cell_microscopy_result_id"

        # Defining the Primary Key Value
        pkValue = cell_microscopy_result_id

        # Class to create Database Connection
        dbConnect = DbConnect()

        # Connect to Database
        dbConnect.createConnection()

        # Connect to specified Schema
        dbConnect.setSchema("mca")

        # Connect to specified Table
        dbConnect.setTableName("report")

        # Fetch Data from Database
        row = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        # Close the Connection
        dbConnect.closeConnection()
        return row[0]


    # Method to generate a new report.
    def generateReport(
        self,
        cell_microscopy_result_id,
    ):

        # Class to Connect to Config File
        config = ConfigConnect()

        result = Results()
        data_all = result.getResult(cell_microscopy_result_id)

        patient_data = data_all["patient_data"]
        result_data = data_all["result_data"]

        # Fetching configuration Data
        root = config.get_section_config("ROOT")["cwd"]

        # Fetching configuration Data
        data = config.get_section_config("ROOT")["data"]

        # Fetching configuration Data
        dict_values = config.get_section_config("DIR")
        raw_image_folder = dict_values["images_folder"]
        predicted_image_folder = dict_values["predicted_images_folder"]
        report_folder = dict_values["report_folder"]
        name_of_pdf_report = str(cell_microscopy_result_id) + "_report.pdf"
        css_file_folder = dict_values["css_folder"]

        # Fetching configuration Data
        css_file = config.get_section_config("FILE")["css"]

        raw_image_path = os.path.join(
            data,
            raw_image_folder,
            result_data["name_of_image"],
        )
        predicted_image_path = os.path.join(
            data,
            predicted_image_folder,
            result_data["name_of_image"],
        )
        pdf_report_path = os.path.join(
            data,
            report_folder,
            name_of_pdf_report,
        )

        css_path = os.path.join(
            root,
            css_file_folder,
            css_file,
        )

        page_title_text = "Malaria Report"

        html = f"""
            <html>
                <head>
                    <title>{page_title_text}</title>
                    <link rel="stylesheet" href="{css_path}">
                </head>
                <body>
                <center>
                    <h1> Smart Malaria Detection </h1>
                    <h5>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
                        - AI system to Detect & Classify Malaria Viruses from Blood Sample Images</h5>
                </center>
                    <br /><br /><br />
                    <h2 align="center">{page_title_text}</h2>
                    <br /><br /><br />
                    <table align="center">
                        <tr>
                            <td style="vertical-align: top; width:200px">
                                <h2 align="center">Patient Details</h2>
                                <table class="styled-table">
                                <tr>
                                    <td>
                                        Name:
                                    </td>
                                    <td>
                                        { patient_data["name"] }
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        Email:
                                    </td>
                                    <td>
                                        { patient_data["email"] }
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        Phone Number:
                                    </td>
                                    <td>
                                        { patient_data["phone_number"] }
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        DOB:
                                    </td>
                                    <td>
                                        { patient_data["dob"] }
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        Age:
                                    </td>
                                    <td>
                                        { patient_data["age"] }
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        Marital Status:
                                    </td>
                                    <td>
                                        { patient_data["marital_status"] }
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        Address:
                                    </td>
                                    <td>
                                        { patient_data["address"] }
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        State:
                                    </td>
                                    <td>
                                        { patient_data["state"] }
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        Country:
                                    </td>
                                    <td>
                                        { patient_data["country"] }
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        Pincode:
                                    </td>
                                    <td>
                                        { patient_data["pincode"] }
                                    </td>
                                </tr>
                            </table>
                            </td>
                            <td style="vertical-align: top; width:150px">
                                <h2 align="center">Infection Status</h2>
                                <table class="styled-table">
                                    <tr>
                                        <td>Infected:</td>
                                        <td>{result_data["infection_status"]}</td>
                                    </tr>
                                    <tr>
                                        <td>RBC #:</td>
                                        <td>{result_data["number_of_rbc"]}</td>
                                    </tr>
                                    <tr>
                                        <td>Trophozoite:</td>
                                        <td>{result_data["trophozoite"]}</td>
                                    </tr>
                                    <tr>
                                        <td>Ring:</td>
                                        <td>{result_data["ring"]}</td>
                                    </tr>
                                    <tr>
                                        <td>Schizont:</td>
                                        <td>{result_data["schizont"]}</td>
                                    </tr>
                                    <tr>
                                        <td>Gametocyte:</td>
                                        <td>{result_data["gametocyte"]}</td>
                                    </tr>
                                    <tr>
                                        <td>Leukocyte:</td>
                                        <td>{result_data["leukocyte"]}</td>
                                    </tr>
                                    <tr>
                                        <td>Unidentified:</td>
                                        <td>{result_data["unidentified"]}</td>
                                    </tr>
                                    <tr>
                                        <td>Total Infected Cells:</td>
                                        <td>{result_data["total_infection"]}</td>
                                    </tr>
                                    <tr>
                                        <td>Sample Date:</td>
                                        <td>{result_data["upload_date"]}</td>
                                    </tr>
                                    <tr>
                                        <td>Result Date:</td>
                                        <td>{result_data["processing_date"]}</td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <table align="center">
                                    <tr>
                                        <td><h3>Original Sample:</h3></td>
                                    </tr>
                                    <tr>
                                        <td><img src="{raw_image_path}" /></td>
                                    </tr>
                                </table>
                            </td>
                            <td>
                                <table align="center">
                                    <tr>
                                        <td><h3>Processed Sample:</h3></td>
                                    </tr>
                                    <tr>
                                        <td><img src="{predicted_image_path}" /></td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </body>
            </html>
            """
        options = {
            "enable-local-file-access": None,
            "page-size": "A4",
            "encoding": "UTF-8",
        }

        pdfkit.from_string(
            input=html,
            output_path=pdf_report_path,
            options=options,
            css=css_path,
        )

        self.__save_report_to_db(cell_microscopy_result_id, name_of_pdf_report)
        return (True, "Report Generated and Saved. Please download to view.")

    pass
