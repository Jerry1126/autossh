# Filename: Hourly_Partition.py

import os,sys
import xml.etree.ElementTree as et
from SSHLibrary import SSHLibrary
import tempfile
import shutil
class Hourly_Partition:
    _ssh = None
    @property

    def ssh(self):
        return Hourly_Partition._ssh
    
    def set_ssh(self, value):
        Hourly_Partition._ssh = value
        print("*DEBUG* ssh set")


    def get_input_value(self,ss_name):

        global Measurement_dic  #store the Measurement_ID
        Measurement_dic = {}
        
        koala_input_path="metadata"
        ss_name_upper=ss_name.upper()
        xml_file=ss_name+"Koala.xml"
        
        koala_xml_path = "%s%s%s%s%s%s%s" % (os.path.dirname(os.path.dirname(__file__)), os.path.sep, koala_input_path, os.path.sep, ss_name_upper, os.path.sep, xml_file)

        tree =  et.parse(koala_xml_path)
        root = tree.getroot()
        nodes = root.getchildren()

        #get the value and store them into dictionary which will also be stored in a list finally.
        for node in nodes:
            if node.tag == "Measurement":
                secondnodes = node.getchildren()
                for secondnode in secondnodes:
                    if secondnode.tag == "PartitionGranularity":
                        id = node.get("ID").lower()

                        #list in Measurement_dic
                        Record=[]
                        thirdnodes = secondnode.getchildren()
                        
                        for thirdnode in thirdnodes:

                            Item=[]
                            
                            TimeLevel=thirdnode.get("TimeLevel")
                            Item.append(TimeLevel)
                            ServiceType=thirdnode.get("ServiceType")
                            Value=thirdnode.text
                            Item.append(Value)

                            if TimeLevel=='Raw' and ServiceType=='RC':
                                #path="/var/tmp/rtekoa/integrationTool/nokktt/nokkttcdb/nokktt_NOKKTT_PMC_part.cf"
                                path="%s%s%s%s%s%s" % ("/var/tmp/rtekoa/integrationTool/", ss_name, "/", ss_name+"cdb", "/", ss_name.lower()+"_"+ss_name.upper()+"_PMC_part.cf")
                            elif TimeLevel=='Raw' and ServiceType=='GC':
                                #path="/var/tmp/rtekoa/integrationTool/nokktt/nokkttcdb/nokktt_NOKKTT_PMC_part.cf"
                                path="%s%s%s%s%s%s" % ("/var/tmp/rtekoa/integrationTool/", ss_name, "/", ss_name+"cdb", "/", ss_name.lower()+"_"+ss_name.upper()+"_RAW_part.cf")
                            elif TimeLevel!='Raw' and ServiceType=='RC':
                                #path="/var/tmp/rtekoa/integrationTool/nokktt/nokkttcdb/nokktt_NOKKTT_PMC_part.cf"
                                path="%s%s%s%s%s%s" % ("/var/tmp/rtekoa/integrationTool/", ss_name, "/", ss_name+"rdb", "/", ss_name.lower()+"_"+ss_name.upper()+"_AGG_part_rc.cf")
                            elif TimeLevel!='Raw' and ServiceType=='GC':
                                #path="/var/tmp/rtekoa/integrationTool/nokktt/nokkttcdb/nokktt_NOKKTT_PMC_part.cf"
                                path="%s%s%s%s%s%s" % ("/var/tmp/rtekoa/integrationTool/", ss_name, "/", ss_name+"rdb", "/", ss_name.lower()+"_"+ss_name.upper()+"_AGG_part_gc.cf")

                            Item.append(path)

                            #adding a key/value pair
                            Record.append(Item)
                        Measurement_dic[id] = Record

        for x in Measurement_dic:
            print x
            for y in Measurement_dic[x]:
                print y
                
        return Measurement_dic

    def compare(self,ss_name):

        ERR=[]
        err=()

        Measurement_dic=self.get_input_value(ss_name)
        
        for key in Measurement_dic.keys():
            print "key name" ,key
            for x in Measurement_dic[key]:
                flag=0
                print x[0]
                print x[1]
                print x[2]
                temp_file=self.make_file()
                self.ssh.get_file(x[2],temp_file)
                f=open(temp_file)

                print "-----------------",x[2]
                if x[0]=='Raw':

                    line = f.readline()
                    while line :
                        
                        if "table_name" in line and key.lower() in line:
                            flag=1
                            count=1
                            print line

                        if flag==1:
                            count=count+1
                            if count==5 and "partition_level" in line:
                                value_list = line.split("\"")
                                value=value_list[1]
                                if value == x[1]:
                                    print "PASS"
                                else:
                                    print "ERR"
                                    err=(key,x[0],x[1],value)
                                    ERR.append(err)
                        line = f.readline()

                elif x[0]!='Raw':
                    line = f.readline()         
                    while line :
                        
                        if "table_name" in line and key.lower() in line and x[0].lower()+"\"" in line:
                            print line
                            flag=1
                            count=1

                        if flag==1:
                            count=count+1
                            if count==5 and "partition_level" in line:
                                value_list = line.split("\"")
                                value=value_list[1]
                                if value == x[1].lower():
                                    print "PASS"
                                else:
                                    print "ERR"
                                    err=(key,x[0],x[1],x[2],value)
                                    ERR.append(err)
                        line = f.readline() 
  
                f.close()
                self.remove_file(temp_file)
        print "Measurement | TimeLevel | input_Partition_value | output_Partition_value"
        for item in ERR:
            print item

        return ERR

    def make_file(self):
        temp_file=tempfile.mktemp()
        print temp_file
        return temp_file

    def remove_file(self,temp_file):
        os.remove(temp_file)

#HP=Hourly_Partition()
#Measurement_dic=HP.get_input_value("nokktt")
#HP.compare(Measurement_dic)

