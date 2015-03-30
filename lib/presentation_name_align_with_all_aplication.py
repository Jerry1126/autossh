'''
Created on Sep 23, 2014

@author: danting
'''

import os
import sys
import xml.etree.ElementTree as et
import tempfile
import shutil

class presentation_name_align_with_all_aplication:
    def get_Adaptation_RBFolderName(self,ss_name,koala_input_xml):

        tree = et.parse(koala_input_xml)
        root = tree.getroot()

        if root.tag == "Adaptation":
            if(root.get("RBFolderName")):
                RBFolderName_AD = root.get("RBFolderName")
            else:
                nodes = root.getchildren()
                for node in nodes:
                    if node.tag == "Release":
                        secondnodes = node.getchildren()
                        for secondnode in secondnodes:
                            if secondnode.tag == "Vendor":
                                string = secondnode.text
                            elif secondnode.tag == "Element":
                                string = string + " " + secondnode.text
                            elif secondnode.tag == "Version":
                                Ver = secondnode.text.split(";")[0]
                                string = string + " " + Ver
                RBFolderName_AD = string
        return RBFolderName_AD

    def get_Database_RBFolderName(self,sql_result):
        count=0
        sql_result_list1=sql_result.split(")")[0].split("\n")
        for element in sql_result_list1:
            count=count+1
            if element.find("description"):
                break
        sql_result_list2=sql_result.split(")")[1].split(",")
        RBFolderName_DB=sql_result_list2[count]
        return RBFolderName_DB

    def make_dir(self):
        path=tempfile.mkdtemp()
        xml_path = path+os.path.sep+"koala.xml"
        return xml_path

    def remove_dir(self,xml_path):
        os.remove(xml_path)


