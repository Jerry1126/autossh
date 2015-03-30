'''
Created on Oct 21, 2014

@author: danting
'''

import os,sys
import tempfile
import shutil
import xml.etree.ElementTree as et
class Root_Dimension:

    def get_topology_ROOT_ID(self,ss_name):
        IsTransient_flag=0

        koala_input_path="metadata"
        ss_name=ss_name.upper()
        xml_file="nokkddKoala.xml"
        
        koala_xml_path = "%s%s%s%s%s%s%s" % (os.path.dirname(os.path.dirname(__file__)), os.path.sep, koala_input_path, os.path.sep, ss_name, os.path.sep, xml_file)
        
        tree =  et.parse(koala_xml_path)
        root = tree.getroot()
        nodes = root.getchildren()

        #get the value and store them into dictionary which will also be stored in a list finally.
        for node in nodes:
            if node.tag == "Topology":
                if node.get("ID")=="ROOT":
                    secondnodes = node.getchildren()
                    while secondnodes:
                        if secondnodes[0].tag=="Level":
                            Level_flag=1
                            if secondnodes[0].get("IsTransient")=="false":
                                topology_ROOT_ID=secondnodes[0].get("ID") #store the root topology
                                IsTransient_flag=1
                                #If all the level's IsTransient are true, the Koala will report error.
                        if Level_flag==1:
                            secondnodes=secondnodes[0].getchildren()
                            Level_flag=0
                        else:
                            secondnodes=secondnodes[1:]
                    if IsTransient_flag!=1:
                        print "***INFO***: All level's attributes<IsTransient> are true. The Koala will report error!"
                        break
        return topology_ROOT_ID 

    def get_topology_ID(self,ss_name):

        RD=Root_Dimension()
        ROOT_ID=RD.get_topology_ROOT_ID(ss_name)
        
        Topology_dic = {} #store the Topology and Measurement
        Topology_list = [] #store the Topology list in every Measurement

        koala_input_path="metadata"
        ss_name=ss_name.upper()
        xml_file="nokkddKoala.xml"
        
        koala_xml_path = "%s%s%s%s%s%s%s" % (os.path.dirname(os.path.dirname(__file__)), os.path.sep, koala_input_path, os.path.sep, ss_name, os.path.sep, xml_file)
        
        tree =  et.parse(koala_xml_path)
        root = tree.getroot()
        nodes = root.getchildren()

        #get the value and store them into dictionary which will also be stored in a list finally.
        for node in nodes:
            
            if node.tag == "Measurement":
                Measurement_ID = node.get("OMeSName")
                print Measurement_ID
                secondnodes = node.getchildren()
                for secondnode in secondnodes:
                    if secondnode.tag == "TopologyRef":
                        if secondnode.get("ID") == "ROOT":
                            Topology_list.append(ROOT_ID)
                        else:
                            ID = secondnode.get("ID")
                            Topology_list.append(ID)
                Topology_dic[Measurement_ID]=Topology_list
                Topology_list=[]

        print "The input Measurement Topology list:"
        for (k,v) in Topology_dic.items():
           print "Topology_dic[%s]=" % k,v
           
        return Topology_dic

    def get_Dimension_compare(self,ss_name,pmcore_update_path):

        ERR=[]

        RD=Root_Dimension()
        ROOT_ID=RD.get_topology_ROOT_ID(ss_name)
        Topology_dic=RD.get_topology_ID(ss_name)
        
        tree =  et.parse(pmcore_update_path)
        root = tree.getroot()
        nodes = root.getchildren()

        for node in nodes:
            secondnodes = node.getchildren()
            for secondnode in secondnodes:
                if secondnode.tag == "MeOType" and secondnode.get("name") == ROOT_ID:
                    thirdnodes = secondnode.getchildren()
                    for thirdnode in thirdnodes:
                        if thirdnode.tag == "MeasurementType":
                            measurement_name=thirdnode.get("name")
                            forthnodes = thirdnode.getchildren()
                            for forthnode in forthnodes:
                                if forthnode.tag == "ObjectID" and forthnode.get("MeoType") == ROOT_ID:
                                    if forthnode.get("Dimension") == "network_element":
                                        print "PASS: The %s's %s Dimension is correct." %(measurement_name, forthnode.get("OrderInOmes"))
                                    else:
                                        print "FAILD"
                                        err="The %s's first Dimension is not correct" %(measurement_name)
                                        ERR.append(err)
                                if forthnode.tag == "ObjectID" and forthnode.get("MeoType") != ROOT_ID:
                                    for key in Topology_dic.keys():
                                        if key == measurement_name:
                                            if forthnode.get("Dimension") == Topology_dic[key][int(forthnode.get("OrderInOmes"))-1]:
                                                print "PASS: The %s's %s Dimension is correct." %(measurement_name, forthnode.get("OrderInOmes"))
                                            else:
                                                print "FAILD"
                                                err="The %s's %s Dimension is not correct. The wrong Dimension is %s" %(measurement_name, forthnode.get("OrderInOmes"), forthnode.get("Dimension"))
                                                ERR.append(err)

        return ERR

    def modify_xml(self,ss_name,flag1,flag2,flag3):

        koala_input_path="metadata"
        ss_name=ss_name.upper()
        xml_file="nokkddKoala.xml"
        
        koala_xml_path = "%s%s%s%s%s%s%s" % (os.path.dirname(os.path.dirname(__file__)), os.path.sep, koala_input_path, os.path.sep, ss_name, os.path.sep, xml_file)
        
        tree =  et.parse(koala_xml_path)
        root = tree.getroot()
        nodes = root.getchildren()

        #get the value and store them into dictionary which will also be stored in a list finally.
        for node in nodes:
            if node.tag == "Topology":
                if node.get("ID")=="ROOT":
                    secondnodes = node.getchildren()
                    for secondnode in secondnodes:
                        if secondnode.tag=="Level":
                            secondnode.set("IsTransient",flag1)
                            thirdnodes = secondnode.getchildren()
                            for thirdnode in thirdnodes:
                                if thirdnode.tag=="Level":
                                    thirdnode.set("IsTransient",flag2)
                                    forthnodes = thirdnode.getchildren()
                                    for forthnode in forthnodes:
                                        if forthnode.tag=="Level":
                                            forthnode.set("IsTransient",flag3)

        tree.write(koala_xml_path)

    def make_dir(self):
        pmcore_update_dir=tempfile.mkdtemp()
        pmcore_update_path = pmcore_update_dir+os.path.sep+"nokkddcdb_pmcore_update.xml"
        return pmcore_update_path

    def remove_dir(self,xml_path):
        os.remove(xml_path)

#RD=Root_Dimension()
#RD.modify_xml("nokkdd","false","false","false")
