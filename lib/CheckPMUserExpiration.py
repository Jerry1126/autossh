'''
Created on Jul 28, 2014

'''
import re,time
import os.path
class CheckPMUserExpiration:
    def __init__(self):
        pass
    
    @property
    def ssh(self):
        return self._ssh
    
    def set_ssh(self, value):
        self._ssh = value
        print("*DEBUG* ssh set")
        
    @property
    def db(self):
        return self._db
    
    def set_db(self, value):
        self._db = value
        print("*DEBUG* db set")
        
    def upload_koala_input_and_general_config_to_cs(self,alias='root'):
        self.ssh.switch_connection(alias)
        self.ssh.execute_command('mkdir -f /tmp/koala/nokktt')
        time.sleep(1)
        koala_file_folder="%s%s%s%s%s"%(os.path.dirname(os.path.dirname(__file__)),os.path.sep,'metadata',os.path.sep,'NOKKTT')
        self.ssh.put_file('%s%s%s'%(koala_file_folder,os.path.sep,'nokkttGeneralConfiguration.cf'), '/tmp/koala/nokktt/nokkttGeneralConfiguration.cf')
        time.sleep(1)
        self.ssh.put_file('%s%s%s'%(koala_file_folder,os.path.sep,'nokkttKoala.xml'), '/tmp/koala/nokktt/nokkttKoala.xml')
        time.sleep(1)
        self.ssh.execute_command('chown -R omc:sysop /tmp/koala/')
        time.sleep(1)
        self.ssh.execute_command("cd /tmp/koala/nokktt/;perl -pi -e 's;\\(KOALAFileName(\\s*)\".*/(\\w*)\.xml\"\\);(KOALAFileName\\1\"'`pwd`'/\\2.xml\");' nokkttGeneralConfiguration.cf")
        time.sleep(1)
        
    def build_test_pm_package(self,alias='omc',time_out='300'):
        self.ssh.switch_connection(alias)
        self.ssh.write('cd /tmp/koala/nokktt;koartemx.pl -g nokkttGeneralConfiguration.cf -rpm')
        def read_response(response,time_stamp):
            time.sleep(3)
            rs=self.ssh.read()
            print "*INFO* %s"%rs
            rss=rs.splitlines()
            result=response+rss
            last_line=rss[-1] if len(rss)>0 else ''
            if(re.match('.*>\s*$',last_line)):
                self.ssh.write('n');
                print "*FAIL* PM package build failed."
            if(not re.match('\[omc@[^\[\]]*\]\$\s*$',last_line)):
                if(time.time()-time_stamp>time_out):
                    print "*FAIL* deal out put time out"
                else:
                    result=read_response(result,time_stamp)
            return result
        response=read_response([],time.time())
        print "*INFO* %s"%("\n".join(response))
        rpms=map(lambda x:re.match('Wrote:\s*(/var/opt/nokia/oss/global/rtekoa/work/RPM/noarch/[\w\.-]*.rpm)',x).groups()[0],
                 filter(lambda x:re.match('Wrote:\s*/var/opt/nokia/oss/global/rtekoa/work/RPM/noarch/[\w\.-]*.rpm',x),
                        response))
        return rpms
         
    def install_test_pm_package(self,rpms,ds_address,alias='root'):
        result=False
        self.ssh.switch_connection(alias)
        cmd='cd /packages/install/rpm/;ls|grep -i nokktt|xargs rm -f;%s'%(";".join(map(lambda x:'cp %s ./'%x,rpms)))
        cmd='%s;/opt/nokia/oss/itools/bin/adap_install.sh nokktt -i 2>1'%cmd
        rs=self.ssh.execute_command(cmd)
        print "*INFO* %s"%rs
        time.sleep(1)
        rss=self.ssh.execute_command('/usr/bin/nokia/ManageSS.pl --list UMAKTT NOKKTT').splitlines()
        ac=filter(lambda x:re.match('[\w\-\d\.]*\s*\(CONFIGURED\)\s*\(ACTIVATED\)\s*\(ACTIVE\)', x),rss)
        if(len(ac)>0):
            time.sleep(1)
            rss=self.ssh.execute_command('ssh %s /usr/bin/nokia/ManageSS.pl --list UMAKTT NOKKTT-DB'%ds_address).splitlines()
            ac=filter(lambda x:re.match('[\w\-\d\.]*\s*\(CONFIGURED\)\s*\(ACTIVATED\)\s*\(ACTIVE\)', x),rss)
            if(len(ac)>0):
                result=True
        return result
    
    def uninstall_test_pm_package(self,ds_address,alias='root'):
        result=False
        self.ssh.switch_connection(alias)
#        time.sleep(1)
        rs=self.ssh.execute_command('/opt/nokia/oss/itools/bin/adap_install.sh nokktt -u 2>1')
        print "*INFO* %s"%rs
#        time.sleep(1)
        rss=self.ssh.execute_command('/usr/bin/nokia/ManageSS.pl --list UMAKTT NOKKTT').splitlines()
        if(len(rss)==0):
