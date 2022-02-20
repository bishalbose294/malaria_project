import os
from app import app
from app.configUtil import ConfigConnect

if __name__ == "__main__":

    cwd = os.path.dirname(__file__)
    os.chdir(cwd)
    configParser = ConfigConnect()
    configParser.set_section_config("ROOT", "cwd", cwd)
    dict_values = configParser.get_section_config("flask")

    root = configParser.get_section_config("ROOT")["cwd"]
    images = configParser.get_section_config("DIR")["images_folder"]
    app.config["UPLOAD_FOLDER"] = os.path.join(root, images)

    host = dict_values["host"]
    port = dict_values["port"]
    
    templates_folder = configParser.get_section_config("dir")["templates_folder"]
    app.template_folder = os.path.join(root, templates_folder)

    static_folder = configParser.get_section_config("dir")["static_folder"]
    app.static_folder = os.path.join(root, static_folder)

    app.run(host=host, port=port)
