'''
Created on Aug 4, 2014

@author: j19li
'''
import time, os, re, random
rand = random.Random()
koalaRTE_working_dir = '/var/opt/nokia/oss/global/rtekoa/work'
koalaRTE_release_dir = '%s/%s' % (koalaRTE_working_dir, 'releases')
koalaRTE_upgrades_dir = '%s/%s' % (koalaRTE_working_dir, 'upgrades')
koalaRTE_repositories_dir = '%s/%s' % (koalaRTE_working_dir, 'repositories')
build_ack_mapping = {'Do you want to store this report to a file? y/n [n]':'n',
                     'Do you want to store this report to a file ? y/n [y]':'n',
                        'Do you want to accept this changes? y/n [y]':'y'}
cs_info = ''
ds_info = ''

class KoalaRTE:
    ss_registry = set()
    ss_build_dirs = set()
    rpm_registry = set()
    model_file_store_dir = '/tmp/koala_model/'
    koala_remote_path = '/tmp/koala_%s' % rand.randint(0, 2 ** 30)
    _ssh = None
    @property
    def ssh(self):
        return KoalaRTE._ssh
    
    def set_ssh(self, value):
        KoalaRTE._ssh = value
        print("*DEBUG* ssh set")
    def upload_koala_input_and_general_config_to_cs(self,
                                                    ss='NOKKTT',
                                                    alias='onepm_cs1_root',
                                                    koala_input_path='metadata'
                                                    ):
        koala_input_path = "%s%s%s" % (os.path.dirname(os.path.dirname(os.path.dirname(__file__))), os.path.sep, koala_input_path)
        ss_remote_path = '%s/%s' % (KoalaRTE.koala_remote_path, ss.lower())
        koala_file_folder = '%s%s%s' % (koala_input_path, os.path.sep, ss)
        self.ssh.switch_connection(alias)
        self.ssh.execute_command('mkdir -f %s' % ss_remote_path)
        time.sleep(1)
        koala_input_file = '%s%s%s' % (koala_file_folder, os.path.sep, self.get_koala_input_file_name(ss))
        general_configure = '%s%s%s' % (koala_file_folder, os.path.sep, self.get_general_config_file_name(ss))
        self.ssh.put_file(general_configure, '%s/%s' % (ss_remote_path, self.get_general_config_file_name(ss)))
        time.sleep(1)
        self.ssh.put_file(koala_input_file, '%s/%s' % (ss_remote_path, self.get_koala_input_file_name(ss)))
        time.sleep(1)
        self.ssh.execute_command('chown -R omc:sysop %s' % KoalaRTE.koala_remote_path)
        time.sleep(1)
        self.ssh.execute_command("cd %s;perl -pi -e 's;\\(KOALAFileName(\\s*)\".*/(\\w*)\.xml\"\\);(KOALAFileName\\1\"'`pwd`'/\\2.xml\");' %s" % (ss_remote_path,
                                                                                                                                                  self.get_general_config_file_name(ss)))
        time.sleep(1)
        # Modify some parameter values related crontab job in generalconfig file
        ch=time.localtime(time.time()).tm_hour
        cron_map={'DimensionIndexRebuildCronEntry':6,'AggIndexRebuildCronEntry':5,'AggIndexMaintainCronEntry':9,'RawIndexMaintainCronEntry':2,'RawIndexRebuildCronEntry':3,'PartitionManagerCronEntry':1,'DimensionCleanCronEntry':7,'RawIndexMaintainFullCronEntry':8,'AggIndexMaintainCronEntryGC':4}        
        mn=min(cron_map.values())
        mxn=max(cron_map.values())
        step=rand.randint(1,10)
        ns=map(lambda x:ch - step -x if ch - step -x>=0 else 24 + ch - step -x,range(mn,mxn+1))
        cmd="sed -i %s"%" ".join(map(lambda x:r"-e 's/\((%s.*\"[0-9][0-9]*\) [0-9][0-9]* \(.*)\)/\1 %s \2/'"%(x,ns[cron_map[x]-mn]),cron_map.keys()))
        cmd = "cd %s;%s %s" %(ss_remote_path,cmd,self.get_general_config_file_name(ss))
        print cmd
        self.ssh.execute_command(cmd)
        time.sleep(1)
        KoalaRTE.ss_registry = set([ss.upper()]) | KoalaRTE.ss_registry
    def clear_ss_environment(self, alias='onepm_cs1_root'):
        self.ssh.switch_connection(alias)
        cmd = 'rm -rf %s' % KoalaRTE.koala_remote_path
        print "*INFO* %s" % cmd
        self.ssh.execute_command(cmd)
        cmd = ';'.join(map(lambda x:'rm -rf %s' % x, KoalaRTE.ss_build_dirs))
        print "*INFO* %s" % cmd
        self.ssh.execute_command(cmd)
        cmd = ';'.join(map(lambda x:'rm -rf %s' % x, KoalaRTE.rpm_registry))
        print "*INFO* %s" % cmd
        self.ssh.execute_command(cmd)
        cmd = 'cd %s;%s' % (koalaRTE_release_dir, ';'.join(map(lambda x:'ls|grep %s|xargs rm -rf' % x.lower(), KoalaRTE.ss_registry)))
        print "*INFO* %s" % cmd
        self.ssh.execute_command(cmd)
        cmd = 'cd %s;%s' % (koalaRTE_upgrades_dir, ';'.join(map(lambda x:'ls|grep %s|xargs rm -rf' % x.lower(), KoalaRTE.ss_registry)))
        print "*INFO* %s" % cmd
        self.ssh.execute_command(cmd)
        cmd = 'cd %s;%s' % (koalaRTE_repositories_dir, ';'.join(map(lambda x:'ls|grep %s|xargs rm -rf' % x.lower(), KoalaRTE.ss_registry)))
        print "*INFO* %s" % cmd
        self.ssh.execute_command(cmd)
        '''to be done'''
    def _run_koartemx(self, ss_remote_path, general_config, return_print, time_out, **args):
        _args = dict(map(lambda x:(x[0], x[1] if x[1] is not None else ''),
                         args.items()))
        self.ssh.write('cd %s;koartemx.pl -g %s %s' % (ss_remote_path,
                                                       general_config,
                                                       reduce(lambda x, y:'%s %s' % (x,
                                                                                     '-%s %s' % (y,
                                                                                                 _args.get(y))),
                                                              _args.keys(),
                                                              '')))
        def read_response(response, time_stamp):
            time.sleep(3)
            rs = self.ssh.read()
            rss = rs.splitlines()
            result = response + rss
            last_line = rss[-1] if len(rss) > 0 else ''
            if(re.match('.*>\s*$', last_line)):
                m = re.match('^\s*(\S.*\S)\s*>\s*$', last_line)
                notice=m.groups()[0] if m is not None else ''
                ack = build_ack_mapping.get(notice, None)
                if(ack is not None):
                    self.ssh.write(ack)
                else:
                    raise AssertionError(" Not Defined ack type '%s'." % notice)
                    self.ssh.write(chr(3))
            if(not re.match('\[omc@[^\[\]]*\]\$\s*$', last_line)):
                if(time.time() - time_stamp > time_out):
                    raise AssertionError(" deal out put time out")
                else:
                    result = read_response(result, time_stamp)
            return result
        response = read_response([], time.time())
        print "*INFO* %s" % ("\n".join(response))
        adap_dirs = filter(lambda x:re.match('Output\s*directory:\s*[\w\/]*\s*$', x),
                        response)
        adap_dir = map(lambda x:re.match('Output\s*directory:\s*([\w\/]*)\s*$', x).groups()[0],
                     adap_dirs)[0] if len(adap_dirs) > 0 else None
        KoalaRTE.ss_build_dirs = KoalaRTE.ss_build_dirs | (set([adap_dir]) if adap_dir is not None else set())

        def check_response(env, line):
            result = env
            status = env.get('status', None)
            if(status is None):
                if(re.match('^\s*=+\s*$', line)):
                    result = dict(result, **{'status':'S'})
            elif(status == 'S'):
                if(re.match('^\s*=+\s*$', line)):
                    result = dict(result, **{'status':None})
                elif(re.match('^\s*(\d+)\s*Errors\s*found\s*$', line)):
                    print '*INFO* %s' %line
                    error_cnt = int(re.match('^\s*(\d+)\s*Errors\s*found\s*$', line).groups()[0])
                    if(error_cnt > 0):
                        result = dict(result, **{'build_success':False})
            return result
        rs=reduce(check_response, response, {'status':None, 'build_success':True})
        print '*INFO* %s' %rs
        build_success = rs.get('build_success', True)
        #if((not build_success) and (not bool(return_print))):
        if(not build_success and return_print == str(False)):
            raise AssertionError("adaptation build failed")
        return response

    def get_ss_remote_path(self, ss):
        ss_remote_path = '%s/%s' % (KoalaRTE.koala_remote_path, ss.lower())
        return ss_remote_path

    def get_ss_path_after_installation(self,sc,ss):
        '''Fabricate the SS path with installation'''
        sspath="/etc/opt/nokia/oss/"+sc+"-5.0"
        return sspath
    
    def get_ss_path_without_installation(self,ss):
        '''Fabricate the ss path without installation'''
        sspath="/var/tmp/rtekoa/integrationTool/"+ss
        return sspath


    def get_general_config_file_name(self, ss):
        general_config = '%sGeneralConfiguration.cf' % ss.lower()
        return general_config
    def get_general_config_file_path(self,ss):
        return '%s/%s'%(self.get_ss_remote_path(ss),self.get_general_config_file_name(ss))
    def get_koala_input_file_name(self, ss):
        koala_input = '%sKoala.xml' % ss.lower()
        return koala_input
    def get_koala_input_file_path(self,ss):
        return '%s/%s'%(self.get_ss_remote_path(ss),self.get_koala_input_file_name(ss))
    
    def build_test_pm_package(self,
                              ss='NOKKTT',
                              alias='onepm_cs1_omc',
                              time_out='300',return_print=False):
        print_str = ""
        return_list = []
        self.ssh.switch_connection(alias)
        ss_remote_path = self.get_ss_remote_path(ss)
        general_config = self.get_general_config_file_name(ss)
        response = self._run_koartemx(ss_remote_path, general_config, return_print, time_out, rpm='')
        rpms = map(lambda x:re.match('Wrote:\s*([\w\.\-\/]*.rpm)', x).groups()[0],
                 filter(lambda x:re.match('Wrote:\s*[\w\.\-\/]*.rpm', x),
                        response))
        
        for value in response:
            print_str += value + "\n"
        KoalaRTE.rpm_registry = KoalaRTE.rpm_registry | set(rpms)
        print "*INFO* rpms_:%s" % rpms
        if (return_print == str(True)):
            return_list.append(rpms)
            return_list.append(print_str)
            return return_list
        else:
            return rpms
    def release_run_on_ss(self,
                          ss,
                          alias='onepm_cs1_omc',
                          time_out='300'):
        self.ssh.switch_connection(alias)
        ss_remote_path = self.get_ss_remote_path(ss)
        general_config = self.get_general_config_file_name(ss)
        self._run_koartemx(ss_remote_path, general_config, False, time_out, rel='')
    def unrelease_run_on_ss(self,
                            ss,
                            alias='onepm_cs1_omc',
                            time_out='300'):
        self.ssh.switch_connection(alias)
        ss_remote_path = self.get_ss_remote_path(ss)
        general_config = self.get_general_config_file_name(ss)
        self._run_koartemx(ss_remote_path, general_config, False, time_out, unrel='')
    def _install_rpms_as_rc(self, SS):
        cmd = '/opt/nokia/oss/itools/bin/adap_install.sh %s -i 2>1' % (SS)
        rs = self.ssh.execute_command(cmd)
        print "*INFO* %s" % rs
    def _install_rpms_as_gc(self,cs_rpm,ds_rpm,check_log):
        global cs_info
        global ds_info
        stdout=[]
        ds1_node=self.ssh.execute_command("ldapacmx.pl -pkgPrimaryNode db")
        cluster_type=self.ssh.execute_command('/usr/bin/nokia/IFWGetData.pl --ClusterType')
        if(cluster_type!='global'):
            rs=self.ssh.execute_command('echo /opt/nokia/oss/itools/bin/change_cluster_type.sh global|ssh %s'%ds1_node)
            print '*INFO* %s'%rs
            if(self.ssh.execute_command('/usr/bin/nokia/IFWGetData.pl --ClusterType')!='global'):
                raise AssertionError("can't switch cluster to global")
        cs_nodes=self.ssh.execute_command('/usr/bin/nokia/IFWGetData.pl --PhysicalHostForRole BACKEND').splitlines()
        ds_nodes=self.ssh.execute_command('/usr/bin/nokia/IFWGetData.pl --PhysicalHostForRole DSS').splitlines()
        for ds_node in ds_nodes:
            rs=self.ssh.execute_command('echo /usr/bin/nokia/installmx -task INSTALL -pkg %s|ssh %s'%(ds_rpm,ds_node),return_stdout=True,return_rc=True)
            print '*INFO* %s'%rs
            stdout.append(rs[0])
            if (rs[1]==0):
                rs=self.ssh.execute_command('echo /usr/bin/nokia/installmx -task CONFIGURE -pkg %s|ssh %s'%(ds_info,ds_node),return_rc=True)
                print '*INFO* %s'%rs
                stdout.append(rs[0])
                if (rs[1]==0):
                    rs=self.ssh.execute_command('echo /usr/bin/nokia/installmx -task ACTIVATE -pkg %s|ssh %s'%(ds_info,ds_node),return_rc=True)
                    print '*INFO* %s'%rs
                    stdout.append(rs[0])
        for cs_node in cs_nodes:
            rs=self.ssh.execute_command('echo /usr/bin/nokia/installmx -task INSTALL -pkg %s|ssh %s'%(cs_rpm,cs_node),return_rc=True)
            print '*INFO* %s'%rs
            if (rs[1]==0):
                rs=self.ssh.execute_command('echo /usr/bin/nokia/installmx -task CONFIGURE -pkg %s|ssh %s'%(cs_info,cs_node),return_rc=True)
                print '*INFO* %s'%rs
                if (rs[1]==0):
                    rs=self.ssh.execute_command('echo /usr/bin/nokia/installmx -task ACTIVATE -pkg %s|ssh %s'%(cs_info,cs_node),return_rc=True)
                    print '*INFO* %s'%rs
        if(cluster_type!='global'):
            rs=self.ssh.execute_command('echo /opt/nokia/oss/itools/bin/change_cluster_type.sh %s|ssh %s'%(cluster_type,ds1_node))
            print '*INFO* %s'%rs
            if(self.ssh.execute_command('/usr/bin/nokia/IFWGetData.pl --ClusterType')!=cluster_type):
                raise AssertionError("can't switch cluster to %s"%cluster_type)
        if (check_log=='True'):
            print '*INFO* %s' %stdout
            start_time=re.findall('\d*-\d*-\d*\s\d*:\d*:\d*\\|I\\|START', stdout[0])
            ending_time=re.findall('\d*-\d*-\d*\s\d*:\d*:\d*\\|A\\|OK',stdout[-1])
            if len(ending_time) == 0:
                ending_time=re.findall('\d*-\d*-\d*\s\d*:\d*:\d*\\|A\\|ERROR',stdout[-1])
				
            self.ssh.execute_command('echo \"sed -n \'/%s/,/%s/p\' /var/log/installmx.log >/tmp/tmplog.txt\" | ssh %s' %(start_time[0],ending_time[0],ds_node)) 
            warning_info=self.ssh.execute_command("echo \"grep -i 'warning' /tmp/tmplog.txt\" | ssh %s" %ds_node)
            print '*INFO* %s' %warning_info
            warnings=filter(lambda x:re.match(r'^[\w\s\[\]\/\.]+$', x), warning_info.splitlines())
            print '*INFO* %s' %warning_info.splitlines()
            self.ssh.execute_command(" echo \"rm /tmp/tmplog.txt -rf\" | ssh %s" %ds_node)
            if warnings:
                raise AssertionError("There are warnings reported %s" %warnings)
            else:
                print '*INFO* There are no warnings related insert/update/drop table/view,other warnings are %s' %warnings  
    def install_test_pm_package(self, rpms, ds_address, alias='onepm_cs1_root',cluster_type='rc',check_log='False'):
        result = False
        global cs_info
        global ds_info
        print "*INFO* rpms:%s" % rpms
        if(len(rpms) != 2):
            raise AssertionError("the numberof rpm must be 2")
        else:
            def match_rpm(rpm):
                m = re.match('.*/Nokia-(\w*)-(\w*)(-DB){0,1}-([\d\-\.]*).noarch.rpm', rpm)
                g = m.groups() if m is not None else None
                return {'SC':g[0] if g is not None else None,
                        'SS':g[1] if g is not None else None,
                        'isDB':True if (g[2] if g is not None else None) == '-DB' else False,
                        'version':g[3] if g is not None else None}
            rpms_info = map(match_rpm, rpms)
            print "*INFO* rpms_info:%s" % rpms_info
            if(rpms_info[0]['SC'] == rpms_info[1]['SC'] and rpms_info[0]['SC'] is not None 
               and rpms_info[0]['SS'] == rpms_info[1]['SS'] and rpms_info[0]['SS'] is not None 
               and (rpms_info[0]['isDB'] ^ rpms_info[1]['isDB'])
               and rpms_info[0]['version'] == rpms_info[1]['version'] and rpms_info[0]['version'] is not None):
                self.ssh.switch_connection(alias)
                SS = rpms_info[0]['SS'].lower()
                cmd = 'cd /packages/install/rpm/;ls|grep -i %s|xargs rm -f;%s' % (SS, ";".join(map(lambda x:'cp %s ./' % x, rpms)))
                rs = self.ssh.execute_command(cmd)
                print "*INFO* %s" % rs
                if(cluster_type=='rc'):
                    self._install_rpms_as_rc(SS)
                elif(cluster_type=='gc'):
                    cs_package = rpms[0] if rpms_info[0]['isDB'] == False else rpms[1]
                    cs_info = re.search('Nokia-(\w*)-(\w*)-\d.\d',cs_package).group()
                    ds_package = rpms[0] if rpms_info[0]['isDB'] == True else rpms[1]
                    ds_info = re.search('Nokia-(\w*)-(\w*)-DB-\d.\d',ds_package).group()
                    self._install_rpms_as_gc(cs_package,ds_package,check_log)
                else:
                    raise AssertionError("Illegal cluster_type:%s"%cluster_type) 
                time.sleep(1)
                rss = self.ssh.execute_command('/usr/bin/nokia/ManageSS.pl --list %s %s' % (rpms_info[0]['SC'], rpms_info[0]['SS'])).splitlines()
                ac = filter(lambda x:re.match('[\w\-\d\.]*\s*\(CONFIGURED\)\s*\(ACTIVATED\)\s*\(ACTIVE\)', x), rss)
                if(len(ac) > 0):
                    time.sleep(1)
                    rss = self.ssh.execute_command('ssh %s /usr/bin/nokia/ManageSS.pl --list %s %s-DB' % (ds_address,
                                                                                                      rpms_info[0]['SC'],
                                                                                                      rpms_info[0]['SS'])).splitlines()
                    ac = filter(lambda x:re.match('[\w\-\d\.]*\s*\(CONFIGURED\)\s*\(ACTIVATED\)\s*\(ACTIVE\)', x), rss)
                    if(len(ac) > 0):
                        result = True
            else:
                raise AssertionError("Illegal rpms") 
        return result
    
    def store_koala_output_model_file(self,ssname='nokktt',scname='umaktt',alias='onepm_cs1_root'):
        model_file_path = ''
        exist_flag = 'not exist'
        ss = []
        temp_ss = []
        match_item = ''
        match_flag = None
        version_str = ''
        model_file_list = ''
        
        self.ssh.switch_connection(alias)
        exist_flag = self.ssh.execute_command('echo `if [ -d %s ]; then echo "exist"; else echo "not exist"; fi`'%KoalaRTE.model_file_store_dir)
        if exist_flag == 'not exist':
            self.ssh.execute_command('mkdir -p %s' %KoalaRTE.model_file_store_dir)
        
        rss = self.ssh.execute_command('/usr/bin/nokia/ManageSS.pl --list %s %s'%(scname,ssname))
        temp_ss = rss.split('\n')
        for item in temp_ss:
            match_flag = re.search('ACTIVE',item)
            if match_flag is None:
                continue
            else:
                match_item = item
        
        if match_flag is not None:
            ss = match_item.split()
            version_str = ss.pop(0)
            model_file_path = '/opt/nokia/oss/%s/conf/addon/%s.model'%(version_str.lower(),ssname.lower())
            self.ssh.execute_command('cp %s %s'%(model_file_path,KoalaRTE.model_file_store_dir))
            print "*INFO* %s have been copied to %s"%(model_file_path,KoalaRTE.model_file_store_dir)
            return True
        else:
            raise AssertionError("*ERROR* SS not active")
                
    
    def get_koala_output_model_file(self):
        model_file_list = self.ssh.execute_command('find %s | grep .*\\\.model'%KoalaRTE.model_file_store_dir)
        return model_file_list
           
    def clear_temp_koala_output_model_file(self,alias='onepm_cs1_root'):
        self.ssh.switch_connection(alias)
        self.ssh.execute_command('rm -rf %s'%KoalaRTE.model_file_store_dir)
        print "*INFO* Clear the tmp dir which used to store koala output model file"
        
        
    def _uninstall_test_pm_package_as_gc(self,SS, SC):
        global cs_info
        global ds_info
        ds_adm_path = '/var/adm/subsystems/SS-%s-%s-DB'%(SC.upper(),SS.upper())
        cs_adm_path = '/var/adm/subsystems/SS-%s-%s'%(SC.upper(),SS.upper())
        
        ds1_node=self.ssh.execute_command("ldapacmx.pl -pkgPrimaryNode db")
        cluster_type=self.ssh.execute_command('/usr/bin/nokia/IFWGetData.pl --ClusterType')
        if(cluster_type!='global'):
            rs=self.ssh.execute_command('echo /opt/nokia/oss/itools/bin/change_cluster_type.sh global|ssh %s'%ds1_node)
            print '*INFO* %s'%rs
            if(self.ssh.execute_command('/usr/bin/nokia/IFWGetData.pl --ClusterType')!='global'):
                raise AssertionError("can't switch cluster to global")
        cs_nodes=self.ssh.execute_command('/usr/bin/nokia/IFWGetData.pl --PhysicalHostForRole BACKEND').splitlines()
        cs_version_list=self.ssh.execute_command('rpm -qa | grep -i %s' %SS).splitlines()
        ds_nodes=self.ssh.execute_command('/usr/bin/nokia/IFWGetData.pl --PhysicalHostForRole DSS').splitlines()
        for ds_node in ds_nodes:
            self._modify_uninstall_value(ds_adm_path, ds_node)
            rs=self.ssh.execute_command('echo /usr/bin/nokia/installmx -task DEACTIVATE  -pkg %s|ssh %s'%(ds_info,ds_node))
            print '*INFO* %s'%rs
            rs=self.ssh.execute_command('echo /usr/bin/nokia/installmx -task UNCONFIGURE  -pkg %s|ssh %s'%(ds_info,ds_node))
            print '*INFO* %s'%rs
            ds_version_list=[]
            rs=self.ssh.execute_command("echo 'rpm -qa | grep -i %s' | ssh %s" %(SS,ds_node)).splitlines()
            for line in rs:
                if re.search('Nokia-(\w+)-(\w+).*',line):
                    ds_version_list.append(line)            
            for version in ds_version_list:
                rs=self.ssh.execute_command('echo /opt/nokia/oss/itools/bin/removerpm.pl -r %s|ssh %s'%(version,ds_node))
                print '*INFO* %s'%rs
        for cs_node in cs_nodes:
            self._modify_uninstall_value(cs_adm_path, cs_node)
            rs=self.ssh.execute_command('echo /usr/bin/nokia/installmx -task DEACTIVATE -pkg %s|ssh %s'%(cs_info,cs_node))
            print '*INFO* %s'%rs
            rs=self.ssh.execute_command('echo /usr/bin/nokia/installmx -task UNCONFIGURE -pkg %s|ssh %s'%(cs_info,cs_node))
            print '*INFO* %s'%rs
            for version in cs_version_list:
                rs=self.ssh.execute_command('echo /opt/nokia/oss/itools/bin/removerpm.pl -r %s|ssh %s'%(version,cs_node))
                print '*INFO* %s'%rs
        if(cluster_type!='global'):
            rs=self.ssh.execute_command('echo /opt/nokia/oss/itools/bin/change_cluster_type.sh %s|ssh %s'%(cluster_type,ds1_node))
            print '*INFO* %s'%rs
            if(self.ssh.execute_command('/usr/bin/nokia/IFWGetData.pl --ClusterType')!=cluster_type):
                raise AssertionError("can't switch cluster to %s"%cluster_type)       
            
            
    def _modify_uninstall_value(self, adm_file, node):
        rs = ""
        new_str = ""
        rs=self.ssh.execute_command('echo tail -1 %s | ssh %s'%(adm_file, node))
        if rs.strip() == "":
            print '*INFO* %s not exist!'%adm_file
        else:
            if re.search(ur"YES.*::0$", rs):
                print "*INFO* modify %s for uninstall!"%adm_file
                p = re.compile(r'(YES.*)(::0)$')
                new_str  = p.sub(r'\1::1', rs)
                print new_str
                self.ssh.execute_command('echo sed -i \'s/%s/%s/g\' %s | ssh %s'%(rs, new_str, adm_file, node))
            else:
                print "*INFO* No need to modify %s"%adm_file
        
    def uninstall_test_pm_package(self, ds_address, SC, SS, alias='onepm_cs1_root',cluster_type='rc'):
        result = False
        self.ssh.switch_connection(alias)
        time.sleep(1)
        if cluster_type == 'rc':
            rs = self.ssh.execute_command('/opt/nokia/oss/itools/bin/adap_install.sh %s -u 2>1' % SS)
            print "*INFO* %s" % rs
            time.sleep(1)
        elif cluster_type == 'gc':
            self._uninstall_test_pm_package_as_gc(SS, SC)
        else:
            raise AssertionError("Illegal cluster_type:%s"%cluster_type) 
        rss = self.ssh.execute_command('/usr/bin/nokia/ManageSS.pl --list %s %s' % (SC, SS)).splitlines()
        if(len(rss) == 0):
            time.sleep(1)
            rss = self.ssh.execute_command('ssh %s /usr/bin/nokia/ManageSS.pl --list %s %s-DB' % (ds_address, SC, SS)).splitlines()
            if(len(rss) == 0):
                result = True
        return result
    def close_ssh_sessions(self):
        self.ssh.close_all_connections()
    
