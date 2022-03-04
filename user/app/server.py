from datetime import datetime
from app.configUtil import ConfigConnect
from app.report import Report
from app import app
from flask import request, jsonify, send_file, render_template
import os
import traceback
from app.login import LoginUser
from app.register import RegisterUser
from app.results import Results
from app.mlProcess import MLProcess

# API to test 
@app.route("/test")
def testAPI():
    try:
        return "Hello, World! Test Successfull !"
    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        return {"ERROR": str(e), "status": False}

# API to load default page
@app.route('/')
def index():
    return render_template("login.html", registration_message="")

# API to Login user
@app.route("/login", methods=["POST"])
def loginAPI():
    try:
        content = request.form
        username = content["username"]
        password = content["password"]

        login = LoginUser()
        result = login.userLogin(username, password)

        if result[0]:
            # return jsonify({"status": status, "message": msg})

            id = int(result[1])
            patient_data = login.getUserDetails(id)

            isAdmin = login.isAdmin(id)
            if isAdmin:
                login.setImpersonatingAsUser(isAdmin, username, id)

            isimpersonatingasuser = login.isImpersonatingAsUser()

            return render_template("home.html", isAdmin=isAdmin, isimpersonatingasuser=isimpersonatingasuser, username=username, patient_id=result[1], patient_data=patient_data)
        else:
            # return jsonify({"status": status, "message": msg})
            return render_template("login.html", registration_message=" - "+result[2])

    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message=str(e))

# API to redirect user to Home after successful login or to error page otherwise
@app.route("/userHome", methods=["POST"])
def userHomeAPI():
    try:
        content = request.form

        login = LoginUser()
        id = int(content["id"])
        patient_data = login.getUserDetails(id)
        username = login.getUsername(id)

        isAdmin = login.isAdmin(id)
        isimpersonatingasuser = login.isImpersonatingAsUser()

        return render_template("home.html", isAdmin=isAdmin, isimpersonatingasuser=isimpersonatingasuser, username=username, patient_id=id, patient_data=patient_data)

    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message=str(e))

# API to reset password for user
@app.route("/resetPassword", methods=["POST"])
def resetPasswordAPI():
    try:
        content = request.form
        status = content["status"]
        username = content["username"]
        login = LoginUser()

        if status == "answers":
            security1 = content["security1"]
            security2 = content["security2"]
            security3 = content["security3"]
            result = login.verifySecurityDetails(
                username, security1, security2, security3)

            reset = result[0]
            status_message = result[1]
            return render_template("reset_password.html", reset=reset, status_message=status_message)
        else:
            password = content["password"]
            result = login.changePassword(username, password)
            reset = result[0]
            status_message = result[1]

            if reset:
                return render_template("login.html", registration_message=" - "+status_message)
            else:
                return render_template("reset_password.html", reset=reset, status_message=status_message)

    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message=str(e))

# API to update profile of user
@app.route("/updateProfile", methods=["POST"])
def updateProfileAPI():
    try:
        content = request.form
        id = content["patient_id"]
        email = content["email"]
        phone_number = content["phone_number"]
        dob = content["dob"]
        age = content["age"]
        marital_status = content["marital_status"]
        address = content["address"]
        state = content["state"]
        country = content["country"]
        pincode = content["pincode"]

        register = RegisterUser()

        register.updateUserDetails(
            id, email, phone_number, dob, age, marital_status, address, state, country, pincode,)

        login = LoginUser()
        patient_data = login.getUserDetails(int(id))
        username = login.getUsername(id)
        isAdmin = login.isAdmin(id)
        isimpersonatingasuser = login.isImpersonatingAsUser()
        return render_template("home.html", isAdmin=isAdmin, isimpersonatingasuser=isimpersonatingasuser, username=username, patient_id=id, patient_data=patient_data)

    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message=str(e))

# API to register patient for website
@app.route("/registerPatient", methods=["POST"])
def registerPatientAPI():
    try:
        content = request.form
        username = content["username"]
        password = content["password"]
        name = content["name"]
        email = content["email"]
        phone_number = content["phone_number"]
        dob = content["dob"]
        age = int(content["age"])
        marital_status = content["marital_status"]
        address = content["address"]
        state = content["state"]
        country = content["country"]
        pincode = int(content["pincode"])
        security1 = content["security1"]
        security2 = content["security2"]
        security3 = content["security3"]

        register = RegisterUser()

        result = register.registerPatientDetails(
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
        )

        if not result[0]:
            # return jsonify({"status" : result[0], "message": result[1]})
            return render_template("register.html", error_message=" - "+result[1])
        else:
            # return jsonify({"status": result[0], "id": result[1], "message": result[2]})
            return render_template("login.html", registration_message="Please login with newly registered username.")

    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message=str(e))

