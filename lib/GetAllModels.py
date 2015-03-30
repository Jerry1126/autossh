# -*- encoding: utf8 -*-
import SSHLibrary

class GetAllModels:

	def GetList(self,connection):
		ModelString = connection.execute_command("ls /opt/nokia/oss/uma*-5.0-*-*/conf/addon/*.model")
		Models = ModelString.splitlines()	
		return Models


