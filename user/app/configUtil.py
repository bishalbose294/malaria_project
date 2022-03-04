import configparser as cp
import os


class ConfigConnect:

    # Relative path for config file
    configFilePath = "configuration/config.cfg"

    # Initialization Parameters
    def __init__(
        self,
    ):
        self.config = cp.ConfigParser()
        self.config.read(ConfigConnect.configFilePath)

    # Method to fetch config values
    def get_section_config(self, sectionName):
        return dict(self.config.items(str(sectionName).upper()))

    # Method to set config values
    def set_section_config(self, sectionName, key, value):
        self.config.set(str(sectionName).upper(), str(key), str(value))
        with open(ConfigConnect.configFilePath, "w") as configfile:
            self.config.write(configfile)
