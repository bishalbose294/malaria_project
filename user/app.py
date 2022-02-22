import os
from app import app
from app.configUtil import ConfigConnect

if __name__ == "__main__":

    cwd = os.path.dirname(os.path.abspath(__file__))
    os.chdir(cwd)
    data = os.path.abspath(os.path.join(cwd, os.pardir))
    configParser = ConfigConnect()
    configParser.set_section_config("ROOT", "cwd", cwd)
    configParser.set_section_config("ROOT", "data", data)  # Addition
    configParser.set_section_config("admin", "isimpersonatingasuser", False)
    configParser.set_section_config("admin", "admin_username", None)
    configParser.set_section_config("admin", "admin_id", 0)

    dict_values = configParser.get_section_config("flask")

    # root = configParser.get_section_config("ROOT")["cwd"]
    data = configParser.get_section_config("ROOT")["data"]  # Addition
    images = configParser.get_section_config("DIR")["images_folder"]
    app.config["UPLOAD_FOLDER"] = os.path.join(data, images)

    host = dict_values["host"]
    port = dict_values["port"]

    static_folder = configParser.get_section_config("dir")["static_folder"]
    app.static_folder = os.path.join(data, static_folder)

    root = configParser.get_section_config("ROOT")["cwd"]
    templates_folder = configParser.get_section_config("dir")[
        "templates_folder"]
    app.template_folder = os.path.join(root, templates_folder)

    app.run(host=host, port=port)
