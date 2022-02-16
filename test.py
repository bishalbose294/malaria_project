from app.configUtil import ConfigConnect
import os

id = 1
config = ConfigConnect()
root = "d:/Softwares & Others/Development Softwares/Python/VSCodeWorkspace/MCAProject"
report_folder = "data/report"
file_name = str(id)+"_report.pdf"
abs_path = os.path.join(root,report_folder,file_name)
print(abs_path)
print(os.path.exists(abs_path))