import os.path
import SSHLibrary
import string
import BuiltIn
import time
import Constants
import paramiko

class CommonFunctions_Koala:

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    
    def __init__(self):
        print "initial..."
    
    def get_koaversion (self,text):
        if (text.find('Nokia-UMAKOA-RTEKOA-5.0')==-1):
            return -1;
        else:
            return text[24:31]

    def get_koala_tar (self):
        print 'get_koala_tar started'
        cd_path = '/buds/programs/oss5.3cd2/originalbuilds/OSS_CD_3858/'
        cdlist_command='ls /buds/programs/oss5.3cd2/originalbuilds/OSS_CD_3858/'
        self.ssh.open_connection(Constants.BUDS[0])
        self.ssh.login(Constants.BUDS[1], Constants.BUDS[2])            
        cdlist=self.ssh.execute_command(cdlist_command)
        print cdlist
        if cdlist is not None:
            print cdlist.rfind('OSS_CD_3858')
            cd_num=cdlist[cdlist.rfind('OSS_CD_3858'):cdlist.rfind('OSS_CD_3858')+15]
            print cd_num
            tar_path=cd_path+cd_num+'/tar/'
            print tar_path
            tar_name=cdlist=self.ssh.execute_command('ls '+ tar_path)
            print tar_name
            tar_location=tar_path+tar_name
            return tar_location
        else:
            return -1

    def get_file_name(self,text):
        if text is not None:
            return text[text.rfind('/OSS'):text.rfind('z')+1]
        else:
            return -1

    def get_rpm_package(self, host, user, password, command):
        print 'get_rpm_package started'
        self.ssh.open_connection(host)
        self.ssh.login(user, password)      
        return self.ssh.execute_command(command)

    def Trim(self, command):
        print 'INFO*'+command

        return command.strip()

    def get_cosprc_date(self,text):
        if text is not None:
            return text[len(text)-19:len(text)-10]
        else:
            return -1

    def get_log_file(self, files):
        if files is not None:
            return files[files.rfind('cusrta'):len(files)]
        else:
            return -1

    def execute_koala_regular(self, host, user, password, command):
        print 'INFO*'+command
        s = paramiko.Transport((host, 22))
        s.connect(username=user, password=password)
        chan = s.open_session()
        chan.get_pty()
        chan.invoke_shell()
        chan.send(command+'\n')
        chan.send('\n')
        chan.send('\n')
        time.sleep(100)
        result=chan.recv(1000000)
        print 'INFO*'+result
        chan.send('\n')
        chan.send('\n')
        chan.close()
        s.stop_thread()
        s.close()
        return result
    
    def execute_koala_upgrade(self, host, user, password, command):
        print 'INFO*'+command
        s = paramiko.Transport((host, 22))
        s.connect(username=user, password=password)
        chan = s.open_session()
        chan.get_pty()
        chan.invoke_shell()
        chan.send(command+'\n')
        time.sleep(15)
        print 'INFO*'+chan.recv(10000)
        chan.send('\n')
        time.sleep(15)
        print 'INFO*'+chan.recv(10000)
        chan.send('\n')
        time.sleep(200)
        result = chan.recv(1000000)
        print 'INFO*'+result
        chan.send('\n')
        time.sleep(30)
        print 'INFO*'+chan.recv(10000)
        chan.send('\n')
        time.sleep(30)
        print 'INFO*'+chan.recv(10000)
        chan.close()
        s.stop_thread()
        s.close()
        return result
    
    def execute_ds_deactivate(self, host, user, password, command):
        print 'INFO*'+command

        self.ssh.open_connection(host)
        self.ssh.login(user, password)      
        dc = self.ssh.execute_command(command)
        while dc.count('ERROR:') != 0:
            dc = self.ssh.execute_command(command)
            print dc
        else:
            print 'Go ON!'
        
    def check_contain_views(self, views, measid):
        print 'INFO*' + views
        print 'INFO*' + measid

        result = 'PASS'
        check_list = self.get_exist_list(measid)
        for i in range(0,len(check_list)):
            if views.find(check_list[i]) != -1 :
                continue
            else:
                print check_list[i]+ ' NONEXISTED'
                result = 'FAIL'
                break

        nresult = 'PASS'
        check_nonlist=self.get_nonexist_list(measid)              
        for i in range(0,len(check_nonlist)):
            if views.find(check_nonlist[i]) == -1 :                
                continue
            else:
                res=views[views.find(check_nonlist[i]):views.find(check_nonlist[i])+30]
                print res
                if res.find('_BHQ')!=-1:                    
                    continue
                elif res.find('_WEEKBH')!=-1:    
                    continue
                elif res.find('_HOURQ')!=-1:
                    continue
                else:
                    print check_nonlist[i] + ' EXISTED'
                    nresult = 'FAIL'
                    break
            
        if (result=='PASS' and nresult=='PASS'):
            return 'PASS'
        else:
            return 'FAIL'
       
    def get_exist_list(self, measid):
        if measid=='SERV2':
			print Constants
            #print Constants.__file__
            return Constants.SERV2_VIEWS_EXIST
        if measid=='TPBHQ':
            return Constants.TPBHQ_VIEWS_EXIST
        if measid=='POFF':
            return Constants.POFF_VIEWS_EXIST
        if measid=='QPBH':
            return Constants.QPBH_VIEWS_EXIST
        if measid=='FMING':
            return Constants.FMING_VIEWS_EXIST
        if measid=='FMOFF':
            return Constants.FMOFF_VIEWS_EXIST
        if measid=='FMBH':
            return Constants.FMBH_VIEWS_EXIST
        if measid=='TTL':
            return Constants.TTL_VIEWS_EXIST
        if measid=='TTLOFF':
            return Constants.TTLOFF_VIEWS_EXIST
        if measid=='ECONE':
            return Constants.ECONE_VIEWS_EXIST
        if measid=='ECTWO':
            return Constants.ECTWO_VIEWS_EXIST
        if measid=='ECTHR':
            return Constants.ECTHR_VIEWS_EXIST
        if measid=='ECFIVE':
            return Constants.ECFIVE_VIEWS_EXIST        
        if measid=='EXTTL':
            return Constants.EXTTL_VIEWS_EXIST
        if measid=='QPBHOFF':
            return Constants.QPBHOFF_VIEWS_EXIST
        if measid=='FMBHOFF':
            return Constants.FMBHOFF_VIEWS_EXIST
        if measid=='UPUSE':
            return Constants.UPUSE_VIEWS_EXIST
        if measid=='QPSBH':
            return Constants.QPSBH_VIEWS_EXIST
        if measid=='QPBHSBH':
            return Constants.QPBHSBH_VIEWS_EXIST
        if measid=='FMSBH':
            return Constants.FMSBH_VIEWS_EXIST
        if measid=='FMBHSBH':
            return Constants.FMBHSBH_VIEWS_EXIST
        if measid=='TTLSBH':
            return Constants.TTLSBH_VIEWS_EXIST
        if measid=='ECFOUR':
            return Constants.ECFOUR_VIEWS_EXIST
        if measid=='ECSIX':
            return Constants.ECSIX_VIEWS_EXIST
        if measid=='SYNONMS':
            return Constants.ECSIX_VIEWS_NONEXIST
        #For new standard adaptation
