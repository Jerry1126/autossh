import sys
import os
import re
import random
import shutil
import tempfile
import paramiko
#import pexpect

rand = random.Random()
temp_path = tempfile.gettempdir()
BuDs_ip = '10.8.136.68'
BuDs_username = 'Adapuser1'
BuDs_passwd = 'AcEla901'

class OMeSGenerateAndAgg:
    scripts_name = 'pmdata_factory.pl'
    local_file = '%s%s%s'%(temp_path,os.path.sep,'data_factory.tar.gz')
    copy_source_file = '/home/Adapuser1/tony/data_factory.tar.gz'
    copy_destination_file = '/tmp/tmp%s%s%s'%(rand.randint(0, 2 ** 30),'/','data_factory.tar.gz')
#    copy_cmd = 'scp Adapuser1@10.8.136.68:/home/Adapuser1/tony/data_factory.tar.gz /home/omc/k6_chen/'
    _ssh = None
    @property
    def ssh(self):
        return OMeSGenerateAndAgg._ssh
        
    def set_ssh(self, value):
        OMeSGenerateAndAgg._ssh = value
        print("*INFO* ssh set")

    def run_pmdata_tool(self,ssname,scname,data_insert_row_number,root_alias='onepm_cs1_root'):
        return_value_final = ""
        pmdata_execute_flag = ""
        ssname = ssname.lower()
        scname = scname.lower()
        self.ssh.switch_connection(root_alias)
        return_value_whereis = self.ssh.execute_command('whereis %s'%OMeSGenerateAndAgg.scripts_name)
        m = re.match(r'\w+:\S+',return_value_whereis.replace(' ',''))
        if m:
            pmdata_execute_flag = "run"
            print "*INFO* mdata_factory.pl have been installed already,  begin to generate OMeS data\n"
#            return_value_final = self._insert_data_to_table(ssname,scname,data_insert_row_number)
        else:
            print "*INFO* mdata_factory.pl not installed, please wait for install...\n"
            return_value_install2 = self._install_pmdata_tool(BuDs_ip,BuDs_username,BuDs_passwd)
            if return_value_install2 == "pass":
                pmdata_execute_flag = "run"
#                return_value_final = self._insert_data_to_table(ssname,scname,data_insert_row_number)
#        print "The return value is ",return_value_final

        if pmdata_execute_flag == "run":
            return_value_final = self._insert_data_to_table(ssname,scname,data_insert_row_number)
            
        return return_value_final
    
        
        
    def run_cosprcmx(self,db_prefix,agg_date='None',omc_alias='onepm_cs1_omc'):
        self.ssh.switch_connection(omc_alias)
        return_value_cosprc = ""
        if agg_date == 'None':
            return_value_cosprc = self.ssh.execute_command('cosprcmx.pl -dm %s -a -s -e -t 9'%db_prefix,return_rc=True)
        else:
            return_value_cosprc = self.ssh.execute_command('cosprcmx.pl -dm %s -a -s %s -e -t 9'%(db_prefix,agg_date),return_rc=True)
        
        print return_value_cosprc[0]
        
        if return_value_cosprc[1] == 0:
            print "*INFO* Cosprc execute successful!\n"
            return "pass"
        else:
            print "*ERROR* Cosprc running met some error!\n"
            return "failed"


    def _install_pmdata_tool(self,host_ip,username,password):
        return_value_scp = self._remote_scp(host_ip=host_ip,username=username,password=password)
        if return_value_scp == "failed":
            return "failed"
        else:
            return_value_install = self._extract_and_install()
            if return_value_install == "failed":
                return "failed"
            else:
                return "pass"
            
    
        
    def _insert_data_to_table(self,ssname,scname,data_insert_row_number):
        delimiter = ','    
        return_value_pmdata = self.ssh.execute_command('%s -ss %s -sc %s -t %s' %(OMeSGenerateAndAgg.scripts_name,ssname,scname,data_insert_row_number))
        print return_value_pmdata
        new_string = delimiter.join(return_value_pmdata.split('\n'))
#        print new_string
        m = re.match(r'.*%s row inserted,Data generated!!'%data_insert_row_number,new_string,re.I)
        if m:
            print "*INFO* %s rows data have been inserted, please check the DB!\n"%data_insert_row_number
            return "pass"
        else:
            print "*ERROR* Insert to DB met some error, plese find the root cause!\n"
            return "failed"


        
        
    
    def _remote_scp(self,host_ip,username,password):
        t = paramiko.Transport((host_ip,22))
        t.connect(username=username,password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        src = OMeSGenerateAndAgg.copy_source_file
        des = OMeSGenerateAndAgg.local_file
        print src
        print des
        sftp.get(src,des)
        t.close
        
        if os.path.exists(des):
            print "*INFO* Copy data_factory.tar.gz from BuDs server successful!\n"
            remote_file = OMeSGenerateAndAgg.copy_destination_file
            self.ssh.put_file(des,remote_file)
            return_value_file_exsit = self.ssh.execute_command('if [ -f %s ]; then echo "exists"; else echo "not found"; fi;'%remote_file)
            print return_value_file_exsit
            if return_value_file_exsit.strip() != "exists":
                print "*ERROR* Copy data_factory.tar.gz to current Lab met error!\n"
                return "failed"
            else:
                print "*INFO* Copy data_factory.tar.gz to current Lab successful!\n" 
                return "pass"
        else:
            print "*ERROR* Copy data_factory.tar.gz from BuDs server met error!\n"
            return "failed"
    
    
    def _extract_and_install(self):
        install_dir = os.path.dirname(OMeSGenerateAndAgg.copy_destination_file)
        extract_file = os.path.basename(OMeSGenerateAndAgg.copy_destination_file)
        self.ssh.execute_command('cd %s;tar -xzvf %s;perl pmfactory_install.pl'%(install_dir,extract_file))
        return_value_whereis2 = self.ssh.execute_command('whereis %s'%OMeSGenerateAndAgg.scripts_name)
        m = re.match(r'\w+:\S+',return_value_whereis2.replace(' ',''))
        if m:
            print "*INFO* mdata_factory.pl have been installed successful!\n"
            return "pass"
        else:
            print "*ERROR* mdata_factory.pl installing failed!\n"
            return "failed"

       
    def clear_tmp_env(self,root_alias='onepm_cs1_root'):
        flag = "pass"
        self.ssh.switch_connection(root_alias)

        if os.path.isfile(OMeSGenerateAndAgg.local_file):
            os.remove(OMeSGenerateAndAgg.local_file)
            print "*INFO* All the temp file in local have been deleted\n"
        else:
            print "*INFO* Local temp file not exist, no need to clear\n"
            
        self.ssh.execute_command('rm -rf %s'%os.path.dirname(OMeSGenerateAndAgg.copy_destination_file))
        return_value_dir_exist = self.ssh.execute_command('if [ -d %s ]; then echo "exists"; else echo "not found"; fi;'%os.path.dirname(OMeSGenerateAndAgg.copy_destination_file))
        if return_value_dir_exist.strip() != "exists":
            print "*INFO* All the temp file in remote have been deleted!\n"
        else:
            print "*ERROR* Remote temp file delete failed!\n" 
            flag = "failed"
        return flag
        