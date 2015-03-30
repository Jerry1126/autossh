'''
    Draft created by Chen Jinping on 2014/9/20
    This Library used to verify the function 
    of pmpmgrmx_part_copy_stat.sh enhancement 
    for PET optimize.
'''

import os
import sys
import re
import string
import random
import shutil
import tempfile


rand = random.Random()
temp_path = tempfile.gettempdir()


class PetOptimize:
    new_script_for_add = '/opt/nokia/oss/bin/pmpmgrmx_part_copy_stat.sh'
    dir_path = '/var/tmp/rtekoa/integrationTool'
    local_file_dir = '%s%stransient_object_%s'%(temp_path,os.path.sep,rand.randint(0, 2 ** 30))
    
    _ssh = None
    @property
    def ssh(self):
        return PetOptimize._ssh
    
    def set_ssh(self, value):
        PetOptimize._ssh = value
        print("*DEBUG* ssh set")
    
    def get_agg_raw_value_from_general_config_file(self,general_config_file):
        agg_raw_value_dict = {}
        keyworld_lists = ["EnablePartTableStatsforAgg","EnablePartTableStatsforRaw"]
    
        print "***INFO*** Execute to get the EnablePartTableStatsforAgg and EnablePartTableStatsforRaw in general config file\n"
        local_general_config_file = self._fetch_file_from_remote(general_config_file)
        agg_raw_value_dict = self._file_handle_to_get_agg_raw_value(local_general_config_file,keyworld_lists)
    
        for keyword in keyworld_lists:
            if agg_raw_value_dict.has_key(keyword):
                continue
            else:
                print "***INFO*** %s not defined in general config file, the value will set default!\n"%keyword
                agg_raw_value_dict[keyword] = 0
        for key in agg_raw_value_dict.keys():
            value = agg_raw_value_dict[key]
            str_dict_value = str(value)
            if str_dict_value == "":
                print "***INFO*** %s defined with empty value in general config file, change it to default - 0\n"%key
                agg_raw_value_dict[key] = 0
            elif str_dict_value.strip() != "0" and str_dict_value.strip() != "1":
                print "***INFO*** %s defined with not 1 or 0 or empty value in general config file, change it to default - 1\n"%key
                agg_raw_value_dict[key] = 1
            else:
                print "***INFO*** %s defined with %s in general config file\n"%(key,str_dict_value)
  
        print "***INFO*** The dictionary of EnablePartTableStatsforAgg and EnablePartTableStatsforRaw is :"
        print agg_raw_value_dict
        return agg_raw_value_dict

    def _fetch_file_from_remote(self,fn_remote):
        local_file = "%s/%s"%(PetOptimize.local_file_dir,os.path.basename(fn_remote))
        self.ssh.get_file(fn_remote,local_file)
        return local_file

    def _file_handle_to_get_agg_raw_value(self,local_file,keyworld_lists):
        return_dict = {}
        file_object = open(local_file)
        try:
            for line in file_object.readlines():
                for keyword in keyworld_lists:
                    m = re.match(r'\s*\(\s*'+keyword+r'\s+"(.*)"\s*\)',line,re.I)
                    if m:
                        return_dict[keyword] = m.group(1)
                    else:
                        continue                
        finally:
            file_object.close()
        return return_dict

    def get_cron_str_from_db_config_unconfig(self,ss_name,sc_name,agg_raw_value_dict,install_type='rc'):
        print agg_raw_value_dict
        return_flag = []
        cron_str_values = []
        count = 0
        db_config_return_value = "fail"
        db_unconfig_return_value = "fail"
        ss_name = ss_name.upper()
        sc_name = sc_name.upper()
        configure_file_name = 'Nokia-%s-%s-DB.configure'%(sc_name,ss_name)
        unconfigure_file_name = 'Nokia-%s-%s-DB.unconfigure'%(sc_name,ss_name)
        path_tmp = '%s%s%s'%(PetOptimize.dir_path,'/',ss_name.lower())
        path = '%s%s%s'%(path_tmp,'/','INSTALL')
        
        configure_file_exists_return_value = self._check_file_exists(path,configure_file_name)
        unconfigure_file_exists_return_value = self._check_file_exists(path,unconfigure_file_name)
        
        for agg_or_raw_key in agg_raw_value_dict.keys():
            agg_or_raw_value = str(agg_raw_value_dict['%s'%agg_or_raw_key])
            
            if agg_or_raw_key == "EnablePartTableStatsforRaw":
                agg_or_raw = "raw"
            else:
                agg_or_raw = "agg"
                
            if configure_file_exists_return_value == "exists":
                db_config_return_value = self._check_cron_in_db_config_unconfig(path,ss_name,configure_file_name,agg_or_raw,agg_or_raw_value,install_type)
        
            if unconfigure_file_exists_return_value == "exists":
                db_unconfig_return_value = self._check_cron_in_db_config_unconfig(path,ss_name,unconfigure_file_name,agg_or_raw,agg_or_raw_value,install_type)
        
            if db_config_return_value[0] == "pass" and db_unconfig_return_value[0] == "pass":
                return_flag.append(True)
                cron_str_values.append(db_config_return_value[1])
            else:
                return_flag.append(False)
                cron_str_values.append(db_config_return_value[1])
                
        for flag in return_flag:
            if flag is True:
                count +=1
                
        if count == len(return_flag):
            cron_str_values.insert(0,True)
        else:
            cron_str_values.insert(0,False)
            
        return cron_str_values
        
        
    def _check_cron_in_db_config_unconfig(self, path, ss_name, file_name,agg_or_raw,agg_or_raw_value,install_type):
        return_value = []
        string_for_grep1 = '%s_CBO_P%s'%(ss_name.upper(),agg_or_raw.upper())
        if agg_or_raw == "raw" and install_type == "rc":
            string_for_grep2 = '%s_PMC'%ss_name.upper()
        elif agg_or_raw == "raw" and install_type == "gc":
            string_for_grep2 = '%s_RAW'%ss_name.upper()
        elif agg_or_raw == "agg":
            string_for_grep2 = '%s_AGG'%ss_name.upper()
            
        print "***INFO*** Check the cron statement in %s \n"%file_name
        print_str = self.ssh.execute_command('find %s -name "%s" | xargs grep -e "^[[:blank:]]*execute.*%s"| grep -i \'%s\''%(path,file_name,string_for_grep1,string_for_grep2))
        sed_return_value = self.ssh.execute_command('find %s -name "%s" | xargs grep -e "^[[:blank:]]*execute.*%s"| grep -i \'%s\' | sed \'s/.*\\\\\\\\\\\\"\([^"]*\)\\\\\\\\\\\\".*/\\1/\' | awk -F \'&&\' \'{print $2}\''%(path,file_name,string_for_grep1,string_for_grep2))
        str_for_cronjob = self.ssh.execute_command('find %s -name "%s" | xargs grep -e "^[[:blank:]]*execute.*%s"| grep -i \'%s\' | awk -F \\\' \'{print $2}\''%(path,file_name,string_for_grep1,string_for_grep2))
    
        str_after_split = sed_return_value.split()
        
        str_for_cronjob = str_for_cronjob.replace('\\','')
            
        print "********** The grep output from %s is **********\n%s\n"%(file_name,print_str)
        
        if agg_or_raw.lower() == "raw":
            ss_name = '%sraw'%ss_name
            
        if len(str_after_split) == 2 and agg_or_raw_value == "1":
            if str_after_split[0] == PetOptimize.new_script_for_add and str_after_split[1] == ss_name.lower():
                print "***INFO*** The %s %s have been added in %s\n"%(PetOptimize.new_script_for_add, ss_name.lower(), file_name)
                return_value = ["pass",str_for_cronjob]
            else:
                print "***ERROR*** The %s %s not add correctly in %s\n"%(PetOptimize.new_script_for_add, ss_name.lower(), file_name)
                return_value = ["fail",str_for_cronjob]
        elif len(str_after_split) != 2 and agg_or_raw_value == "1":
            print "***ERROR*** The %s %s not add correctly in %s\n"%(PetOptimize.new_script_for_add, ss_name.lower(), file_name)
            return_value = ["fail",str_for_cronjob]
        
        if agg_or_raw_value == "0":
            if sed_return_value.strip() == "":
                print "***INFO*** %s %s not added in %s as the correspoding value in general config is 0\n"%(PetOptimize.new_script_for_add, ss_name.lower(), file_name)
                return_value = ["pass",str_for_cronjob]
            else:
                print "***ERROR*** Forbid to add %s %s in %s as the correspoding value in general config is 0\n"%(PetOptimize.new_script_for_add, ss_name.lower(), file_name)
                return_value = ["fail",str_for_cronjob]
        return return_value
    
    
    def _check_file_exists(self,path,file_name):
        ls_return_value = self.ssh.execute_command('ls %s | grep %s'%(path,file_name),return_rc=True)
        if ls_return_value[1] == 0:
            print "***INFO*** File %s exists in path %s \n"%(file_name,path)
            return "exists"
        else:
            print "***ERROR*** File %s not exists in path %s \n"%(file_name,path)
            return "not exists"
    
    
    def check_oracle_cronjob_statement(self,cronjob_str_arr,oracle_alias='onepm_cs1_oracle'):
        return_values = []
        cronjob_arr = []
        count = 0
        self.ssh.switch_connection(oracle_alias)
        if cronjob_str_arr[0] is True or cronjob_str_arr[0] is False:
            cronjob_str_arr.pop(0)
        for cronjob_str in cronjob_str_arr:
            str_for_grep = cronjob_str.replace("*","\*")
            contab_grep_return_value = self.ssh.execute_command('crontab -l | grep -E \'(%s)\''%str_for_grep,return_rc=True)
            print contab_grep_return_value
            if contab_grep_return_value[1] == 0:
                print "***INFO*** %s exists in crontab lists\n"%cronjob_str
                return_values.append(True)
            else:
                print "***ERROR*** %s not exists in crontab lists\n"%cronjob_str
                return_values.append(False)
                
        for value in return_values:
            if value is True:
                count +=1
                
        if count == len(return_values):
            return True
        else:
            return False
        
    
    def clear_local_tmp_env(self):
        if os.path.exists(PetOptimize.local_file_dir):
            shutil.rmtree(PetOptimize.local_file_dir)
            print "***INFO*** All the temp file have been deleted\n"
        else:
            print "***INFO*** temp file not exist, no need to clear\n"
                
                    
    def close_ssh_sessions(self):
        print "***INFO*** Execute to close all the ssh connection session"
        self.ssh.close_all_connections()
        
    
        
        
        