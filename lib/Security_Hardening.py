import os,sys
import xml.etree.ElementTree as et
import tempfile
import shutil

class Security_Hardening:

    def get_lower(self,string):
        string = string.lower()
        return string
    
    def check_lock_schema_owner(self,file_path):
        file=open(file_path)
        for line in file.readlines():
            if "LOCK_SCHEMA_OWNER" in line:
                print line
                result=line.split("\"")[1]
                print "result:"+result
                if result == "YES":
                    result="1"
                elif result == "NO":
                    result="0"
        return result

    def make_dir(self,ss_name):
        update_dir=tempfile.mkdtemp()
        update_path = update_dir+os.path.sep+ss_name+".cfg"
        print update_path
        return update_path

    def remove_dir(self,xml_path):
        os.remove(xml_path)

#SH=Security_Hardening()
#SH.check_lock_schema_owner("D:\\")
