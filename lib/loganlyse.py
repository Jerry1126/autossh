# -*- encoding: utf8 -*-
import SSHLibrary

class loganlyse:

    def CountErrors(self,connection):
        f = connection.execute_command("grep \"Errors found\" /tmp/koalog | awk -F \" \" \'{print $1}\'")
	errors = f.splitlines()
	connection.execute_command("cp /tmp/koalog /tmp/koalog.bk")
	return errors
