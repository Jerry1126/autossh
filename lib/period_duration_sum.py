'''
Created on Feb. 10, 2015

@author: danting
'''

import os,sys
import xml.etree.ElementTree as et
import tempfile
import shutil

class period_duration_sum:

    def get_lower(self,string):
        string = string.lower()
        return string

    def get_period_duration_sum_measurementID(self,koala_xml_path):
        Measurement_list = []
        measurement_count=0

        tree =  et.parse(koala_xml_path)
        root = tree.getroot()
        nodes = root.getchildren()
        for node in nodes:
            if node.tag == "Adaptation" : 
                nodes=node.getchildren()

        #get the value and store them into dictionary which will also be stored in a list finally.
        for node in nodes:
            if node.tag == "Measurement":
                secondnodes = node.getchildren()
                for secondnode in secondnodes:
                    if secondnode.tag == "LogicalCounters":
                        id = node.get("ID").lower() #Measurement ID
                        thirdnodes = secondnode.getchildren()
                        
                        for thirdnode in thirdnodes:
                            if thirdnode.tag=="Counter" and thirdnode.get("ID")=="period_duration_sum":
                                Measurement_list.append(id)
                                measurement_count=measurement_count+1

        print "*INFO* measurement_count=%s"%measurement_count
        return Measurement_list

    def check_dnDB(self,file_path,measurement_ID):
        measurement_ID=measurement_ID.upper()
        tree =  et.parse(file_path)
        root = tree.getroot()
        nodes = root.getchildren()
        table_list=[]
        index=-1
        flag=False
        for node in nodes:
            if node.tag == "body" :
                nodes=node.getchildren()

        for node in nodes:
            if node.tag == "div":
                secondnodes = node.getchildren()
                for secondnode in secondnodes:
                    if secondnode.tag == "table":
                        table_list.append(secondnode)
        print "table_list",table_list

        for node in nodes:
            if node.tag == "div":
                secondnodes = node.getchildren()

                for secondnode in secondnodes:
                    if secondnode.tag == "table":
                        thirdnodes = secondnode.getchildren()
                        for thirdnode in thirdnodes:
                            if thirdnode.tag == "caption":
                                line = thirdnode.text
                                if measurement_ID+"_O2" in line:
                                    index=table_list.index(secondnode)
                                    
                    if secondnode == table_list[index+1]:
                        print secondnode
                        thirdnodes = secondnode.getchildren()
                        for thirdnode in thirdnodes:
                            if thirdnode.tag == "tgroup":
                                count=0
                                forthnodes=thirdnode.getchildren()
                                for forthnode in forthnodes:
                                    if forthnode.tag == "tbody":
                                        fifthnodes= forthnode.getchildren()
                                        for fifthnode in fifthnodes:
                                            if fifthnode.tag == "row":
                                                sixthnodes = fifthnode.getchildren()
                                                for sixthnode in sixthnodes:
                                                    if sixthnode.tag == "entry" and sixthnode.get("colname")=="1":
                                                        seventhnodes = sixthnode.getchildren()
                                                        for seventhnode in seventhnodes:
                                                            if seventhnode.tag== "para":
                                                                if seventhnode.text == "period_duration_sum":
                                                                    print seventhnode.text
                                                                    flag = True

        return flag
    
    def check_pmc_view(self,output_file_path,measurement_ID):
        measurement_ID=measurement_ID.lower()
        flag=0
        iflag=False
        file=open(output_file_path)
        for line in file.readlines():
            if "CREATE OR REPLACE FORCE VIEW" in line and measurement_ID in line:
                flag=1
            if flag==1 and "rawtable.duration as period_duration_sum" in line:
                iflag=True
            if flag==1 and "FROM" in line:
                break
        return iflag

    def check_pvps_view(self,output_file_path,measurement_ID):
        measurement_ID=measurement_ID.lower()
        flag=0
        iflag=False
        file=open(output_file_path)
        for line in file.readlines():
            if "CREATE OR REPLACE FORCE VIEW" in line and measurement_ID in line:
                flag=1
            if flag==1 and "b.period_duration_sum" in line:
                iflag=True
            if flag==1 and "from" in line:
                break
        print iflag
        return iflag

    def check_ps_AND_pv_gc_view(self,output_file_path,measurement_ID):
        measurement_ID=measurement_ID.lower()
        flag=0
        iflag=False
        file=open(output_file_path)
        for line in file.readlines():
            if "CREATE OR REPLACE FORCE VIEW" in line and measurement_ID in line:
                flag=1
            if flag==1 and "period_duration as period_duration_sum" in line:
                iflag=True
            if flag==1 and "FROM" in line:
                break
        print iflag
        return iflag
    
    def make_file(self):
        temp_file=tempfile.mktemp()
        print temp_file
        return temp_file

    def remove_file(self,file_path):
        os.remove(file_path)

#PD=period_duration_sum()
#PD.check_dnDB("D:\\userdata\\danting\\Desktop\\dnDBDescription.xml","traffict")

