import sys
import os
import re
import random
import shutil
import tempfile


class PropertyValueSetting:
    _ssh = None
    @property

    def ssh(self):
        return PropertyValueSetting._ssh
    
    def set_ssh(self, value):
        PropertyValueSetting._ssh = value
        print("*DEBUG* ssh set")

    def set_property_value_in_general_config_file(self,configfile_path,property_name,substitution_value='null'):
        substitution_string = ""
        tmp_value = substitution_value.lower()
        if tmp_value == "null":
            substitution_string = ""
        elif tmp_value == "empty":
            substitution_string = "(%s            \"\")" %property_name
        elif tmp_value == "space":
            substitution_value = "  "
            substitution_string = "(%s            \"%s\")" %(property_name,substitution_value)
        else:
            substitution_value_slash = substitution_value.replace("/","\/")
            substitution_string = "(%s            \"%s\")" %(property_name,substitution_value_slash)
        
        
        returnlist = self.ssh.execute_command('grep -w %s < %s' %(property_name,configfile_path), return_rc=True)
        print "the %s in general config file is defined as %s"%(property_name, returnlist)
        if returnlist[1] == 0:
            output1 = self.ssh.execute_command('sed -i \'s/.*%s .*/%s/\' %s' %(property_name,substitution_string,configfile_path),return_rc=True)
            if output1[1] == 0:
                print "***INFO*** Modify the %s value with %s successful\n" %(property_name,substitution_value)
                return True
            else:
                print "***ERROR*** Modify the %s value with %s failed\n" %(property_name,substitution_value)
                return False
            
        elif returnlist[1] != 0 and substitution_string != "":
            output2 = self.ssh.execute_command('sed -i \'$a %s\' %s' %(substitution_string,configfile_path),return_rc=True)
            if output2[1] == 0:
                print "***INFO*** Append the %s value with %s successful\n" %(property_name,substitution_value)
                return True
            else:
                print "***ERROR*** Append the %s value with %s failed\n" %(property_name,substitution_value)
                return False
        else:
            print "****INFO*** Try to set the %s with null value (not set %s in general config file)"%(property_name,property_name)
            print "***INFO*** No need to modify the general config file as the %s not exists in this file\n"%property_name
            return True

    def close_ssh_sessions(self):
        print "***INFO*** Execute to close all the ssh connection session"
        self.ssh.close_all_connections()
