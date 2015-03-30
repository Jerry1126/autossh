import os,sys
import string
from random import Random
from random import choice
import random
import tempfile
import shutil
import xml.etree.ElementTree as et

class ExecuteCmdCommand:
    def command_line(self,cmd):
        rc = os.system(cmd)
        if rc ==0:
            return True
        else:
            return False
    
    def _get_dir(self,dir_name,count=0):
        while count>0:
            dir_name = self._get_dir(os.path.dirname(dir_name))
            count = count-1
        return dir_name
    
    def get_absolute_path(self,postfix_str,count='0'):
        '''str: the str that are different contrasted to current lib file path
        count: the times that upwards to the parent dir based on current lib file dir'''
        count = string.atoi(count)
        print type(count)
        if count>0:
            sub_path = self._get_dir(os.path.dirname(__file__), count)
        else:
            sub_path = os.path.dirname(__file__)
        #tail_pos = string.atoi(tail_pos)
        print "sys path:%s" %sys.path[0]
        print "os.getcwd():%s" %os.getcwd()
        print "os.path.abspath('.')%s" %os.path.abspath('.')
        #print type(tail_pos)
        #print "INFO: the lib path is %s" %lib_path
        #sub_path = lib_path[:"%d"% tail_pos]
        path = sub_path + postfix_str
        print "The sub_path:%s" %sub_path
        print "The postfix_str:%s" %postfix_str
        print "The path:%s" %path
        return path

    def random_str(self,randomlength):
        str = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(randomlength):
            str+=chars[random.randint(0, length)]
        return str

    def get_counter_list(self, koala_input_path):
        tree =  et.parse(koala_input_path)
        t=tree.getiterator("Counter")
        counter_list=[]
        for counter in t:
            counter_name=counter.get("ID")
            counter_list.append(counter_name)
        return counter_list

    def make_dir(self):
        pmcore_update_dir=tempfile.mkdtemp()
        pmcore_update_path = pmcore_update_dir+os.path.sep+"nokkddcdb_pmcore_update.xml"
        return pmcore_update_path

    def remove_dir(self,xml_path):
        os.remove(xml_path)

    def get_random_formula(self,length,koala_input_path):
        counter_list=self.get_counter_list(koala_input_path)
        formula_list=['SUM', 'AVG', 'MAX', 'MIN', 'LOG','POWER']
        value_list=['0','1','2','3','4','5','6','7','8','9']
        formula_len=3
        formula=choice(counter_list)
        print choice(formula_list)
        while formula_len < length-1:
            value=choice(value_list+counter_list)
            formula = choice(formula_list)+"("+value+","+formula+")"
            formula_len = len(formula)
        print formula_len
        return formula
