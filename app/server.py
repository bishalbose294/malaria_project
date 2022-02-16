from app.configUtil import ConfigConnect
from app.report import Report
from app.dbUtil import DbConnect
from configuration.contstants import AppConstants
from app import app
from flask import request, jsonify, send_file, render_template
import os
import traceback
from app.login import LoginUser
from app.register import RegisterUser
from app.results import Results
from app.mlProcess import MLProcess


@app.route("/test")
def testAPI():
    try:
        return "Hello, World! Test Successfull !"
    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        return {"ERROR": str(e), "status": False}


@app.route('/')
def home():
    return render_template("login.html", registration_message="")

@app.route("/login", methods=["POST"])
def loginAPI():
    try:
        content = request.form
        username = content["username"]
        password = content["password"]

        login = LoginUser()
        result = login.userLogin(username, password)

        if result[0]:
            #return jsonify({"status": status, "message": msg})
            return render_template("home.html", username = username, patient_id=result[1]) 
        else:
            #return jsonify({"status": status, "message": msg})
            return render_template("login.html", registration_message = " - "+result[2]) 

    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        #return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message = str(e)) 

@app.route("/navigateToRegistrationPage")
def navigateToRegistrationPageAPI():
    return render_template("register.html", error_message="")

@app.route("/registerPatient", methods=["POST"])
def registerPatientAPI():
    try:
        content = request.form
        username = content["username"]
        password = content["password"]
        name = content["name"]
        email = content["email"]
        phone_number = content["phone_number"]
        age = int(content["age"])
        address = content["address"]
        state = content["state"]
        pincode = int(content["pincode"])

        register = RegisterUser()

        result = register.registerPatientDetails(
            username,password, name, email, phone_number, age, address, state, pincode
        )

        if not result[0]:
            # return jsonify({"status" : result[0], "message": result[1]})
            return render_template("register.html", error_message = " - "+result[1]) 
        else:
            # return jsonify({"status": result[0], "id": result[1], "message": result[2]})
            return render_template("login.html", registration_message="Please login with the registered username.")

    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message = str(e)) 


@app.route("/uploadNewSample", methods=["POST"])
def uploadNewSampleAPI():
    try:
        file = request.files["file"]
        content = request.form
        patient_id = content["patient_id"]
        name_of_image = file.filename
        infected = False
        number_of_rbc = 0
        trophozoite = 0
        unidentified = 0
        ring = 0
        schizont = 0
        gametocyte = 0
        leukocyte = 0

        imagePath = os.path.join(app.config["UPLOAD_FOLDER"], name_of_image)
        file.save(imagePath)

        res = Results()
        result = res.persistDataToDB(
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
        )
        return jsonify({"status": result[0], "id": result[1], "message": result[2]})
    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message = str(e))



@app.route("/fetchPatientDetails", methods=["POST"])
def fetchPatientAPI():
    try:
        content = dict(request.get_json())
        keys = [x.lower() for x in list(content.keys())]
        columnName = None
        columnValue = None

        if str("id") in keys:
            columnName = "id"
            columnValue = content[columnName]
        elif str("email") in keys:
            columnName = "email"
            columnValue = content[columnName]
        elif str("phone_number") in keys:
            columnName = "phone_number"
            columnValue = content[columnName]
        else:
            return jsonify(
                {
                    "status": False,
                    "message": "Please provide ID or Email or Phone to fetch user.",
                }
            )

        dbConnect = DbConnect()
        dbConnect.createConnection()
        dbConnect.setSchema("mca")
        dbConnect.setTableName("patient")

        const = AppConstants()
        columnList = const.patient_TableColumns()

        result = dbConnect.fetchOne(columnList, columnName, columnValue)

        dbConnect.closeConnection()

        if result is None or len(result) == 0:
            return jsonify(
                {"status": False, "message": "No user found with specified details"}
            )

        data = dict()

        for i in range(0, len(columnList)):
            data[columnList[i]] = result[i]

        return jsonify(data)
    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message = str(e))

@app.route("/fetchResult", methods=["POST"])
def fetchResultAPI():
    try:
        content = request.get_json()
        id = int(content["id"])
        result = Results()
        data = result.getResult(id)
        data["result_details"].pop("patient_id")
        data["result_details"].pop("name_of_image")
        return jsonify(
            {
                "status": True,
                "patient_details": data["patient_details"],
                "result_details": data["result_details"],
            }
        )
    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message = str(e))


@app.route("/fetchAllResult", methods=["POST"])
def fetchAllResultAPI():
    try:
        content = request.get_json()
        patientId = int(content["patientId"])
        result = Results()
        all_results = result.getAllResult(patientId)
        return jsonify(all_results)
    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message = str(e))

@app.route("/predict", methods=["POST"])
def predictAPI():
    try:
        content = dict(request.get_json())
        id = int(content["id"])
        mlProcess = MLProcess()
        result = mlProcess.model_predict(id)
        return jsonify({"status": result[0], "message": result[1]})
    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message = str(e))



@app.route("/generateReport", methods=["POST"])
def generateReportAPI():
    try:
        content = request.get_json()
        id = int(content["id"])
        report = Report()
        result = report.generateReport(id)
        return jsonify({"status": result[0], "message": result[1]})
    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message = str(e))



@app.route("/downloadReport", methods=["POST"])
def downloadReportAPI():
    try:
        content = request.get_json()
        id = int(content["id"])
        config = ConfigConnect()
        root = config.get_section_config("ROOT")["cwd"]
        report_folder = config.get_section_config("DIR")["report_folder"]
        file_name = str(id)+"_report.pdf"
        abs_path = os.path.join(root,report_folder,file_name)
        if not os.path.exists(abs_path):
            return jsonify({"status" : False, "message" : "No such report Exists."})
        return send_file(abs_path, attachment_filename='report.pdf')
    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message = str(e))