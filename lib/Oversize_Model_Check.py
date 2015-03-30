'''
Created on Oct 21, 2014

@author: danting
'''

import os,sys
import tempfile
import shutil
import xml.etree.ElementTree as et
class Oversize_Model_Check:

    def get_lower(self,string):
        string = string.lower()
        return string

    def get_koala_xml_path(self,ss_name):
        koala_input_path="metadata"
        ss_name_upper=ss_name.upper()
        xml_file=ss_name+"Koala.xml"
        
        koala_xml_path = "%s%s%s%s%s%s%s" % (os.path.dirname(os.path.dirname(__file__)), os.path.sep, koala_input_path, os.path.sep, ss_name_upper, os.path.sep, xml_file)

        return koala_xml_path

    def get_measurement_dic(self,koala_xml_path):
        Measurement_dic = {} #store the Measurement
        
        tree =  et.parse(koala_xml_path)
        root = tree.getroot()
        nodes = root.getchildren()
        for node in nodes:
            if node.tag == "Adaptation" : 
                nodes=node.getchildren()

        #get the value and store them into dictionary which will also be stored in a list finally.
        for node in nodes:
            if node.tag == "Measurement":
                if node.get("OverSize")!= None and node.get("SubMeasName") != None:
                    ID = node.get("ID")
                    print ID
                    Value_list=[]
                    Value1 = node.get("OverSize")
                    if Value1=="true" or Value1=="True":
                        Value1='1'
                    Value2 = node.get("SubMeasName")
                    Value_list.append(Value1)
                    Value_list.append(Value2)
                    Measurement_dic[ID]=Value_list
        print Measurement_dic
        return Measurement_dic

    def get_compare(self,dic1,dic2):
        if cmp(dic1,dic2)==0:
            print "PASSED"
            return True
        else:
            print "FALLED"
            print dic1
            print dic2
            return False

    def make_dir(self,ss_name):
        update_dir=tempfile.mkdtemp()
        update_path = update_dir+os.path.sep+ss_name+".xml"
        print update_path
        return update_path

    def remove_dir(self,xml_path):
        os.remove(xml_path)

#OS=Oversize_Model_Check()
#dic1=OS.get_measurement_dic("D:\\nokmod.xml")
#dic2=OS.get_measurement_dic("D:\\userdata\\danting\\Desktop\\Oversize.xml")
#Err=OS.get_compare(dic1,dic2)