#            time.sleep(1)
            rss=self.ssh.execute_command('ssh %s /usr/bin/nokia/ManageSS.pl --list UMAKTT NOKKTT-DB'%ds_address).splitlines()
            if(len(rss)==0):
                result=True
        return result
    def get_user_expire_lock_and_profile_info(self,username):
        result=(None,None,None)
        rs=self.db.get_rows("select to_char(EXPIRY_DATE,'yyyy-mm-dd'),to_char(LOCK_DATE,'yyyy-mm-dd'),PROFILE from dba_users where USERNAME='%s'"%username.upper())
        if(len(rs)==1):
            result=map(lambda x:x if x is not None else '',rs[0])
        else:
            print "*FAIL* db user %s not exists"%username
        return result
    
    def try_login_db_with_user(self,username,password):
        rs=self.ssh.execute_command("echo 'exit;'|sqlplus -L %s/%s"%(username,password)).splitlines()
        print "*INFO* command response"%rs
        err_lines=filter(lambda x:re.match("ORA-\d+:.*", x),rs)
        err_numbers=()
        if(len(err_lines)>0):
            err_numbers=tuple(map(lambda x:re.match("ORA-(\d+):.*",x).groups()[0],err_lines))
        return err_numbers;
    
    def lock_db_user(self,username,db_system_password="manager"):
        rs=self.ssh.execute_command("echo 'alter user %s account lock;'|sqlplus system/%s"%(username,db_system_password)).splitlines()
        if(len(filter(lambda x:re.match('User altered.',x),rs))<1):
            print "*FAIL* db user %s not locked!"%username
            
    def unlock_db_user(self,username,db_system_password="manager"):
        rs=self.ssh.execute_command("echo 'alter user %s account unlock;'|sqlplus system/%s"%(username,db_system_password)).splitlines()
        if(len(filter(lambda x:re.match('User altered.',x),rs))<1):
            print "*FAIL* db user %s not unlocked!"%username
            
    def expire_db_user(self,username,db_system_password='manager'):
        rs=self.ssh.execute_command("echo 'alter user %s password expire;'|sqlplus system/%s"%(username,db_system_password)).splitlines()
        if(len(filter(lambda x:re.match('User altered.',x),rs))<1):
            print "*FAIL* db user %s not expired!"%username
            
    def change_db_user_password(self,username,new_password,db_system_password='manager'):
        rs=self.ssh.execute_command("echo 'alter user %s identified by %s;'|sqlplus system/%s"%(username,new_password,db_system_password)).splitlines()
        if(len(filter(lambda x:re.match('User altered.',x),rs))<1):
            print "*FAIL* password of db user %s not changed!"%username
            
    def get_db_user_encrypted_password(self,username,db_sys_password="manager"):
        rs=self.ssh.execute_command("echo \"select password from user$ where name='%s';\"|sqlplus sys/%s as sysdba"%(username.upper(),db_sys_password)).splitlines()
        print "*INFO* %s"%"\n".join(rs)
        def deal_rs(result,line):
            tmp_rs=result
            if result.get('status', None) =='END':
                tmp_rs=result
            elif(result.get('status',None) is None):
                if(re.match("^SQL>\s*$",line)):
                    tmp_rs={'status':'SQL','passowrd_value':None}
                else:
                    tmp_rs={'status':None,'passowrd_value':None}
            elif(result.get('status',None)=='SQL'):
                print "*INFO* result=%s"%result
                if(re.match("^PASSWORD\s*$",line)):
                    tmp_rs={'status':'PASSWORD','passowrd_value':None}
                else:
                    tmp_rs={'status':None,'passowrd_value':None}
            elif(result.get('status',None)=='PASSWORD'):
                if(re.match("^-*\s*$",line)):
                    tmp_rs={'status':'HYPHEN','passowrd_value':None}
                else:
                    tmp_rs={'status':None,'passowrd_value':None}
            elif(result.get('status',None)=='HYPHEN'):
                m=re.match('^\s*(\S*)\s*$',line)
                if(m):
                    tmp_rs={'status':'END','passowrd_value':m.groups()[0]}
                else:
                    tmp_rs={'status':None,'passowrd_value':None}
            else:
                tmp_rs={'status':None,'passowrd_value':None}
            return tmp_rs
        password=reduce(deal_rs,
                        rs,
                        {'status':None,
                         'passowrd_value':None}).get('passowrd_value',
                                                     None)
        if password is None or password=='':
            print "*FAIL* user %s not exists!"%username
        return password
    
    def restore_db_user_password(self,username,encrypted_password,db_system_password='manager'):
        rs=self.ssh.execute_command("echo \"alter user %s identified by values '%s';\"|sqlplus system/%s"%(username,encrypted_password,db_system_password)).splitlines()
        if(len(filter(lambda x:re.match('User altered.',x),rs))<1):
            print "*FAIL* password of db user %s not restored!"%username
    
