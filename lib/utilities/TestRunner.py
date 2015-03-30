'''
Created on Sep 2, 2014

@author: j19li
'''
import os
class TestRunner:
    def run_test(self,name,testcase_path,include_tags=[],exlude_tags=[],extra_variables={}):
        result=True
        python_runable=os.environ.get('TEX_PYTHON',"python")
        python_path=os.environ.get('PYTHONPATH',"")
        tex_robot=os.environ.get('TEX_ROBOT',r'C:\Python27\Lib\site-packages\robotframework-2.7-py2.7-win-amd64.egg\robot\run.py')
        tex_reports_tmp_dir=os.environ.get('TEX_REPORTS_TMP_DIR','./')
        sdv_python_file=os.environ.get('SDV_PYTHON_FILE','sdv.py')
        hostname=os.environ.get('HOSTNAME','localhost')
        ldapbasedn=os.environ.get('BASEDN','')
        sc_home=os.environ.get('SC_HOME','./')
        sc_java_lib=os.environ.get('SC_JAVA_LIB','./lib')
        sc_python_lib=os.environ.get('SC_PYTHON_LIB','./lib')
        tex_selenium_port=os.environ.get('TEX_SELENIUM_PORT','')
        sc=os.environ.get('SC','')
        xml=os.environ.get('XML','output.xml').replace('output.xml',
                                                       '%s_output.xml'%name)
        log=os.environ.get('LOG','log.html').replace('log.html',
                                                    '%s_log.html'%name)
        report=os.environ.get('REPORT','report.html').replace('report.html',
                                                             '%s_report.html'%name)
        cmd='''%s\\
    %s \\
    --pythonpath %s \\
    --noncritical not_ready \\
    --variable hostname:%s \\
    --variable ldapbasedn:%s \\
    --variable SC_HOME:%s \\
    --variable SC_JAVA_LIB:%s \\
    --variable SC_PYTHON_LIB:%s \\
    --variable TEX_SELENIUM_PORT=%s \\
    --variable moduleId:%s \\
    --variable PROGRAM_NAME:nac \\
    --variable itk_Program_RPM_Name:NSN-itk \\
    --variablefile %s \\
    --outputdir "%s" \\
    --output "%s" \\
    --log "%s" \\
    --report "%s" \\
    --name "%s" \\
    %s\\
    %s\\
    %s\\
    "%s"'''%(python_runable,
             tex_robot,
             python_path,
             hostname,
             ldapbasedn,
             sc_home,
             sc_java_lib,
             sc_python_lib,
             tex_selenium_port,
             sc,
             sdv_python_file,
             tex_reports_tmp_dir,
             xml,
             log,
             report,
             name,
             " \\\n".join(map(lambda x:'--include %s'%x,include_tags)),
             " \\\n".join(map(lambda x:'--exclude %s'%x,exlude_tags)),
             " \\\n".join(map(lambda x:'--variable %s:%s'%(x,
                                                           extra_variables[x]),
                              extra_variables.keys())),
             testcase_path)
        print "*INFO* %s"%cmd
        rs=os.system(cmd)
        if(rs!=0):
            print("*INFO* Test cases: '%s' failed"%sc)
            result=False
        return result