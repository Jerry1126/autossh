#feature:Fix conflicting contents between post work and koarte in creating big measurement ps view

import os,sys
import xml.etree.ElementTree as et
import tempfile

class Oversize_psview:

    def get_lower(self,string):
        string = string.lower()
        return string
    
    def Oversize_psview(self,output_file_path,ssname):
        ERR=[]
        Measurement_dict=self.get_FromSubViewName(ssname)
        flag=0
        i=0
        table_list=[]
        sort_list=[]
        for key in Measurement_dict.keys():#traversal the key of dictory
            key_lower=key.lower()
            file=open(output_file_path)
            print key_lower
            for line in file.readlines():
                if "CREATE OR REPLACE FORCE VIEW" in line and key_lower in line:
                    flag=1
                if flag==1 and "period_duration_sum" in line:
                    line=line.strip("\n") #delete "\n"
                    line=line.strip(" ") #delete " "
                    period_duration_sum_table = line.split(".")[0]
                if flag==1 and "&owner" in line and "CREATE OR REPLACE FORCE VIEW" not in line:
                    line=line.strip("\n") #delete "\n"
                    line=line.strip(" ") #delete " "
                    table_list.append(line)
                    i=i+1
                if "WHERE" in line:
                    flag=0
                    #print table_list
                    for item in table_list:
                        sort_list.append(item.split(" ")[1].strip(",").strip("t"))
                        if Measurement_dict[key] in item:
                            if period_duration_sum_table in item.split(" ")[1]:
                                print "period_duration_time:PASSED"
                            else:
                                print "FAILED : The SubViewName of period_duration_time is incorrect!"
                                ERR.append(period_duration_time)
                    for item in sort_list:
                        i_str=str(i)
                        if item == i_str:
                            print "order:PASSED"
                        else:
                            print "FALLED : Incorrect order!"
                            ERR.append(order)

                        i=i-1
                    i=0
                    table_list=[]
                    sort_list=[]
        return ERR
            

    def get_koala_xml_path(self,ss_name):
        koala_input_path="metadata"
        ss_name_upper=ss_name.upper()
        xml_file=ss_name+"Koala.xml"
        
        koala_xml_path = "%s%s%s%s%s%s%s" % (os.path.dirname(os.path.dirname(__file__)), os.path.sep, koala_input_path, os.path.sep, ss_name_upper, os.path.sep, xml_file)

        return koala_xml_path

    def get_FromSubViewName(self,ssname):
        Measurement_dict={}
        koala_xml_path=self.get_koala_xml_path(ssname)
        
        tree =  et.parse(koala_xml_path)
        root = tree.getroot()
        nodes = root.getchildren()
        for node in nodes:
            if node.tag == "Adaptation":
                nodes=node.getchildren()

        #get FromSubViewName value
        for node in nodes:
            if node.tag == "Measurement":
                if node.get("OverSize")!= None and node.get("SubMeasName") != None:
                    ID = node.get("ID")
                    secondnodes=node.getchildren()
                    for secondnode in secondnodes:
                        if secondnode.tag == "LogicalCounters":
                            thirdnodes=secondnode.getchildren()
                            for thirdnode in thirdnodes:
                                if thirdnode.tag == "Counter" and thirdnode.get("ID") == "period_duration_sum" and thirdnode.get("FromSubViewName") != None:
                                    Measurement_dict[ID]=thirdnode.get("FromSubViewName")
                    
        print Measurement_dict
        return Measurement_dict

    def get_compare(self,dic1,dic2):
        if cmp(dic1,dic2)==0:
            print "PASSED"
            return True
        else:
            print "FALLED"
            print dic1
            print dic2
            return False

    def make_file(self):
        temp_file=tempfile.mktemp()
        print temp_file
        return temp_file

    def remove_dir(self,xml_path):
        os.remove(xml_path)

#OP=Oversize_psview()
#Measurement_dict=OP.get_FromSubViewName("nokddt")
#OP.Oversize_psview("D:\\nokddtrdb_cre_psviews.sql","nokddt")
