import sys
import os
import re
import SSHLibrary

class GetLevelFlag:
    def connection(self, ip="10.9.137.108", user="oneac", passwd="caeno"):
        con = SSHLibrary.SSHLibrary()
        con.open_connection(ip)
        con.login(user, passwd)
        return con
    def get_flag(self, build_dir):
        print "*INFO* build folder on mpp is: %s\n"%build_dir
        con = self.connection()
        file_path = os.path.join(build_dir,"level_flag.txt")
        command = "tail -1 %s | awk '{print $1}'"%file_path
        result = con.execute_command(command)
        con.close_connection()
        return result
        
