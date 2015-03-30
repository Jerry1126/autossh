# -*- coding:utf-8 -*-
"""
@Filename: check_partation_level.py
@Author:   qgao(qianjing.gao.ext@nokia.com)
@Version:  version 1.0
@Date:     27/Mar/2015
@Purpose:  To check the partition level values between input .xml file and output .cf file
"""
from SSHLibrary import SSHLibrary

import os
import sys
import shutil
import tempfile
import xml.etree.ElementTree as et


class CheckPartationLevel(object):
    _ssh = None    
    @property
    def ssh(self):
        return CheckPartationLevel._ssh
    
    def set_ssh(self, value):
        CheckPartationLevel._ssh = value
        print("*DEBUG* ssh set")

    def get_input_value(self, ss_name):
        '''
        To parse the input value according ss_name. The result seems as below:
        Measure_id TimeLevel  Context  Directory
        ---------- ---------- -------- --------------------------------------------------------------------------------
        [['basey', 'Raw',     'hour',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03cdb/koac03_KOAC03_PMC_part.cf'], 
         ['basey', 'Hour',    'hour',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_rc.cf'], 
         ['basey', 'Day',     'hour',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_rc.cf'], 
         ['basey', 'Week',    'hour',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_rc.cf'], 
         ['basey', 'Month',   'hour',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_rc.cf'], 
         ['basey', 'Raw',     'week',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03cdb/koac03_KOAC03_RAW_part.cf'], 
         ['basey', 'Hour',    'week',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_gc.cf'], 
         ['basey', 'Day',     'week',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_gc.cf'], 
         ['basey', 'Week',    'week',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_gc.cf'], 
         ['basey', 'Month',   'week',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_gc.cf'], 
         ['upgy' , 'Raw',     'hour',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03cdb/koac03_KOAC03_PMC_part.cf'], 
         ['upgy' , 'Hour',    'hour',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_rc.cf'], 
         ['upgy' , 'Day',     'hour',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_rc.cf'], 
         ['upgy' , 'Week',    'hour',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_rc.cf'], 
         ['upgy' , 'Month',   'hour',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_rc.cf'], 
         ['upgy' , 'Raw',     'week',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03cdb/koac03_KOAC03_RAW_part.cf'], 
         ['upgy' , 'Hour',    'week',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_gc.cf'], 
         ['upgy' , 'Day',     'week',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_gc.cf'], 
         ['upgy' , 'Week',    'week',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_gc.cf'], 
         ['upgy' , 'Month',   'week',  u'/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_gc.cf']]
        '''
        measurement_list = []
        koala_input_path = "metadata"
        ss_name_upper = ss_name.upper()
        xml_file = ss_name + "Koala.xml"
        
        # D:\Work\KOALA\test\rtekoa\robot_case\src\metadata\KOAC03\koac03Koala.xml
        koala_xml_path = "%s%s%s%s%s%s%s" % (os.path.dirname(os.path.dirname(__file__)), os.path.sep, koala_input_path, os.path.sep, ss_name_upper, os.path.sep, xml_file)
        
        tree  = et.parse(koala_xml_path)
        root  = tree.getroot()
        nodes = root.getchildren()

        # To get the value and store them into dictionary which will also be stored in a list finally.
        for node in nodes:
            if node.tag == "Measurement":
                secondnodes = node.getchildren()

                for secondnode in secondnodes:
                    if secondnode.tag == "PartitionLevels":
                        id = node.get("ID").lower()
                        record = []
                        thirdnodes = secondnode.getchildren()
                        
                        for thirdnode in thirdnodes:
                            item = []
                            item.append(id)
                            server_type = secondnode.get("ServerType")
                            item.append(thirdnode.tag)

                            value = thirdnode.text
                            item.append(value)

                            if   server_type == 'RC' and thirdnode.tag == 'Raw':
                                # path="/var/tmp/rtekoa/integrationTool/koac03/koac03cdb/koac03_KOAC03_PMC_part.cf"
                                path="%s%s%s%s%s%s" % ("/var/tmp/rtekoa/integrationTool/", ss_name, "/", ss_name+"cdb", "/", ss_name.lower()+"_"+ss_name.upper()+"_PMC_part.cf")                                    
                            elif server_type == 'RC' and thirdnode.tag != 'Raw':
                                # path="/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_rc.cf"
                                path="%s%s%s%s%s%s" % ("/var/tmp/rtekoa/integrationTool/", ss_name, "/", ss_name+"rdb", "/", ss_name.lower()+"_"+ss_name.upper()+"_AGG_part_rc.cf")
                            elif server_type == 'GC' and thirdnode.tag == 'Raw':
                                # path="/var/tmp/rtekoa/integrationTool/koac03/koac03cdb/koac03_KOAC03_RAW_part.cf"
                                path="%s%s%s%s%s%s" % ("/var/tmp/rtekoa/integrationTool/", ss_name, "/", ss_name+"cdb", "/", ss_name.lower()+"_"+ss_name.upper()+"_RAW_part.cf")
                            elif server_type == 'GC' and thirdnode.tag != 'Raw':
                                # path="/var/tmp/rtekoa/integrationTool/koac03/koac03rdb/koac03_KOAC03_AGG_part_gc.cf"
                                path="%s%s%s%s%s%s" % ("/var/tmp/rtekoa/integrationTool/", ss_name, "/", ss_name+"rdb", "/", ss_name.lower()+"_"+ss_name.upper()+"_AGG_part_gc.cf")

                            item.append(path)
                            measurement_list.append(item)
                
        return measurement_list

        
    def compare(self, ss_name):
        '''
        Parse the output .cf file and compare with the input file's value. The format seems as below:
        --------------------------------
          (table_name	"koac03_p_basey_levi_hour"
          (part_col_name	"period_start_time")
          (data_type		"DATE")
          (partition_level	"week")
        --------------------------------
        '''
        result_list = []   # To restore the result list
        error_list  = []   # To restore the error list
        measurement_list = self.get_input_value(ss_name)
        
        for item in measurement_list:
            # ['basey', 'Raw', 'hour', u'/var/tmp/rtekoa/integrationTool/koac03/koac03cdb/koac03_KOAC03_PMC_part.cf'], 
            print "item", item         
            flag = 0
            temp_file = self.make_file()
        
            self.ssh.get_file(item[3], temp_file)
            f = open(temp_file)

            print "-" * 10, item[3]
 
            if item[1] == 'Raw':
                line = f.readline()
                while line:
                    if "table_name" in line and item[0].lower() in line:
                        flag  = 1 
                        count = 0
                        print line
                    
                    if flag == 1:  # The flag to get the fourth line to get the value of partition_level
                        count += 1
                        if count == 4 and "partition_level" in line:
                            value_list = line.split("\"")
                            print 'value_list: ', value_list
                            value = value_list[1]
                            if value == item[2]:
                                print "%s == %s" % (value, item[2])                            
                                print "PASS"
                            else:
                                print "ERROR"
                                error_list = [item[0], item[1], item[2], value]
                                result_list.append(error_list)
                    line = f.readline()


            elif item[1] != 'Raw':
                line = f.readline()
                while line:           
                    if "table_name" in line and item[0].lower() in line and item[0].lower()+"\"" in line:
                    #  (table_name	"koac03_p_meas_upgy_O2"
                        print line
                        flag = 1
                        count = 0
                    
                    if flag == 1:
                        count += 1
                        if count == 4 and "partition_level" in line:
                            value_list = line.split("\"")
                            value = value_list[1]                                
                            if value == item[2].lower():
                                print "%s == %s" % (value, item[2])
                                print "PASS"
                            else:
                                print "ERROR"
                                error_list = [item[0], item[1], item[2], value]
                                result_list.append(error_list)
                    line = f.readline()

            f.close()
            self.remove_file(temp_file)
        print "Measurement | TimeLevel | input_Partition_value | output_Partition_value"
        for error in error_list:
            print error

        return result_list

    def make_file(self):
        temp_file = tempfile.mktemp()
        print temp_file
        return temp_file

    def remove_file(self,temp_file):
        os.remove(temp_file)

