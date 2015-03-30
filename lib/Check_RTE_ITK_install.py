# -*- encoding: utf8 -*-
import SSHLibrary
import random

class Check_RTE_ITK_install(object):
    def __init__(self, lab_ip, username, passwd):
        self.lab_ip = lab_ip
        self.username = username
        self.passwd = passwd
        
    def connect_lab(self, lab_ip, user, passwd):
        con = SSHLibrary.SSHLibrary()
        con.open_connection(lab_ip)
        con.login(user, passwd)
        return con
        
    def check_RTE_install(self, con):        
        con.execute_command("/usr/bin/nokia/ManageSS.pl --list umakoa rtekoa > tmp")
        re = con.execute_command("grep '(CONFIGURED) (ACTIVATED) (ACTIVE)' tmp")
        if re:
            print "Lab install KOARTE successfully!"
            ret = True
        else:
            print "Lab don't install KOARTE successfully!"
            ret = False
           
        return str(ret)
        
    def check_ITK_install(self, con):
        re=con.execute_command("cd /opt/nokia/oss/reporter-5.0*;echo $?")
        print "re=%s" % re
        if re == "0":
            print "Lab install ITK successfully!"
            ret = True
        else:
            print "Lab don't install ITK successfully!"
            ret = False
        return str(ret)
    
    def Close_Connection(self, con):
        con.close_connection() 
        
    
                               
