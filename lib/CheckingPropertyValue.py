'''
Created on Nov 3, 2014

@author: danting
'''
from SSHLibrary import SSHLibrary

class PropertyValueChecking:
    _ssh = None
    @property

    def ssh(self):
        return PropertyValueChecking._ssh
    
    def set_ssh(self, value):
        PropertyValueChecking._ssh = value
        print("*DEBUG* ssh set")

    def check_property_value(self,property_name,file_path,find_str,value):
        #property_name means the cron entry name
        #file_path means the .configure file path
        #find_str means the related progress
        #value means the setting value in cf file and it's the value we should check
        returnlist = self.ssh.execute_command('grep -i "%s" < %s' %(find_str,file_path))
        #print "the %s in %s file is defined as %s \n"%(find_str, file_path, returnlist)

        output = returnlist.find(value)
        if output != -1:
            print "***INFO*** The %s value \"%s\" is correct!\n" %(property_name,value)
            return True
        else:
            print "***ERROR*** The %s value is incorrect!\n" %(property_name)
            return False

    def close_ssh_sessions(self):
        print "***INFO*** Execute to close all the ssh connection session"
        self.ssh.close_all_connections()

#pv=PropertyValueChecking()
#ssh=SSHLibrary()
#ssh.open_connection("10.92.17.1")
#ssh.login('omc','omc')
#pv.set_ssh(ssh)
#pv.check_property_value("DimensionIndexRebuildCronEntry","/var/tmp/rtekoa/integrationTool/nokkoo/INSTALL/Nokia-UMAKOO-NOKKOO-DB.configure","mdbcbo_analyse.sh nokkooraw -NON_PARTITION 10 1","30 2 * * 1")