# API to upload a new sample to website
@app.route("/uploadNewSample", methods=["POST"])
def uploadNewSampleAPI():
    try:
        file = request.files["file"]
        content = request.form
        patient_id = content["patient_id"]
        name_of_image = file.filename
        processed = False
        infection_status = False
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
            processed,
            infection_status,
            number_of_rbc,
            trophozoite,
            unidentified,
            ring,
            schizont,
            gametocyte,
            leukocyte,
        )
        id = int(result[1])
        status_message = result[2]

        isNew = not res.isProcessed(id)
        data = res.getResult(id)
        data["result_data"]["id"] = id

        report = Report()
        reportGenerated = report.isReportGenerated(id)

        # return jsonify({"status": result[0], "id": result[1], "message": result[2]})

        imagePath = "images/"+str(name_of_image)

        login = LoginUser()
        isAdmin = login.isAdmin(patient_id)
        isimpersonatingasuser = login.isImpersonatingAsUser()

        return render_template("sample_details.html",  isAdmin=isAdmin, isimpersonatingasuser=isimpersonatingasuser, new_sample=isNew, data=data, imagePath=imagePath, status_message=status_message, reportGenerated=reportGenerated)
    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message=str(e))

# API to fetch all patient details
@app.route("/fetchAllPatients")
def fetchAllPatientsAPI():
    try:
        register = RegisterUser()
        patient_list = register.getAllUserDetails()
        return render_template("patient_listing.html", isAdmin=True, isimpersonatingasuser=True, patient_list=patient_list)
    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message=str(e))

# API to fetch specific result for a patient
@app.route("/fetchResult", methods=["POST"])
def fetchResultAPI():
    try:
        content = request.form
        id = int(content["id"])
        patient_id = int(content["patient_id"])
        result = Results()
        data = result.getResult(id)
        data["result_data"]["id"] = id

        isNew = not result.isProcessed(id)

        if isNew:
            imagePath = "images/"+str(data["result_data"]["name_of_image"])
            status_message = "Please Predict to generate Report."
        else:
            imagePath = "predicted/"+str(data["result_data"]["name_of_image"])
            status_message = "Click on Generate Report to make it available for Download."

        report = Report()
        reportGenerated = report.isReportGenerated(id)

        if reportGenerated:
            status_message = "Please Download Report to View"

        # return jsonify(
        #     {
        #         "status": True,
        #         "patient_data": data["patient_data"],
        #         "result_data": data["result_data"],
        #     }
        # )
        login = LoginUser()
        isAdmin = login.isAdmin(patient_id)
        isimpersonatingasuser = login.isImpersonatingAsUser()

        return render_template("sample_details.html", isAdmin=isAdmin, isimpersonatingasuser=isimpersonatingasuser, new_sample=isNew, data=data, imagePath=imagePath, status_message=status_message, reportGenerated=reportGenerated)
    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message=str(e))

# API to fetch all result for a patient
@app.route("/fetchAllResult", methods=["POST"])
def fetchAllResultAPI():
    try:
        content = request.form
        patientId = int(content["patient_id"])
        result = Results()
        all_results = result.getAllResult(patientId)

        # return jsonify(all_results)

        return render_template("sample_listing.html", patientId=patientId, all_results=all_results)

    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message=str(e))

# API to predict result for a new sample
@app.route("/predict", methods=["POST"])
def predictAPI():
    try:
        content = dict(request.form)
        id = int(content["id"])
        patient_id = int(content["patient_id"])

        res = Results()

        isNew = not res.isProcessed(id)

        if isNew:
            mlProcess = MLProcess()
            result = mlProcess.model_predict(id)
            status_message = result[1]
        else:
            status_message = "Prediction Exists. Fetching Predition."

        isNew = not res.isProcessed(id)

        name_of_image = res.getNameOfImage(id)

        data = res.getResult(id)
        data["result_data"]["id"] = id

        report = Report()
        reportGenerated = report.isReportGenerated(id)

        # return jsonify({"status": result[0], "message": result[1]})

        if isNew:
            imagePath = "images/"+str(name_of_image)
        else:
            imagePath = "predicted/"+str(name_of_image)

        login = LoginUser()
        isAdmin = login.isAdmin(patient_id)
        isimpersonatingasuser = login.isImpersonatingAsUser()

        return render_template("sample_details.html", isAdmin=isAdmin, isimpersonatingasuser=isimpersonatingasuser, new_sample=isNew, data=data, imagePath=imagePath, status_message=status_message, reportGenerated=reportGenerated)
    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message=str(e))

