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
        self.__re_param_module_ioport = r"\s*module\s*\w+[\s\n\w:\*;]*#\(([.\s\w,\n\+\-\*\/`=\d[$\(\)']*)\)\s*\n*\(([.\s\w,:\d`\[\]\-\+\*\/\(\)]*)\);"
        self.__re_module_ioport = r"\s*module\s*\w+\s*\s*\(([.\s\w,:\d`\[\]\-\+\*\/]*)\);"
        self.__re_extract_ioport = r"[,\t ]*(?:input|output)[\t ]*(?:wire|)[\t ]*(?:\[([\w\d\s:\(\)\+\-\*\/`]+)\]|)[\t ]*(\w+)" # group(1): bitwidth; group(2): signal name
        self.__re_extract_param = r"[\t ]*(\w+)[\t ]*=[\t ]*([`\d\w\+\-\*\/\(\)$]+)" # group(1): parameter name; group(2): value
        self.module_name = ""
        self.io_lists = [] # one of io_lists: [macro, signal_name, signal_range]
        self.param_lists = [] # one of io_lists: [macro, param_name, signal_value]
    def parseModule(self, input_file):
        input_handler = open(input_file, 'r')
        input_str = remove_comments(input_handler.read())
        # self.__logging.debug(input_str)
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
            ioport_str = m_module_ioport.group(1)
        re_param_module_ioport = re.compile(self.__re_param_module_ioport)
        m_param_module_ioport = re_param_module_ioport.search(input_str)
        if(m_param_module_ioport is not None):
            param_str = m_param_module_ioport.group(1)
            ioport_str = m_param_module_ioport.group(2)
        else:
            param_str = ""
        self.get_io_lists(ioport_str)
        self.get_param_list(param_str)


    def get_param_list(self,param_str):
        param_list = param_str.split('\n')
        param_count = 0
        for index, line in enumerate(param_list):
            m_extract_param = re.compile(self.__re_extract_param).search(line)
            if(m_extract_param is not None):
                param_name = m_extract_param.group(1)
                param_value = m_extract_param.group(2)
                self.param_lists.append([None,param_name,param_value])
                param_count = param_count + 1
            else:
                if(line.strip() is not ""):
                    self.param_lists.append([line,None,None])
        self.__logging.debug("[DEBUG] Module parameter count: %d"%param_count)
    def get_io_lists(self, ioport_str):
        # Function: Get each IO item
        ioport_list = ioport_str.split('\n')
        io_count = 0
        for index, line in enumerate(ioport_list):
            m_extract_ioport = re.compile(self.__re_extract_ioport).search(line)
            if(m_extract_ioport is not None):
                if(m_extract_ioport.group(1) is not None):
                    signal_range = m_extract_ioport.group(1)
                else:
                    signal_range = ""
                io_signal_name = m_extract_ioport.group(2)
                self.io_lists.append([None,io_signal_name,signal_range])
                io_count = io_count + 1
            else:
                if(line.strip() is not ""):
                    self.io_lists.append([line,None,None])
        self.__logging.debug("[DEBUG] Module IO count: %d"%io_count)
    def instance_param_top(self):
        self_param_str = ""
        self_param_str += "#(\n"
        for param_list in self.param_lists:
            macro_str = param_list[0]
            param_name = param_list[1]
            param_value = param_list[2]
            try:
                if('`if' in macro_str or '`endif' in macro_str):
                    self_param_str += "  %s\n"%macro_str
            except:
                pass
            if(param_name is not None):
                self_param_str += "    parameter %40s = %s,\n"%(param_name,param_value)
        self_param_str += ")"
        return self_param_str
    def instance_param_empty(self):
        self_param_str = ""
        self_param_str += "#(\n"
        for param_list in self.param_lists:
            macro_str = param_list[0]
            param_name = param_list[1]
            param_value = param_list[2]
            try:
                if('`if' in macro_str or '`endif' in macro_str):
                    self_param_str += "  %s\n"%macro_str
            except:
                pass
            if(param_name is not None):
                self_param_str += "    .%s(),\n"%io_signal_str
        self_param_str += ")"
        return self_param_str
    def instance_param_self(self):
        self_param_str = ""
        self_param_str += "#(\n"
        for param_list in self.param_lists:
            macro_str = param_list[0]
            param_name = param_list[1]
            param_value = param_list[2]
            try:
                if('`if' in macro_str or '`endif' in macro_str):
                    self_param_str += "  %s\n"%macro_str
            except:
                pass
            if(param_name is not None):
                self_param_str += "    .%-40s%40s),\n"%("%s("%param_name,param_name)
        self_param_str += ")"
        return self_param_str
    def instance_module_empty(self,param_option):
        instance_str = ""
        instance_str += "%s i_%s\n"%(self.module_name,self.module_name.lower())
        # print(self.instance_param_self())
        instance_str += self.instance_param_self()
        instance_str += "(\n"
        for io_list in self.io_lists:
            macro_str = io_list[0]
            io_signal_str = io_list[1]
            io_range_str = io_list[2]
            try:
                if('`if' in macro_str or '`endif' in macro_str):
                    instance_str += " %s\n"%macro_str
            except:
                pass
            if(io_signal_str is not None):
                instance_str += " .%s(),\n"%io_signal_str
        instance_str += ");"
        self.__logging.debug("[DEBUG] Instance String\n%s"%instance_str)
    def instance_module_fill_self(self):
        instance_str = ""
        instance_str += "%s i_%s\n"%(self.module_name,self.module_name.lower())
        # print(self.instance_param_self())
        instance_str += self.instance_param_self()
        instance_str += "(\n"
        for io_list in self.io_lists:
            macro_str = io_list[0]
            io_signal_str = io_list[1]
            io_range_str = io_list[2]
            try:
                if('`if' in macro_str or '`endif' in macro_str):
                    instance_str += " %s\n"%macro_str
            except:
                pass
            if(io_signal_str is not None):
                instance_str += " .%-40s%40s),\n"%("%s("%io_signal_str,io_signal_str)
        instance_str += ");"
        instance_str = remove_last_comma(instance_str)
        self.__logging.debug("[DEBUG] Instance String\n%s"%instance_str)
        return instance_str
    def declare_wires(self):
        wire_declare_str = ""
        for io_list in self.io_lists:
            macro_str = io_list[0]
            io_signal_str = io_list[1]
            io_range_str = io_list[2]
            try:
                if('`if' in macro_str or '`endif' in macro_str):
                    wire_declare_str += " %s\n"%macro_str
            except:
                pass
            if(io_signal_str is not None):
                if(io_range_str is not ""):
                    wire_declare_str += " wire %-50s %s;\n"%("[%s]"%io_range_str,io_signal_str)
                else:
                    wire_declare_str += " wire %-50s %s;\n"%("",io_signal_str)
        # self.__logging.debug("[DEBUG] Wire Declaration String\n%s"%wire_declare_str)
        return wire_declare_str
   
def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)
def remove_last_comma(comma_str):
    return comma_str.rstrip(',')    