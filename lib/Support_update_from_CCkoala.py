# -*- coding: cp936 -*-
'''
Created on Sep 4, 2014

@author: l2sun
'''
from SSHLibrary import SSHLibrary
import time,os
from os import listdir
class UpdateFromCCKoala:
        _ssh = None
        ss_registry = set()
        @property
        def ssh(self):
                return UpdateFromCCKoala._ssh
        def set_ssh(self, value):
                UpdateFromCCKoala._ssh = value
                print("*DEBUG* ssh set")                
        def upload_koala_metadata_and_rpm_packages(self,
                                                ss_remote_path,
                                                ss='NOKKTT',
                                                switch='on',
                                                alias='onepm_cs1_root',
                                                koala_input_path='metadata'
                                                ):
            rpm_packages=[]
            koala_input_path = "%s%s%s" % (os.path.dirname(os.path.dirname(__file__)), os.path.sep, koala_input_path)
            print "koala_input_path : %s" %koala_input_path            
            koala_file_folder = '%s%s%s' % (koala_input_path, os.path.sep, ss)  
            print "koala_file_folder :%s" %koala_file_folder        
            self.ssh.switch_connection(alias)
            koala_input_file = '%s%s*.*' % (koala_file_folder, os.path.sep)
            source=koala_file_folder
            target_dir=ss_remote_path
            filelist = listdir(source)
            for name in filelist:
                srcFilename = source + os.path.sep + name
                desFilename = target_dir +os.path.sep+ name
                time.sleep(1)
                '''switch on for copy rpm to $rpm_path''' 
                if switch=='on':
                    self.ssh.put_file( srcFilename,desFilename)
                    contain=name.find('.rpm') 
                    if contain>=0:
                        rpm_packages.append(name)
                else:
                    if name.find('.cf')>0 or name.find('.xml')>0:
                        self.ssh.put_file( srcFilename,desFilename)
                    else:
                        continue                        
            self.ssh.execute_command('chown -R omc:sysop ..%s' % ss_remote_path)
            time.sleep(1)
            '''switch on for copy rpm to $rpm_path, ID_repositories to related directory''' 
            if switch=='on':
                rpm_path='/var/opt/nokia/oss/global/rtekoa/work/RPM/noarch/'
                self.ssh.execute_command('mkdir /var/opt/nokia/oss/global/rtekoa/work/repositories/%s' %ss.lower())
                '''move rpm packages to rpm_path directory'''
                for m in rpm_packages:
                    self.ssh.execute_command('mv %s/%s %s/%s' %(ss_remote_path,m,rpm_path,m))
                self.ssh.execute_command('mv %s/noksun_IDRepository.dat /var/opt/nokia/oss/global/rtekoa/work/repositories/%s/%s_IDRepository.dat' %(ss_remote_path,ss.lower(),ss.lower()))
                self.ssh.execute_command('chown -R omc:sysop  /var/opt/nokia/oss/global/rtekoa/work/repositories/')
                files=self.ssh.execute_command('ls %s' % rpm_path)
                print files
                for i in range(len(rpm_packages)):
                    package_name=rpm_packages[i]
                    rpm_packages[i]=rpm_path+package_name
            self.ssh.execute_command("cd %s;perl -pi -e 's;\\(KOALAFileName(\\s*)\".*/(\\w*)\.xml\"\\);(KOALAFileName\\1\"'`pwd`'/\\2.xml\");' %sGeneralConfiguration.cf" % (ss_remote_path,
                                                                                                                                                              ss.lower()))            
            time.sleep(1)
            UpdateFromCCKoala.ss_registry = set([ss.upper()]) | UpdateFromCCKoala.ss_registry            
            return rpm_packages

        