##        if measid=='FCELLR':
##            return Constants.FCELLR_VIEWS_EXIST
##        if measid=='HWRES':
##            return Constants.HWRES_VIEWS_EXIST
##        if measid=='HWROFF':
##            return Constants.HWROFF_VIEWS_EXIST
##        if measid=='HWRBH':
##            return Constants.HWRBH_VIEWS_EXIST
##        if measid=='HBOFF':
##            return Constants.HBOFF_VIEWS_EXIST
##        if measid=='CPUT':
##            return Constants.CPUT_VIEWS_EXIST
##        if measid=='CPUTBH':
##            return Constants.CPUTBH_VIEWS_EXIST
##        if measid=='CPUTOFF':
##            return Constants.CPUTOFF_VIEWS_EXIST
##        if measid=='CBOFF':
##            return Constants.CBOFF_VIEWS_EXIST
##        if measid=='FANS':
##            return Constants.FANS_VIEWS_EXIST
##        if measid=='FANSOFF':
##            return Constants.FANSOFF_VIEWS_EXIST
##        if measid=='FANS3':
##            return Constants.FANS3_VIEWS_EXIST
##        if measid=='FANS4':
##            return Constants.FANS4_VIEWS_EXIST
##        if measid=='FANS5':
##            return Constants.FANS5_VIEWS_EXIST
##        if measid=='FANS6':
##            return Constants.FANS6_VIEWS_EXIST
        
    def get_nonexist_list(self, measid):
        if measid=='SERV2':
            return Constants.SERV2_VIEWS_NONEXIST
        if measid=='TPBHQ':
            return Constants.TPBHQ_VIEWS_NONEXIST
        if measid=='POFF':
            return Constants.POFF_VIEWS_NONEXIST
        if measid=='QPBH':
            return Constants.QPBH_VIEWS_NONEXIST
        if measid=='FMING':
            return Constants.FMING_VIEWS_NONEXIST
        if measid=='FMOFF':
            return Constants.FMOFF_VIEWS_NONEXIST
        if measid=='FMBH':
            return Constants.FMBH_VIEWS_NONEXIST
        if measid=='TTL':
            return Constants.TTL_VIEWS_NONEXIST
        if measid=='TTLOFF':
            return Constants.TTLOFF_VIEWS_NONEXIST
        if measid=='ECONE':
            return Constants.ECONE_VIEWS_NONEXIST
        if measid=='ECTWO':
            return Constants.ECTWO_VIEWS_NONEXIST
        if measid=='ECTHR':
            return Constants.ECTHR_VIEWS_NONEXIST
        if measid=='ECFIVE':
            return Constants.ECFIVE_VIEWS_NONEXIST         
        if measid=='EXTTL':
            return Constants.EXTTL_VIEWS_NONEXIST
        if measid=='QPBHOFF':
            return Constants.QPBHOFF_VIEWS_NONEXIST
        if measid=='FMBHOFF':
            return Constants.FMBHOFF_VIEWS_NONEXIST
        if measid=='UPUSE':
            return Constants.UPUSE_VIEWS_NONEXIST
        if measid=='QPSBH':
            return Constants.QPSBH_VIEWS_NONEXIST
        if measid=='QPBHSBH':
            return Constants.QPBHSBH_VIEWS_NONEXIST
        if measid=='FMSBH':
            return Constants.FMSBH_VIEWS_NONEXIST
        if measid=='FMBHSBH':
            return Constants.FMBHSBH_VIEWS_NONEXIST
        if measid=='TTLSBH':
            return Constants.TTLSBH_VIEWS_NONEXIST
        if measid=='ECFOUR':
            return Constants.ECFOUR_VIEWS_NONEXIST
        if measid=='ECSIX':
            return Constants.ECSIX_VIEWS_NONEXIST
    #For new standard adaptation
