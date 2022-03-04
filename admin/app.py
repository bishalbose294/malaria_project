import os
from app import app
from app.configUtil import ConfigConnect


# To start Flask Server execute this file using command python3 app.py in command line.
if __name__ == "__main__":

    # Get current working directory
    cwd = os.path.dirname(os.path.abspath(__file__))

    # Change working directory to current folder
    os.chdir(cwd)

    # Get parent of current working directory for DATA
    data = os.path.abspath(os.path.join(cwd, os.pardir))

    # Update all required parameters in CONFIG file
    # Class to Connect to Config File
    config = ConfigConnect()

    # Setting configuration Data
    config.set_section_config("ROOT", "cwd", cwd)

    # Setting configuration Data
    config.set_section_config("ROOT", "data", data)

    # Setting configuration Data
    config.set_section_config("admin", "isimpersonatingasuser", False)

    # Setting configuration Data
    config.set_section_config("admin", "admin_username", None)

    # Setting configuration Data
    config.set_section_config("admin", "admin_id", 0)

    # Fetching configuration Data
    dict_values = config.get_section_config("flask")

    # Fetching configuration Data
    data = config.get_section_config("ROOT")["data"]

    # Fetching configuration Data
    images = config.get_section_config("DIR")["images_folder"]

    # Set upload folder for Flask server
    app.config["UPLOAD_FOLDER"] = os.path.join(data, images)

    # Set the host and port from CONFIG file
    host = dict_values["host"]
    port = dict_values["port"]

    # Set the static folder for Flask Server
    static_folder = config.get_section_config("dir")["static_folder"]
    app.static_folder = os.path.join(data, static_folder)

    # Set the template / UI folder for Flask Server
    # Fetching configuration Data
    root = config.get_section_config("ROOT")["cwd"]

    # Fetching configuration Data
    templates_folder = config.get_section_config("dir")[
        "templates_folder"]
    app.template_folder = os.path.join(root, templates_folder)

    # To run the server on specified HOST and PORT
    app.run(host=host, port=port)
