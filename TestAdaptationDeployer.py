import getopt,sys
from SSHLibrary import SSHLibrary
from Koala import KoalaRTE
stdout=sys.stdout
sys.stdout=sys.stderr
def print_usage():
    print """
This is a tool for run koalaRTE on lab and install the generated PM adaptation.
Li Jun @2014-8-8
Usage: python TestAdaptationDeployer [--sc] [--ss] [--koala_input_path] --onepm_cs_address --onepm_ds_address [--root_pass] [--omc_pass] [--root_prompt] [--omc_promt] [--reserve_environment_after_exit] operation
    --sc default UMAKTT
    --ss default NOKKTT
    --koala_input_path the path which store the koala input and general config from TA root path
    --onepm_cs_address dns or ip address of onepm cs node
    --onepm_ds_address dns or ip address of onepm ds node
    --root_pass the password for root user of onepm cs node
    --omc_pass the password for omc user of onepm cs node
    --root_prompt default #
    --omc_promt default $
    --reserve_environment_after_exit if the program clear the generated files by koalaRTE before exits
    operation, could be,
        upload, upload koala input and general config to lab
        build, upload koala input and general config to lab and then run koala and gen rpms
        install, upload koala input and general config to lab and then run koala and gen rpms and then install the rpms
        uninstall, uninstall the ss from lab
"""


if __name__ == '__main__':
    dic = getopt.getopt(sys.argv[1:],
                        '',
                        ['sc=',
                         'ss=',
                         'koala_input_path=',
                         'onepm_cs_address=',
                         'onepm_ds_address=',
                         'root_pass=',
                         'omc_pass=',
                         'root_prompt=',
                         'omc_promt=',
                         'reserve_environment_after_exit'])
    options=reduce(lambda op,p:dict(op,**{p[0]:op.get(p[0],[])+[p[1]]}),dic[0],{})
    print options
    args=dic[1]
    sc=options.get('--sc',['UMAKTT'])[0]
    ss=options.get('--ss',['NOKKTT'])[0]
    koala_input_path=options.get('--koala_input_path',['metadata'])[0]
    onepm_cs_address=options.get('--onepm_cs_address',[None])[0]
    onepm_ds_address=options.get('--onepm_ds_address',[None])[0]
    root_pass=options.get('--root_pass',['arthur'])[0]
    omc_pass=options.get('--omc_pass',['omc'])[0]
    root_prompt=options.get('--root_prompt',['#'])[0]
    omc_prompt=options.get('--omc_prompt',['$'])[0]
    if(len(filter(lambda x:x is not None,[sc,ss,koala_input_path,onepm_cs_address,onepm_ds_address,root_pass,omc_pass]))==0 or len(args)!=1):
        print_usage()
    else:
        operation=args[0]
        ssh=SSHLibrary()
        ssh.open_connection(onepm_cs_address,'onepm_cs1_root',prompt='#')
        ssh.login('root',root_pass)
        ssh.open_connection(onepm_cs_address,'onepm_cs1_omc',prompt='$')
        ssh.login('omc',omc_pass)
        rte=KoalaRTE()
        rte.set_ssh(ssh)
        if(operation in ['upload','build','install']):
            rte.upload_koala_input_and_general_config_to_cs(ss,
                                                            alias='onepm_cs1_root',
                                                            koala_input_path=koala_input_path)
            if(operation in ['build','install']):
                rpms=rte.build_test_pm_package(ss,
                                               alias='onepm_cs1_omc')
                if(operation=='install'):
                    rs=rte.install_test_pm_package(rpms,onepm_ds_address,alias='onepm_cs1_root')
                    if(rs):
                        sys.stdout=stdout
                        print "\n".join(map(lambda x:x.split('/')[-1],filter(lambda x: 'DB' not in x,rpms)))
                        sys.stdout=sys.stderr
                    else:
                        exit(1)
            if(not options.has_key('--reserve_environment_after_exit')):
                rte.clear_ss_environment(alias='onepm_cs1_root')
        elif(operation=='uninstall'):
            rte.uninstall_test_pm_package(onepm_ds_address,sc,ss,alias='onepm_cs1_root')
        rte.close_ssh_sessions()
    exit(0)
        
