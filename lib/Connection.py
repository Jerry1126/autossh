import SSHLibrary

class Connection:

	def connect(self, lab_ip, user, passwd):
		con = SSHLibrary.SSHLibrary()
		con.open_connection(lab_ip)
		con.login(user, passwd)
		return con
	def scp(self,connection,source,destination):
		connection.put_file(source,destination)
	def close(self,connection):
		connection.close_connection()
	def execute(self,connection,command):
		result = connection.execute_command(command)
		return result
