# -*- coding: cp936 -*-
'''
Created on Sep 4, 2014

@author: l2sun
'''
from SSHLibrary import SSHLibrary
import re
class OracleInsallationEnhance:
        _ssh = None
        @property
        def ssh(self):
                return OracleInsallationEnhance._ssh
        def set_ssh(self, value):
                OracleInsallationEnhance._ssh = value
                print("*DEBUG* ssh set")                
        def get_filepath_without_installation(self,ss):
            '''Fabricate the output file($ssrapsysrcmx.cf.cf) path'''
            filepath=""
            filepath="/var/tmp/rtekoa/integrationTool/"+ss+"/"+ss+"cdb/"
            output_file_name=ss+"cdb_cre_pdprivileges.sql"
            filepath+=output_file_name
            return filepath
        def previliges_version_check(self,ssname,filepath,version='new'):
            result=""
            flag=False
            privilege_expected=[]
            privilege_old=[]
            view_table_name=ssname[-3:]+"_ps_working_sets"
            #grep '^[[:blank:]]*GRANT[[:blank:]]*SELECT[[:blank:]]*ON[[:blank:]]*ktt_ps_working_sets' nokkttcdb_cre_pdprivileges.sql
            cmd="grep '^[[:blank:]]*GRANT[[:blank:]]*SELECT[[:blank:]]*ON[[:blank:]]*%s' %s" %(view_table_name,filepath)
            result=self.ssh.execute_command(cmd)
            privilege_expected=['GRANT SELECT ON %s TO &readUser;' %view_table_name, 'GRANT SELECT ON %s TO &writeUser;' %view_table_name, 'GRANT SELECT ON %s TO omc WITH GRANT OPTION;' %view_table_name]
            privilege_old=['GRANT SELECT ON %s TO &readUser;' %view_table_name, 'GRANT SELECT,UPDATE, INSERT, DELETE ON %s TO &writeUser;' %view_table_name, 'GRANT SELECT,UPDATE, INSERT, DELETE ON %s TO omc WITH GRANT OPTION;' %view_table_name]
            # Convert the previliges commands as a list
            result_list_type=result.split('\n')  # Now the last element is empty
            if version=="new":
                if result_list_type==privilege_expected:
                    print "*INFO* The privileges commands are the current version,the commands are %s" %privilege_expected
                    flag=True
                else:
                    print "*INFO* The privileges commands are not same as expected one: %s, but the actual one is %s" %(privilege_expected,result_list_type)
            elif version=="old":
                if result_list_type==privilege_old:
                    print "*INFO* The privileges commands are the old version,the commands are %s" %privilege_old
                else:
                    print "*INFO* The old privileges commands does not exist,the old privileges commands are %s,but the finnal privileges commands are %s" %(privilege_old,result_list_type)
            print flag
            return flag
                

        




