import sys
import os
import re
import random
import shutil
import tempfile


rand = random.Random()
temp_path = tempfile.gettempdir()

class GCDirectIntegration:
    local_file_dir = '%s%sgc_direct_integration_%s'%(temp_path,os.path.sep,rand.randint(0, 2 ** 30))
    sql_file_path = '/var/tmp/rtekoa/integrationTool/'
    line_indicator = 3
    _ssh = None
    @property


    def ssh(self):
        return GCDirectIntegration._ssh
    
    def set_ssh(self, value):
        GCDirectIntegration._ssh = value
        print("*DEBUG* ssh set")



    def set_GCDirectIntegration_value(self,configfile_path,substitution_value='null'):
        substitution_string = ""
        if substitution_value == "Null" or substitution_value == "null":
            substitution_string = ""
        else:
            substitution_string = "(GCDirectIntegration            \"%s\")" %substitution_value
        
        returnlist = self.ssh.execute_command('grep -i GCDirectIntegration < %s' %(configfile_path), return_rc=True)
        
        if returnlist[1] == 0:
            output1 = self.ssh.execute_command('sed -i \'s/.*GCDirectIntegration.*/%s/\' %s' %(substitution_string,configfile_path),return_rc=True)
            if output1[1] == 0:
                print "***INFO*** Modify the GCDirectIntegration value with %s successful\n" %substitution_value
                return True
            else:
                print "***ERROR*** Modify the GCDirectIntegration value with %s failed\n" %substitution_value
                return False
            
        else:
            output2 = self.ssh.execute_command('sed -i \'$a %s\' %s' %(substitution_string,configfile_path),return_rc=True)
            if output2[1] == 0:
                print "***INFO*** Append the GCDirectIntegration value with %s successful\n" %substitution_value
                return True
            else:
                print "***ERROR*** Append the GCDirectIntegration value with %s failed\n" %substitution_value
                return False
             

    def get_GCDirectIntegration_value(self,filename):
        print "***INFO*** Execute to get GCDirectIntegration value\n"
        local_file = self._fetch_file_from_remote(filename)
        value = self._file_handle_GCDirectIntegration(local_file)
    
##        value = self._file_handle_GCDirectIntegration(filename)
        if value == "1" or value == "0":
            print "***INFO*** The GCDirectIntegration value is - %s\n" %value
        elif value == "":
            print "***INFO*** The GCDirectIntegration value is set to default (1) as GCDirectIntegration not configure in general configuration file\n"
            value = "1"
        else:
            print "***INFO*** The GCDirectIntegration value is set to default (1) as GCDirectIntegration value is - %s in general configuration file\n" %value
            value = "1"
        return value

    def check_agg_on_value(self,ssname,gcd_direct_integration_value):
        count = 0
        key = ""
        value = ""
        return_value = "pass"
        output = ""

        print "***INFO*** Start to check agg_on value in SQL file\n"
        
        filearry = []
        filelist = self._list_sql_file(ssname)
        filearry=filelist.strip().split("\n")
#        file_path = "%s/%s/%srdb" %(GCDirectIntegration.sql_file_path,ssname,ssname)
        temp_name = "%srdb" %(ssname.lower())
        file_path = os.path.join(GCDirectIntegration.sql_file_path,ssname.lower(),temp_name)
        
        for filename in filearry:
            remote_file = '%s/%s' %(file_path,filename)
            local_file = self._fetch_file_from_remote(remote_file)
            flag_value = self._rc_gc_sql_flag(local_file,gcd_direct_integration_value)
            
            output = self._block_handle(local_file,flag_value)
                
            if output == "pass":
                print "***INFO*** all the agg_on value in SQL file %s is correct\n" % os.path.basename(local_file)
            else:
                return_value = "fail"
                print "***ERROR*** Parts of agg_on value in SQL file %s is not correct\n" % os.path.basename(local_file)
                
        if return_value == "pass":
            return True
        else:
            return False
        
    def _file_handle_GCDirectIntegration(self,local_file):
        file_object = open(local_file)
        try:
            for line in file_object.readlines():                
                m = re.match(r'\s*\(\s*GCDirectIntegration\s+"(.*)"\s*\)',line,re.I)
                if m:
                    return m.group(1).strip()
                    break
                else:
                    continue
            return "".strip()
        finally:
            file_object.close()

    def _fetch_file_from_remote(self,fn_remote):
        local_file = "%s/%s"%(GCDirectIntegration.local_file_dir,os.path.basename(fn_remote))
        self.ssh.get_file(fn_remote,local_file)
        return local_file


    def _list_sql_file(self,ssname):
