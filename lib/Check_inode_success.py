# -*- coding: cp936 -*-
'''
Created on Sep 4, 2014

@author: l2sun
'''
from SSHLibrary import SSHLibrary
class InodeSuccess:
        _ssh = None
        @property
        def ssh(self):
                return InodeSuccess._ssh
        def set_ssh(self, value):
                InodeSuccess._ssh = value
                print("*DEBUG* ssh set")                
        def del_the_ss_directory_if_exist(self,ss):
            '''The function is used for inode TA case'''
            filepath=""
            result=""
            filepath="/var/tmp/rtekoa/integrationTool/"+ss
            result=self.ssh.execute_command('if [ -e %s ]; then echo \'The directory exists\'; else echo \'The directory does not exist\'; fi' %(filepath))
            if result=='The directory exists':
                sdout= self.ssh.execute_command(' rm %s -r' %filepath)
            
        def check_whether_ss_directory_exsit(self,ss,version):
            '''The function is used for inode TA case'''
            filepath=""
            rs=""
            print "Enter the function"
            if version=="old":
                filepath="/home/omc/integrationTool/"+ss
                print "old version filepath is %s" %filepath
            elif version=="new":
                filepath="/var/tmp/rtekoa/integrationTool/"+ss
                print "new version filepath is %s" %filepath
            rs=self.ssh.execute_command('if [ -e %s ]; then echo \'The directory exists\'; else echo \'The direcotry does not exists\'; fi' %filepath )
            print "the result is %s" %rs
            return rs
        