##        if measid=='FCELLR':
##            return Constants.FCELLR_VIEWS_NONEXIST
##        if measid=='HWRES':
##            return Constants.HWRES_VIEWS_NONEXIST
##        if measid=='HWROFF':
##            return Constants.HWROFF_VIEWS_NONEXIST
##        if measid=='HWRBH':
##            return Constants.HWRBH_VIEWS_NONEXIST
##        if measid=='HBOFF':
##            return Constants.HBOFF_VIEWS_NONEXIST
##        if measid=='CPUT':
##            return Constants.CPUT_VIEWS_NONEXIST
##        if measid=='CPUTBH':
##            return Constants.CPUTBH_VIEWS_NONEXIST
##        if measid=='CPUTOFF':
##            return Constants.CPUTOFF_VIEWS_NONEXIST
##        if measid=='CBOFF':
##            return Constants.CBOFF_VIEWS_NONEXIST
##        if measid=='FANS':
##            return Constants.FANS_VIEWS_NONEXIST
##        if measid=='FANSOFF':
##            return Constants.FANSOFF_VIEWS_NONEXIST
##        if measid=='FANS3':
##            return Constants.FANS3_VIEWS_NONEXIST
##        if measid=='FANS4':
##            return Constants.FANS4_VIEWS_NONEXIST
##        if measid=='FANS5':
##            return Constants.FANS5_VIEWS_NONEXIST
##        if measid=='FANS6':
##            return Constants.FANS6_VIEWS_NONEXIST
        
    def Verification(self, errors, errno, measurement,formu='test'):
        errormsg=''
        if errno=='713':
            errormsg = "713: Measurement '"+measurement+"'"  
        elif errno=='714':
            errormsg="714: Measurement '"+measurement+"'"  
        elif errno=='715':
            errormsg="715: Measurement '"+measurement+"'"  
        elif errno=='716':
            errormsg="716: Measurement '"+measurement+"'"  
        elif errno=='717':
            errormsg="717: Measurement '"+measurement+"'"  
        elif errno=='718':
            errormsg="718: Measurement '"+measurement+"'"  
        elif errno=='719':
            errormsg="719: Measurement '"+measurement+"'"  
        elif errno=='720':
            errormsg="720: Measurement '"+measurement            
        elif errno=='721':
            errormsg="721: Measurement '"+measurement           
        elif errno=='722':
            errormsg="722: Measurement '"+measurement
        elif errno=='723':
            errormsg="723: Measurement '"+measurement  
        elif errno=='724':
            errormsg="724: Measurement '"+measurement  
        elif errno=='725':
            errormsg="725: Measurement '"+measurement  
        elif errno=='726':
            errormsg="726: Measurement '"+measurement              
        elif errno=='727':
            errormsg="727: Measurement '"+measurement              
        elif errno=='728':
            errormsg="728: Measurement '"+measurement  
        elif errno=='729':
            errormsg="729: Measurement '"+measurement+"'"           
        elif errno=='730':
            errormsg="730: Measurement '"+measurement+"'"
        elif errno=='731':
            errormsg="731: BusyHour rule type : '"+measurement+"'"
        elif errno=='732':
            errormsg="732: Measurement '"+measurement+"' SkipStandardLevels should be 'NONE'"
        elif errno=='733':
            errormsg="733: Measurement '"+measurement+"' aggregation rule is :'"
        elif errno=='734':
            errormsg="734: Measurement '"+measurement+"' 's SynMapMeas measurement"
        elif errno=='735':
            errormsg="735: Measurement '"+measurement+"' Aggregation rule should set to 'ALL'"
##        elif errno=='442':
##            errormsg="442: '"+measurement+"' Busy Hour formula '"+formu+"'"
        elif errno=='620':
            errormsg = "620: Level '"+measurement.upper()+"' and its child level '"+formu.upper()+"'"
        else:
            errormsg=''

        print 'ERROR: '+errormsg

        if errors.find(errormsg)!=-1:
            return 'PASS'
        else:
            return 'FAIL'

    def check_synonms(self, synonms):
        print "Synonms:" + synonms
        result = 'PASS'
        for i in range(0,len(Constants.CHECK_SYNONMS)):
            if synonms.find(Constants.CHECK_SYNONMS[i]) != -1 :
                continue
            else:
                print Constants.CHECK_SYNONMS[i]+ ' NONEXISTED'
                result = 'FAIL'
                break
            
        return result
    def generate_sql(self, colume, table):
        print "Checked colume name:" + colume
        print "Checked table name:" + table

        sql= "select column_name from all_tab_columns where table_name='"+table.upper()+"' and column_name='"+colume.upper()+"';"

        print "INFO* SQL:" + sql

        return sql
    
    def check_ref_counter(self, aim, result):
        res = 'PASS'

        if aim.upper()!=result.upper():
            res='FAIL'

        return res


        

            
