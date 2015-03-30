import sys
import os
import re
import random
import shutil
import tempfile
##import cx_Oracle
from xml.etree.ElementTree import ElementTree  
from xml.etree.ElementTree import Element  
from xml.etree.ElementTree import SubElement as SE

rand = random.Random()
temp_path = tempfile.gettempdir()

class TRANSIENT_OB_ENHANCE:
    local_file_dir = '%s%stransient_object_%s'%(temp_path,os.path.sep,rand.randint(0, 2 ** 30))
    sql_file_path = '/opt/nokia/oss/bin'
    _ssh = None
    @property
    def ssh(self):
        return TRANSIENT_OB_ENHANCE._ssh
    
    def set_ssh(self, value):
        TRANSIENT_OB_ENHANCE._ssh = value
        print("*DEBUG* ssh set")
        
    def get_ssname(self,filename):
        print "***INFO*** Execute to get the Subsystemm name"
        local_file = self._fetch_file_from_remote(filename)
        ssname = self._file_handle_TRANSIENT_OB_ENHANCE(local_file,'Subsystem')
        print "***INFO*** The SSNAME is - %s" %ssname
        return ssname
        
    def get_scname(self,filename):
        print "***INFO*** Execute to get the Subcomponent name"
        local_file = self._fetch_file_from_remote(filename)
        scname = self._file_handle_TRANSIENT_OB_ENHANCE(local_file,'SCName')
        print "***INFO*** The SCNAME is - %s" %scname
        return scname
        
    def get_dbprefix(self,filename):
        print "***INFO*** Execute to get the DB Prefix"
        local_file = self._fetch_file_from_remote(filename)
        dbprefix = self._file_handle_TRANSIENT_OB_ENHANCE(local_file,'DatabaseObjectPrefix')
        print "***INFO*** The DBPREFIX is - %s" %dbprefix
        return dbprefix

    def sql_minus_exist(self,ssname,scname):
        print "***INFO*** Execute to check the SQL minus statement exist or not"
        filearry = []
        minor_version = self._get_minor_version(ssname)
        filelist = self._list_sql_file(ssname)
        filearry=filelist.strip().split("\n")
##        print filearry
##        for index,filename in enumerate(filearry):
##            print filename
        for filename in filearry:
            remote_file = '/opt/nokia/oss/%s-5.0-%s-%s/bin/%s' %(scname.lower(),ssname.lower(),minor_version,filename)
            print remote_file
            local_file = self._fetch_file_from_remote(remote_file)
            flag = self._file_handle_sql_minus_exist(local_file,'MINUS')
            print "***INFO*** The minus exist flag is - %s" %flag
            return flag
            
            

##        local_file = self._fetch_file_from_remote(filename)
##        flag = self._file_handle_sql_minus_exist(local_file,'MINUS')
##        print "INFO: The minus exist flag is : %s" %flag
##        return flag

    def _list_sql_file(self,ssname):
        print "***INFO*** Execute to list the SQL file in %s"% TRANSIENT_OB_ENHANCE.sql_file_path
        filelist = []
        filelist  = self.ssh.execute_command('ls %s | egrep "^%sDimTables[(Insert)|(Update)]" | egrep "_" | egrep -v "gc\.sql"' %(TRANSIENT_OB_ENHANCE.sql_file_path,ssname.lower()), return_rc=True)
        if filelist[1] == 0:
            print "***INFO*** The SQL file name is - \n%s"% filelist[0]
            return filelist[0]
        else:
            print "***ERROR*** list the SQL file failed"
        
##        path = 'D:/Practise/'
##        file_exist_flag = 'false'
##        file_array = []
##        try:
##            for filename in os.listdir(path):
##                m = re.match(r'\w+(_gc_all\.sql|_gc_raw\.sql|_rc\.sql)',filename)
##                if m:
##                    file_exist_flag = 'true'
##                    print path + m.group(0)
##                    #self.sql_minus_exist(path + m.group(0))
##                    file_array.append((path + m.group(0)).strip().split("\t"))
##                    #print file_array
##                else:
##                    continue
##            if file_exist_flag == 'false' :
##                print "INFO: Indicated sql file not exist!"
##        except:
##            print "ERROR: error met when list the dir %s" %path
##        return  file_array

