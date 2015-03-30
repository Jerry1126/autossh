# -*- coding=utf-8 -*-  
'''
Created on Oct 21, 2014

@author: sun li/chen jingping
'''

import os,re,sys,random,string
from SSHLibrary import SSHLibrary
import copy
import tempfile
import shutil
import xml.etree.ElementTree as etree
#from xml.etree.ElementTree import Element

rand = random.Random()
resultOfParentsList  = []
resultOfParents=''
ss_name="nokktt"
koala_input_path='metadata'
xml_file="nokkttKoala.xml"       
koala_xml_path = "%s%s%s%s%s%s%s" % (os.path.dirname(os.path.dirname(__file__)), os.path.sep, koala_input_path, os.path.sep, ss_name, os.path.sep, xml_file)

match_flag = False
dict = []
class ModifySSKoalaxmlfile():
    _ssh = None
    @property
    def ssh(self):
        return ModifySSKoalaxmlfile._ssh
    def set_ssh(self, value):
        ModifySSKoalaxmlfile._ssh = value
        print("*DEBUG* ssh set")    
    def __init__(self,fileName):
        global koala_input_path
        global koala_xml_path
        global ss_name
        global xml_file
        if file=='':
            self.fileName = koala_xml_path
        else:
            self.fileName = fileName
        print self.fileName

        if os.path.isfile(self.fileName) == True:

            self.tree = etree.parse(self.fileName)
            self.root = self.tree.getroot()
            self.resultOfParentsList  = []
        else:
            print " The file %s does not exist! please input a tag name. \n" %self.fileName
            return 
    def get_XMLNode(self,name):
        return self.tree.getiterator(name) if self.tree.getiterator(name) else []
    def nodeList(self,koala_input_path,returnRequire='IDlist',tag='Measurement',xml_file='nokkttKoala.xml'):
        fileName=self.get_xml_from_server(koala_input_path,xml_file='nokkttKoala.xml')
        self.fileName=fileName
        self.__init__(self.fileName)
        nodeList=[]
        ms=self.tree.getiterator(tag)
        print ms
        if len(ms)==0:
            print "The given tag %s is not found" %tag
            self.remove_temp_file(self.fileName)
            return         
        for m in ms:
            nodeList.append(m.get('ID'))
        print nodeList
        self.remove_temp_file(self.fileName)
        if returnRequire=='length':
            return len(nodeList)
        else:
            return nodeList
    def AddNode(self,tag,koala_input_path,xml_file='nokkttKoala.xml',ID=''):
        '''add node bellow node which with parameter ID property value,if its empty then add 
        node similar to anyone,after add a node, put the updated file to koala_input_path '''
        fileName=self.get_xml_from_server(koala_input_path,xml_file='nokkttKoala.xml')
        self.fileName=fileName
        self.__init__(self.fileName)
        m=0
        ms=self.get_XMLNode(tag)
        if len(ms)==0:
            print "The given tag %s is not found" %tag
            self.remove_temp_file(self.fileName)
            return        
        if ID =='':
            ID=self.cloneAndModifyNode(ms[rand.randint(0,len(ms)-1)],initRoot='')
        else:
            for i in range(len(ms)):
                if ms[i].attrib.has_key('ID'):
                    if ms[i].get('ID') == ID :
                        ID=self.cloneAndModifyNode(ms[i],initRoot='')
                        break
                    else:
                        continue
                elif ms[i].text:
                        if ms[i].text == ID:
                            ID=self.cloneAndModifyNode(ms[i],initRoot='')
                            break
                        else:
                            continue
                else:
                    continue
            if i==len(ms)-1:
                print ' ***INFO*** There is no node similar to  %s property or text content,then add similar to another one ' %ID
                ID=self.cloneAndModifyNode(ms[rand.randint(0,len(ms)-1)],initRoot='')      
        self.ssh.put_file(self.fileName,koala_input_path)
        self.remove_temp_file(self.fileName)
        return ID     
         
    def deleteNode(self,tag,koala_input_path,xml_file='nokkttKoala.xml',ID=''):
        '''delete node bellow node which with parameter ID property value,if its empty then delete 
        node anyone,after delete a node, put the updated file to koala_input_path '''        
        fileName=self.get_xml_from_server(koala_input_path,xml_file)
        self.fileName=fileName
        self.__init__(self.fileName)
        m=0		
        ms=self.get_XMLNode(tag)
        if len(ms)==0:
            print "The given tag %s is not found" %tag
            return
        if ID == '':
            l=len(ms)
            m=rand.randint(0,l-1)
        else:
            for i in range(len(ms)):
                if ms[i].attrib.has_key('ID'):
                    if ms[i].get('ID') == ID :
                        print "node with %s ID property value is found,it's %s" %(ID,ms[i])
                        m=i
                        break
                    else:
                        continue
                elif ms[i].text:
                    if ms[i].text == ID:
                        print "node with %s ID text value is found,it's %s" %(ID,ms[i])
                        m=i
                        break
                    else:
                        continue
                else:
                    continue
            if i== len(ms)-1:                
                print ' ***INFO*** There is no node with %s property or text content,then delete another one ' %ID
                m=i  
        if tag== 'Counter':
            filePath=self.fileName
            regex='<Formula>.*%s.*</Formula>' %ms[m].get('ID')
            while True:                
                if self.findString(filePath,regex):
                    print 'The counter %s is used in busyhourdefination formula' %ms[m].get('ID')
                    m=rand.randint(0,len(ms)-1)
                    regex='<Formula>.*%s.*</Formula>' %ms[m].get('ID')
                    continue
                else:
                    break        
        if ms[m].get('ID'):
            property = ms[m].get('ID')
        elif ms[m].text:
            property = ms[m].text
        else:
            property='there is no ID property and also no text value'
        print " *** INFO *** You are trying to remove node with tag %s,and it property ID/text is %s" %(ms[m].tag,property) 
        ms[m].clear()
        print " clear the current element's children"
        initRoot=''
        parentElement=self.findParent(ms[m],initRoot)
        print " found the parent element"
        parentElement.remove(ms[m])
        self.tree.write(self.fileName)
        self.ssh.put_file(fileName,koala_input_path)
        self.remove_temp_file(fileName)
        return property       
    def findString(self,filePath,regex):
        fileObj=open(filePath,'r')
        flag= False
        for eachLine in fileObj:
            if re.search(regex,eachLine,re.I):
                print eachLine
                flag = True
                break
        return flag
    def findFatherTag(self,tag,initRoot = ""):
        resultOfParents=''       
        if initRoot is "":
            initRoot = self.root
        else:
            initRoot=initRoot
        print " initRoot in the beginning is %s,and resultOfParents is %s" %(initRoot,resultOfParents)
        for self.children in initRoot.getchildren():                    
            if self.children.tag == tag: 
                print "self.children when self.children equal to tag is: %s" %self.children   
                resultOfParents = initRoot 
                print " ***INFO *** resultOfParents is found,it's %s. and should break recursion" %resultOfParents
                resultOfParentsList.append(resultOfParents)
                return resultOfParents                
            else:    
                print " ***INFO *** self.children is %s not equal to tag is: %s,and enter next recursion" %(self.children,tag)
                if len(initRoot.getchildren())>0 and resultOfParents is '':
                    self.findFatherTag(tag,self.children)
    

    def cloneAndModifyNode(self,element,initRoot=''):
        if initRoot is "":     
            initRoot = self.root
        else:
            initRoot=initRoot
        # copy element content to new xml file
        pmcore_update_dir=tempfile.mkdtemp()    
        copyed_path = pmcore_update_dir+os.path.sep+"temp.xml"
        file = open(copyed_path, "w+b")
        xmlstr = etree.tostring(element, encoding='utf8', method='xml')
        file.write(copy.deepcopy(xmlstr))
        file.close()
        newName= ''.join(random.sample(string.ascii_letters,5))
        # replace ID property value with new value
        f = open(copyed_path,'r')
        xmldata=f.read() 
        if element.attrib.has_key('ID'):
            xmldata = re.sub(element.get('ID'),newName,xmldata)
            f.close()
            f = open(copyed_path,'w')
            f.write(xmldata)
            f.close()
            print " New node with tag %s similart to whose ID proverty value %s is generated" %(element.tag,element.get('ID'))
        else:
            print "***INFO*** there is no content to be replaced"
        # append the content to koala.xml
        newTree= etree.parse(copyed_path)
        parentElement=self.findParent(element,initRoot)   
        parentElement.append(copy.deepcopy(newTree.getroot())) 
        print "copy node %s ,and it's attrib is %s finished" %(element,element.attrib)
        self.tree.write(self.fileName)
        self.remove_temp_file(copyed_path)        
        if element.attrib.has_key('ID'):
            property = newName
        elif newTree.text:
            property = element.text
        else:
            property='there is no ID property and also no text value'  
        return property
            
    def localFile_create(self,xml_file='nokkttKoala.xml'):
        pmcore_update_dir=tempfile.mkdtemp()
        copyed_path = pmcore_update_dir+os.path.sep+xml_file     
        return copyed_path
    
    def get_xml_from_server(self,koala_input_path,xml_file='nokkttKoala.xml'):
        localFile_path=self.localFile_create(xml_file='nokkttKoala.xml')
        self.ssh.get_file(koala_input_path,localFile_path)
        return localFile_path   
    def remove_temp_file(self,temp_file_path):
        os.remove(temp_file_path)        
    def findParent(self,element,initRoot=''):
        ms=self.get_XMLNode(element.tag)
        l=len(ms)
        own_parent=''
        m=rand.randint(0,l-1)
        self.findFatherTag(ms[m].tag,initRoot)
        self.resultOfParentsList=[i for i in self.resultOfParentsList if i is not '']
        if len(resultOfParentsList)==1:
            own_parent=resultOfParentsList[0]
        else:
            for i in range(len(resultOfParentsList)):
                for self.children in resultOfParentsList[i].getchildren():
                    if self.children.attrib == {} and element.attrib == {}:
                        if self.children.text==element.text:
                            own_parent=resultOfParentsList[i]
                            break
                        else:         
                            continue
                    elif self.children.attrib == {} and element.attrib != {}:
                        print "self.children.attrib == {} and element.attrib != {},continue;element.attrib is %s" %(element.attrib)                    
                        continue
                    elif self.children.attrib != {} and element.attrib == {}:
                        print "self.children.attrib != {} and element.attrib == {},continue;self.children.attrib is %s," %(self.children.attrib)                    
                        continue
                    elif self.children.attrib != {} and element.attrib != {} :
                        if self.children.attrib==element.attrib:
                            print "self.children.attrib != {} and element.attrib != {},found;self.children.attrib is %s,element.attrib is %s" %(self.children.attrib,element.attrib)                                                
                            own_parent=resultOfParentsList[i]
                            break
                        else:
                            print "self.children.attrib is %s,element.attrib is %s" %(self.children.attrib,element.attrib)                    
                            continue                        
        if own_parent is '':
            print "*INFO* error happen, node has not found its own parent"
        else:
            print "*INFO* own_parent is %s,it's tag is %s" %(own_parent,own_parent.get('ID'))
        return own_parent

    def modify_arrtibute_value(self,attribute,value,koala_input_path,xml_file='nokkttKoala.xml',tagname=None,identify_flag=None):
        #file = o s.path.abspath(filename)
        fileName=self.get_xml_from_server(koala_input_path,xml_file)
        self.fileName=fileName
        self.__init__(self.fileName)
        t=self.get_XMLNode(tagname)
        if identify_flag is not None:
            t = self._identify_specifical_element(t, identify_flag)
        if t == "error 1":
            self.remove_temp_file(fileName)
            raise AssertionError ("***ERROR*** Can't not find the identify_flag - [%s] under the specify tag - %s"%(identify_flag, tagname))
        elif t == "error 2":
            self.remove_temp_file(fileName)
            raise AssertionError ("***ERROR*** Find more than one identify_flag - [%s] under the specify tag - %s"%(identify_flag, tagname))
                        
        match_return_value = self._iteration_find_attribute(t,attribute)    
        if match_return_value is True:
            print ("***INFO*** attribute - [%s] have found under tag - %s"%(attribute,tagname))
            self._modify_attribute_value_randomly(attribute,value)
            self.tree.write(self.fileName)
            self.ssh.put_file(fileName,koala_input_path)
            self.remove_temp_file(fileName)            
            self._clear_temp_setting()
        else:
            self.ssh.put_file(fileName,koala_input_path)
            self.remove_temp_file(fileName)            
            self._clear_temp_setting()
            raise AssertionError ("***ERROR*** attribute - [%s] have not found under tag - %s"%(attribute,tagname))

    def modify_subelement_value(self,subelement,value,koala_input_path,xml_file='nokkttKoala.xml',tagname=None,identify_flag=None):
        fileName=self.get_xml_from_server(koala_input_path,xml_file)
        self.fileName=fileName
        self.__init__(self.fileName)
        self.tree =  etree.parse(fileName)
        t=self.tree.getiterator(tagname)
        if identify_flag is not None:
            t = self._identify_specifical_element(t, identify_flag)
        if t == "error 1":
            self.remove_temp_file(fileName)
            raise AssertionError ("***ERROR*** Can't not find the identify_flag - [%s] under the specify tag - %s"%(identify_flag, tagname))
        elif t == "error 2":
            self.remove_temp_file(fileName)
            raise AssertionError ("***ERROR*** Find more than one identify_flag - [%s] under the specify tag - %s"%(identify_flag, tagname))

        for element in t:
            nodes = element.getchildren()
            for node in nodes:
                if node.tag == subelement:
                    print node.text
                    node.text=value
                    self.tree.write(self.fileName)
                    self.ssh.put_file(fileName,koala_input_path)
                    self.remove_temp_file(fileName)
                    self._clear_temp_setting() 
        
    def _identify_specifical_element(self, element, identify_flag):
        count = 0
        return_element = []
        for t in element:
            if identify_flag in t.attrib.values():
                count += 1
                return_element.append(t)
        if count == 1:
            return return_element
        elif count == 0:
            return "error 1"
        else:
            return "error 2"
        
    def _iteration_find_attribute(self,element,attribute):
        global match_flag
        global dict
        for t in element:
            if attribute in t.attrib.keys():
                match_flag = True
                dict.append(t)
                children_element = t.getchildren()
                if children_element:
                    self._iteration_find_attribute(children_element,attribute)
        return match_flag
        
    def _modify_attribute_value_randomly(self,attribute,value):
        length = 0
        length = len(dict)
        int_number =  random.randint(0,length-1)
        print "***INFO*** %d places have found for attribute - %s"%(length,attribute)
        print "***INFO*** Try to modify the place %d"%(int_number+1)   
        element_object = dict[int_number]
        element_object.set(attribute,value) 
        print "***INFO*** %s in place %d have been modified with - %s"%(attribute,int_number+1,value)
     
    def _clear_temp_setting(self):
        global match_flag,dict
        match_flag = False
        dict = []
    

