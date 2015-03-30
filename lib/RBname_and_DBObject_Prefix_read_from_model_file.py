# -*- coding: cp936 -*-
'''
Created on Sep 4, 2014

@author: l2sun
'''
from SSHLibrary import SSHLibrary
import re
from xml.dom import minidom
class RBandDBprefixReadFrom:
        _ssh = None
        @property
        def ssh(self):
                return RBandDBprefixReadFrom._ssh
        def set_ssh(self, value):
                RBandDBprefixReadFrom._ssh = value
                print("*DEBUG* ssh set")     
        def retrieve_DBObjectPrefix_or_RBNameSpacePrefix(self,ss_remote_path,ss="nokktt"):
            '''Retrieve the DBObjectPrefix value from metadatafile'''
            Prefix_list=['DatabaseObjectPrefix','RBNamespacePrefix']
            DBObjectPrefix=self.ssh.execute_command("awk -F\'[:/(||:/)||:/\"]\' \'/.*%s.*/{print $3}\' %s/%sGeneralConfiguration.cf" %(Prefix_list[0],ss_remote_path,ss))
            RBNamePrefix=self.ssh.execute_command("awk -F\'[:/(||:/)||:/\"]\' \'/.*%s.*/{print $3}\' %s/%sGeneralConfiguration.cf" %(Prefix_list[1],ss_remote_path,ss))
            return {'DBObjectPrefix':DBObjectPrefix,'RBNamePrefix':RBNamePrefix} 
        
        def fabricate_conf_file_without_DBobjectPrefix_and_RBname(self,ss_remote_path,ss="nokktt"):
            '''fabricate configure file without RBNamespacePrefix and DBObjectPrefix'''
            result=self.ssh.execute_command("sed -i \'/.*DatabaseObjectPrefix.*$/d\' %s/%sGeneralConfiguration.cf;sed -i \'/.*RBNamespacePrefix.*$/d\' %s/%sGeneralConfiguration.cf" %(ss_remote_path,ss,ss_remote_path,ss))
            return result
        def retrieve_configure_file(self,ss_remote_path,ss="nokktt"):
            '''Retrieve the file path of the expected file'''
            result="%s/%sGeneralConfiguration.cf" %(ss_remote_path,ss)
            return result
        def edit_dedicated_line_content(self,originalContent,file,newContent=""):
            '''Edit dedicated line content which contain dedicated content'''
            for i in range(len(originalContent)):
                if newContent=="None":
                    print "New content is set to be None"
                    result=self.ssh.execute_command("sed -in-place -e 's/%s.*/%s     )/g' %s" %(originalContent[i],originalContent[i],file))
                else:
                    result=self.ssh.execute_command("sed -in-place -e 's/%s.*/%s     %s)/g' %s" %(originalContent[i],originalContent[i],newContent,file))
            return result

        def comment_dedicated_line(self,content,file):
            '''comment the line which contain the dedicated content'''
            for i in range(len(content)):
                result=self.ssh.execute_command("sed -in-place -e 's/.*%s.*/#&/g' %s" %(content[i],file))
            return result
        
        def check_model_or_info_file_exist_or_not(self,installFalg="True",sc="umaktt",ss="nokktt",fileType="info"):
            '''Check whether ssname.model file or ssname.info file exist or not in conf directory'''
            if installFalg=="True":
                if fileType=="info":
                    Filepath="/opt/nokia/oss/%s-5.0-%s-1.0.0/conf/addon/%s.info" %(sc,ss,ss)
                    FileName="%s.info" %ss
                else:
                    Filepath="/opt/nokia/oss/%s-5.0-%s-1.0.0/conf/addon/%s.model" %(sc,ss,ss)
                    FileName="%s.model" %ss
            else:
                if fileType=="info":
                    Filepath="/var/tmp/rtekoa/integrationTool/%s/conf/%s.info" %(ss,ss)
                    FileName="%s.info" %ss
                else:
                    Filepath="/var/tmp/rtekoa/integrationTool/%s/conf/%s.model" %(ss,ss)
                    FileName="%s.model" %ss
            rs=self.ssh.execute_command('if [ -e %s ]; then echo \'The %s file exists\'; else echo \'The %s file does not exist\'; fi' %(Filepath,FileName,FileName))
            print rs
            if re.match(r'The\s\w+.\w+ file exists',rs):
                FileExistflag=True
            elif re.match(r'The\s\w+.\w+ file does not exist',rs):
                FileExistflag=False
            print "FileExistflag is %s" %FileExistflag
            return FileExistflag

        def prefix_of_RBName_and_DBObject_in_model_or_info_file(self,newContent,fileType,operation="check",installFlag="True",sc="umaktt",ss="nokktt"):
            '''Check whether RBNameSpacePrefix and DBObjectPrefix in info file or modify these items in model or info file'''
            filepath=""
            print "FileType in function prefix_of_RBName_and_DBObject_in_model_or_info_file is %s" %fileType
            if installFlag=="True":
                filepath="/opt/nokia/oss/umaktt-5.0-nokktt-1.0.0"
                if fileType=="info":
                    infoFilepath="/opt/nokia/oss/%s-5.0-%s-1.0.0/conf/addon/%s.info" %(sc,ss,ss)
                elif fileType=="model":
                    modelFilepath="/opt/nokia/oss/%s-5.0-%s-1.0.0/conf/addon/%s.model" %(sc,ss,ss)
            else:
                filepath="/var/tmp/rtekoa/integrationTool/%s/conf" %ss
                if fileType=="info":
                    infoFilepath="/var/tmp/rtekoa/integrationTool/%s/conf/%s.info" %(ss,ss)
                elif fileType=="model":
                    modelFilepath="/var/tmp/rtekoa/integrationTool/%s/conf/%s.model" %(ss,ss)
            ConfFileName="%s.model" %ss
            if fileType=="info":
                DBObjectPrefix=self.ssh.execute_command("awk  -F\'[:/>||:/,]\' \'/DatabasePrefix/{print $2}\' %s|awk -F\"[:/\']\" \'/\w*/{print $2}\'" %infoFilepath)
                RBNamePrefix=self.ssh.execute_command("awk -F\'[:/>||:/,]\' \'/RBNamespacePrefix/{print $2}\' %s|awk -F\"[:/\']\" \'/\w*/{print $2}\'" %infoFilepath)
                if operation=="modify":
                    if newContent=="Space":
                        result=self.ssh.execute_command("sed -in-place -e 's/%s/ /g' %s" %(DBObjectPrefix,infoFilepath))
                    else:
                        result=self.ssh.execute_command("sed -in-place -e 's/%s/%s/g' %s" %(DBObjectPrefix,newContent,infoFilepath))
            elif fileType=="model":
                DBObjectPrefix=self.ssh.execute_command("awk -F\'[:/>||:/<]\' \'/.*DatabasePrefix.*/{print $3}\' %s" %modelFilepath)
                RBNamePrefix=self.ssh.execute_command("awk -F\'[:/>||:/<]\' \'/.*ReportBuilderPrefix.*/{print $3}\' %s" %modelFilepath)
                if operation=="modify":
                    result=self.ssh.execute_command("sed -in-place -e 's/%s/%s/g' %s" %(DBObjectPrefix,newContent,modelFilepath)) 
            print "operation is %s" %operation
            if operation=="check":
                return {'DBObjectPrefix':DBObjectPrefix,'RBNamePrefix':RBNamePrefix} 
            else:
                return result
            
        def check_RBName_and_DBObject_in_model_or_info_file(self,fileType,installFlag="True",sc="umaktt",ss="nokktt"):
            '''Check whether RBNameSpacePrefix and DBObjectPrefix in info file'''
            print "FileType in function check_RBName_and_DBObject_in_model_or_info_file is %s" %fileType
            operation="check"
            newContent="omit"
            RBandDBprefixChecker=RBandDBprefixReadFrom()
            Prefix_RBNameSpace_DBObject=RBandDBprefixChecker.prefix_of_RBName_and_DBObject_in_model_or_info_file(newContent,fileType,operation,installFlag,sc="umaktt",ss="nokktt")
            print "FileType in function check_RBName_and_DBObject_in_model_or_info_file x is %s" %fileType
            return Prefix_RBNameSpace_DBObject
        
        def modify_DBObjectPrefix_RBNamePrefix_in_model_or_info_file(self,replacedContent,sc="umaktt",ss="nokktt",fileType="info"):
            '''Modify DBobjectPrefix and RBNamePrefix in model or info file'''
            operation="modify"
            installFalg="True"
            RBandDBprefixChecker=RBandDBprefixReadFrom()
            execute_result=RBandDBprefixChecker.prefix_of_RBName_and_DBObject_in_model_or_info_file(replacedContent,fileType,operation,installFalg,sc="umaktt",ss="nokktt")    
            return execute_result
        
        def delete_info_file_after_installation(self,sc="umaktt",ss="nokktt"):
            '''Delete ssname.info file in conf/addon directory'''
            filepath=""
            filepath="/opt/nokia/oss/umaktt-5.0-nokktt-1.0.0"
            modelFileName="%s.info" %ss
            modelFilepath="/opt/nokia/oss/%s-5.0-%s-1.0.0/conf/addon/%s.info" %(sc,ss,ss)
            rs=self.ssh.execute_command('if [ -e %s ]; then echo \'The %s file exists\'; else echo \'The %s file does not exist\'; fi' %(modelFilepath,modelFileName,modelFileName))
            if re.match(r'The\s\w+.\w+ file exists',rs):
                result=self.ssh.execute_command('rm %s' %modelFilepath)
            else:
			    result="The info file does not exist!"
            return result
        
        def Check_RBnamePrefix_and_DBPrefix_in_synonymsFile(self,ss,DBPrefix,baseSSname="nokktt"):
            '''Check whether RBnamePrefix and DBPrefix is same as the setting in metadata file'''
            filePath="/var/tmp/rtekoa/integrationTool/%s/%srdb/" %(ss,ss)
            fileName="%srdb_cre_synonyms.sql" %ss
            DBPrefixFoundout=""
            DefaultPrefixFoundout=""
            rs=self.ssh.execute_command('cat %s/%s' %(filePath,fileName))
            tables_with_DBPrefix=self.ssh.execute_command(" grep -i '^[[:blank:]]*for' %s%s" %(filePath,fileName))
            print tables_with_DBPrefix
            print type(DBPrefix)
            #DBPrefixvalue="cus"+DBPrefix['DBObjectPrefix'][-3:]
            DBPrefixvalue=DBPrefix['DBObjectPrefix']
            print "DBPrefixvalue is %s" %DBPrefixvalue
            if DBPrefixvalue!='':
                pattern="FOR\s*(\w*)(.+)%s_(\w*)" %DBPrefixvalue
                print type(pattern)
                DBPrefixFoundout=re.search(pattern,tables_with_DBPrefix)
                print "DBPrefixFoundout is %s" %DBPrefixFoundout
            else:
                print DefaultPrefixFoundout
                DBPrefixFoundout=''
                #print DBPrefixFoundout
                pattern="FOR\s*(\w*)(.+)%s_(\w*)" %baseSSname
                DefaultPrefixFoundout=re.search(pattern,tables_with_DBPrefix)
                print "DefaultPrefixFoundout is %s" %DefaultPrefixFoundout
            if(DBPrefixFoundout is not None and DefaultPrefixFoundout is None):
                flag=True
            else:
                flag=False
                #print type(DefaultPrefixFoundout)
            return flag