##    def get_sql_file_path(self):
##        print "How to get the sql file path"
        

    def _file_handle_TRANSIENT_OB_ENHANCE(self,fn_local,keyword):
        file_object = open(fn_local)
        try:
            for line in file_object.readlines():
                #print line
                m = re.match(r'\s*\(\s*'+keyword+r'\s+"\s*(\w+)\s*"\s*\)',line,re.I)
                if m:
                    return m.group(1)
                else:
                    continue                
        finally:
            file_object.close()
            
    def _file_handle_sql_minus_exist(self,fn_local,keyword):
        file_object = open(fn_local)
        try:
            for line in file_object.readlines():
                #print line
                m = re.match(r'.*\s+'+keyword+r'\s+.*',line,re.I)
                if m:
                    print "***INFO*** The MINUS exist on the SQL file"
                    return True
                    break
                else:
                    continue
            print "***INFO*** The MINUS not exist on the SQL file"
            return False
        finally:
            file_object.close()


    def _fetch_file_from_remote(self,fn_remote):
        local_file = "%s/%s"%(TRANSIENT_OB_ENHANCE.local_file_dir,os.path.basename(fn_remote))
        self.ssh.get_file(fn_remote,local_file)
        return local_file

    def _get_minor_version(self,ssname):
        sql_file_path = '/opt/nokia/oss/bin'
        link_array =  self.ssh.execute_command('ls -l %s | grep -i %sDimTablesInsert_gc_raw.sql'%(sql_file_path,ssname),return_rc=True)
        if link_array[1] == 0:
            m = re.match(r'.+-'+ssname+r'-([\d\.]+)/',link_array[0],re.I)
            if m:
                return m.group(1)
            else:
                return ""
        else:
            return ""

    def _pmcore_xml_path(self,ssname,scname):
        print "***INFO*** Execute to get the pmcore_xml file path"
##        sql_file_path = '/opt/nokia/oss/bin'
##        link_array =  self.ssh.execute_command('ls -l %s | grep -i %sDimTablesInsert_gc_raw.sql'%(sql_file_path,ssname),return_rc=True)
##        if link_array[1] == 0:
##            m = re.match(r'.+-'+ssname+r'-([\d\.]+)/',link_array[0],re.I)
##            if m:
##                pmcore_xml_file = '/opt/nokia/oss/'+scname+'-5.0-'+ssname+'-'+m.group(1)+'/install/conf/'+ssname+'cdb_pmcore_update.xml'
        minor_version = self._get_minor_version(ssname)
        if minor_version != "":
            pmcore_xml_file = '/opt/nokia/oss/'+scname.lower()+'-5.0-'+ssname.lower()+'-db-'+minor_version+'/install/conf/'+ssname.lower()+'cdb_pmcore_update.xml'
            print "***INFO*** The pmcore_xml file path is - ",pmcore_xml_file
            return pmcore_xml_file,True
        else:
            return "",False

    def parse_pmcore_xml(self,ssname,scname,index_or_alias):
        print "***INFO*** Execute to parse the pmcore_xml file"
        filelist = self._pmcore_xml_path(ssname,scname)
        local_file = ""
        if filelist[1] == True:
            remote_file = filelist[0]
            self.ssh.switch_connection(index_or_alias)
            local_file = self._fetch_file_from_remote(remote_file)
        else:
            print "***ERROR*** Failed to get pmcore_file path"

        tree = ElementTree(file=local_file)
        root = tree.getroot()
##        for e in root.getiterator("MeasurementType"):
##            print e.getchildren()
        for node in root.getiterator("Transient"):
            print node.attrib
        

    def clear_local_tmp_env(self):
        if os.path.exists(TRANSIENT_OB_ENHANCE.local_file_dir):
            shutil.rmtree(TRANSIENT_OB_ENHANCE.local_file_dir)
            print "***INFO*** All the temp file have been deleted"
        else:
            print "***INFO*** temp file not exist, no need to clear"

    def close_ssh_sessions(self):
        print "***INFO*** Execute to close all the ssh connection session"
        self.ssh.close_all_connections()

##sd = TRANSIENT_OB_ENHANCE()
##sd.get_ssname('D:/Practise/nokkttGeneralConfiguration.cf')
##sd.get_scname('D:/Practise/nokkttGeneralConfiguration.cf')
##sd.get_dbprefix('D:/Practise/nokkttGeneralConfiguration.cf')
##sd.sql_minus_exist('D:/Practise/nokkttDimTablesInsert_rc.sql')
##sd.list_sql_file()
##sd.clear_local_tmp_env()
        
        