# API to generate report for a sample
@app.route("/generateReport", methods=["POST"])
def generateReportAPI():
    try:
        content = request.form
        id = int(content["id"])
        patient_id = int(content["patient_id"])

        report = Report()
        reportGenerated = report.isReportGenerated(id)

        if not reportGenerated:
            result = report.generateReport(id)
            status_message = result[1]
            reportGenerated = True
        else:
            status_message = "Report Already Generated, Fetching the download Link."

        res = Results()
        data = res.getResult(id)
        data["result_data"]["id"] = id
        isNew = not res.isProcessed(id)

        imagePath = "predicted/"+str(data["result_data"]["name_of_image"])

        # return jsonify({"status": result[0], "message": result[1]})

        login = LoginUser()
        isAdmin = login.isAdmin(patient_id)
        isimpersonatingasuser = login.isImpersonatingAsUser()

        return render_template("sample_details.html", isAdmin=isAdmin, isimpersonatingasuser=isimpersonatingasuser, new_sample=isNew, data=data, imagePath=imagePath, status_message=status_message, reportGenerated=reportGenerated)
    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message=str(e))

# API to download generated report
@app.route("/downloadReport", methods=["POST"])
def downloadReportAPI():
    try:
        content = request.form
        id = int(content["id"])

        # Class to Connect to Config File
        config = ConfigConnect()

        # Fetching configuration Data
        data = config.get_section_config("ROOT")["data"]

        # Fetching configuration Data
        report_folder = config.get_section_config("DIR")["report_folder"]
        report = Report()
        file_name = report.getReportName(id)
        attachment_filename = "report_"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".pdf"
        abs_path = os.path.join(data, report_folder, file_name)
        if not os.path.exists(abs_path):
            return jsonify({"status": False, "message": "No such report Exists."})
        return send_file(abs_path, attachment_filename=attachment_filename)
    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message=str(e))


# API to logout from website
@app.route('/logout')
def logoutAPI():

    # Class to Connect to Config File
    config = ConfigConnect()

    # Setting configuration Data
    config.set_section_config("admin", "isimpersonatingasuser", False)

    # Setting configuration Data
    config.set_section_config("admin", "admin_username", None)

    # Setting configuration Data
    config.set_section_config("admin", "admin_id", 0)
    return render_template("login.html", registration_message="")

################################################################ Navigation API #########################################

# API to navigate to edit profile page
@app.route("/navigateToEditProfile", methods=["POST"])
def navigateToEditProfileAPI():
    try:
        content = request.form
        id = content["patient_id"]
        login = LoginUser()

        patient_data = login.getUserDetails(int(id))

        return render_template("edit_details.html", patient_id=id, patient_data=patient_data)

    except Exception as e:
        traceback.print_exc()
        print("ERROR = " + str(e))
        # return {"ERROR": str(e), "status": False}
        return render_template("error.html", error_message=str(e))

# API to navigate to registration page
@app.route("/navigateToRegistrationPage")
def navigateToRegistrationPageAPI():
    return render_template("register.html", error_message="")

# API to navigate to password reset page
@app.route("/navigateToPasswordResetPage")
def navigateToPasswordResetPageAPI():
    return render_template("reset_password.html", reset=False, status_message="")

# API to navigate to user home
@app.route("/navigateToHome", methods=["POST"])
def navigateToHomeAPI():
    content = request.form
    patient_id = content["patient_id"]
    patient_id = int(patient_id)
    login = LoginUser()
    username = login.getUsername(patient_id)
    patient_data = login.getUserDetails(patient_id)
    isAdmin = login.isAdmin(patient_id)
    isimpersonatingasuser = login.isImpersonatingAsUser()
    return render_template("home.html", isAdmin=isAdmin, isimpersonatingasuser=isimpersonatingasuser, username=username, patient_id=patient_id, patient_data=patient_data)

# API to navigate to Admin home
@app.route("/navigateToAdminHome")
def navigateToAdminHomeAPI():

    # Class to Connect to Config File
    config = ConfigConnect()

    # Fetching configuration Data
    dict_values = config.get_section_config("admin")
    username = dict_values["admin_username"]
    patient_id = int(dict_values["admin_id"])
    login = LoginUser()
    patient_data = login.getUserDetails(patient_id)
    return render_template("home.html", isAdmin=True, isimpersonatingasuser=True, username=username, patient_id=patient_id, patient_data=patient_data)

# API to navigate to listing page
@app.route("/navigateToListingPage", methods=["POST"])
def navigateToListingPageAPI():
    content = request.form
    patientId = int(content["patient_id"])
    result = Results()
    all_results = result.getAllResult(patientId)

    # return jsonify(all_results)

    return render_template("sample_listing.html", patientId=patientId, all_results=all_results)