#        file_path = "%s/%s/%srdb" %(GCDirectIntegration.sql_file_path,ssname,ssname)
        temp_name = "%srdb" %(ssname.lower())
        file_path = os.path.join(GCDirectIntegration.sql_file_path,ssname.lower(),temp_name)

        print "***INFO*** Execute to list the SQL file in %s\n"% file_path
        filelist = []
        filelist  = self.ssh.execute_command('ls %s | egrep "aoa_cre_config"' %(file_path), return_rc=True)
        if filelist[1] == 0:
            print "***INFO*** The SQL file name is - \n%s\n"% filelist[0]
            return filelist[0]
        else:
            print "***ERROR*** list the SQL file failed\n"


    def _rc_gc_sql_flag(self,local_file,gcd_direct_integration_value):
        if gcd_direct_integration_value == "1" and re.match(r'.*aoa_cre_config_rc',local_file,re.I):
            return "0"
        elif gcd_direct_integration_value == "1" and re.match(r'.*aoa_cre_config_gc',local_file,re.I):
            return "1"
        elif gcd_direct_integration_value == "0" and re.match(r'.*aoa_cre_config_rc',local_file,re.I):
            return "1"
        elif gcd_direct_integration_value == "0" and re.match(r'.*aoa_cre_config_gc',local_file,re.I):
            return "0"
        else:
            return gcd_direct_integration_value
    

##Split the SQL files into several blocks for each SQL statement
    def _block_handle(self,filename,flag_value):
        filearray = []
        filearray2 = []
        string = ""
        output = ""
        delimiter = ','
        flag = "discard"
        tag = "begin"
        return_value = "pass"
        
        try:
            file_object = open(filename)
            
            filearray = file_object.readlines()
            length = len(filearray)
            
            for i in range(0,length):
                if re.match(r'INSERT INTO',filearray[i]):
                    tag = "begin"
                    flag = "store"
                elif re.match(r';',filearray[i]):
                    flag = "discard"         
                
                if tag == "end" and string != "":
#                    print string
                    output = self._dict_handle(string,flag_value)
                    filearray2 = []
                    string = ""
                
                if flag == "store" and filearray[i].strip() != "":
                    filearray2.append(filearray[i].strip().strip('(').strip(';').strip(',').strip(')'))
                    string = delimiter.join(filearray2)
                
                if re.match(r'.*\);',filearray[i]):
#                    print ">>>>>>>>>>>>>>>"
                    tag = "end"
                
#                print "The output is <%s>\n" %output
                    
                if output == "fail":
                    return_value = "fail"
                        
#            print string
        finally:
            file_object.close()        
        return return_value


##Store the each SQL statement colums and their values in to directory.And then handle them according to the gc_direct_integration value (0 and 1)
    def _dict_handle(self,string,flag_value):
        array_original = []
        array_attribute = []
        array_value = []
        flag_table = "1"
        return_value = "pass"
        dict = {}
        array_original = string.split(',')
        print "***** The SQL block element store in array as below *****\n",array_original
        print "*********************************************************\n"
        length = len(array_original)
        for i in range(0,length):
            if re.match(r'.*VALUES.*',array_original[i].strip()):
                 flag_table = "2"
             
            if flag_table == "2":
                 array_value.append(array_original[i].strip())
            else:
                 array_attribute.append(array_original[i].strip())
                 
#            print array_original[i].strip()
#         
#        print len(array_attribute)
#         
#        print len(array_value)
             
        if len(array_attribute) == len(array_value):
            for i in range(0,len(array_attribute)):
#                print "****** ", array_attribute[i]
                dict[array_attribute[i]] = array_value[i]
        else:
            print "***ERROR*** Table's values not matching with the table's attributes\n"
            return_value = "fail"
             
#        print array_value
#        print "@@@@@@@@@@@@@@@@@ ",dict
        
        if flag_value == "1" and return_value == "pass":
            if str(dict['agg_on']) == "1":
                print "The agg_on value for measurement type [%s] is %s\n" %(dict['meas_type_name'],dict['agg_on'])
                return_value = "pass"
            else:
                print "The agg_on value for measurement type [%s] is %s\n" %(dict['meas_type_name'],dict['agg_on'])
                print "***ERROR*** The agg_on value must be 1 for mesurement type - %s\n" %dict['meas_type_name']
                return_value = "fail"
        elif flag_value == "0" and return_value == "pass":
            if str(dict['agg_on']) == "0":
                print "The agg_on value for measurement type [%s] is %s\n" %(dict['meas_type_name'],dict['agg_on'])
                return_value = "pass"
            else:
                print "The agg_on value for measurement type [%s] is %s" %(dict['meas_type_name'],dict['agg_on'])
                print "***ERROR*** The agg_on value must be 0 for mesurement type - %s\n" %dict['meas_type_name']
                return_value = "fail"
        
        return return_value
            

    def clear_local_tmp_env(self):
        if os.path.exists(GCDirectIntegration.local_file_dir):
            shutil.rmtree(GCDirectIntegration.local_file_dir)
            print "***INFO*** All the temp file have been deleted\n"
        else:
            print "***INFO*** temp file not exist, no need to clear\n"

    def close_ssh_sessions(self):
        print "***INFO*** Execute to close all the ssh connection session\n"
        self.ssh.close_all_connections()

            
#di = GCDirectIntegration()
##di.get_GCDirectIntegration_value('D:/Practise/nokkttGeneralConfiguration.cf')
##di.check_agg_on_value('D:/Practise/nokkttrdb_aoa_cre_config_rc.sql',1)
