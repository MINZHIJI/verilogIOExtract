import sys
import os
import re
import logging
import string
import json

class verilogIOExtract():
    """
    Class Name: verilogIOExtract
    Class Description:
        Extract module IO port
    """
    def __init__(self):
        self.__logging = logging.getLogger(__name__)
        self.__logging.setLevel(logging.DEBUG)
        self.__re_module_name = r"\s*module\s*(\w+)"
        self.__re_param_module_ioport = r"\s*module\s*\w*\s*#\((.*)\)\s*\(([.\s\w,:\d`\[\]\-\+\*\/]*)\);"
        self.__re_module_ioport = r"\s*module\s*\w*\s*\s*\(([.\s\w,:\d`\[\]\-\+\*\/]*)\);"
        self.module_name = ""
    def parseModule(self, input_file):
        input_handler = open(input_file, 'r')
        input_str = input_handler.read()
        # Function: Find module name
        re_module_name = re.compile(self.__re_module_name)
        m_module_name = re_module_name.search(input_str)
        if(m_module_name is not None):
            self.module_name = m_module_name.group(1)
            self.__logging.debug("[DEBUG] Module name: %s"%self.module_name)
        else:
            self.__logging.error("[ERROR] Syntax error. Not found module name.")

        # Function: Find IO port (support parameterized module)
        re_module_ioport = re.compile(self.__re_module_ioport)
        m_module_ioport = re_module_ioport.search(input_str)
        if(m_module_ioport is not None):
            print(m_module_ioport.group(1))
        re_param_module_ioport = re.compile(self.__re_param_module_ioport)
        m_param_module_ioport = re_param_module_ioport.search(input_str)
        if(m_param_module_ioport is not None):
            print(m_param_module_ioport.group(1))
            print(m_param_module_ioport.group(2))