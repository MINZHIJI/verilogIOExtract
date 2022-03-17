import logging
import json
import verilogIOExtract
import json

class verilogIntegrate():
    """
    Class Name: verilogIntegrate
    Class Description:
        Integrate modules to target module
    """
    def __init__(self):
        self.__logging = logging.getLogger(__name__)
        self.__logging.setLevel(logging.DEBUG)
        self.integrated_module_name = ""
    def instance_module(self,input_file):
        module_dict = self.load_json(input_file)
        self.integrated_module_name = module_dict['module_name']
        vlogIOExtract = verilogIOExtract.verilogIOExtract()
        for verilog_file_dict in module_dict['instance_list']:
            input_verilog_file = verilog_file_dict["module_path"]
            vlogIOExtract.parseModule(input_verilog_file)
    def load_json(self,input_file):
        try:
            file_handler = open(input_file, 'r')
            return json.load(file_handler)
        except Exception as e:
            self.__logging.error("[ERROR] Load json file failed(%s)"%e)
            exit()