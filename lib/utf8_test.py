import os
import sys
import codecs
import re
import random
import string
import shutil
import tempfile
import xml.etree.ElementTree as etree


rand = random.Random()
temp_path = tempfile.gettempdir()


class SpecialUtf8:
    local_file_dir = '%s%sSpecialUtf8_%s%s'%(temp_path,os.path.sep,rand.randint(0, 2 ** 30), os.path.sep)
    local_kola_input_dir = '%s%skoalaInput_%s'%(temp_path,os.path.sep,rand.randint(0, 2 ** 30))
    
    _ssh = None
    @property
    def ssh(self):
        return SpecialUtf8._ssh
    
    def set_ssh(self, value):
        SpecialUtf8._ssh = value
        print("*DEBUG* ssh set")
    
    def _get_unicode(self):
        unicode_list = [u"\u5F66",u"\uFF61",u"\u2EC0",u"\u3004",u"\u31CC",u"\u2FD4",
                        u"\u2FF7",u"\u311E",u"\u31B1",u"\u3077",u"\u30DB",u"\u31FB",
                        u"\uAC83",u"\u11E6",u"\u3180",u"\u1D315",u"\u4DF8",u"\uA0B2",
                        u"\uA4B4",u"\u2896",u"\u3244",u"\u3360",u"\u273A",u"\u26F7",u"\uFE17",u"\uFE46"]
        '''unicode_list = [u"\u0000",u"\u0020",u"\u0080",u"\u00A0",u"\u0100",u"\u0180",
                        u"\u0250",u"\u02B0",u"\u0300",u"\u0370",u"\u0400",u"\u0500",
                        u"\u0530",u"\u0590",u"\u0600",u"\u0700",u"\u0750",u"\u0780",
                        u"\u07C0",u"\u0800",u"\u0840",u"\u0860",u"\u0900",u"\u0980",
                        u"\u0A00",u"\u0A80",u"\u0B00",u"\u0B80",u"\u0C00",u"\u0C80",
                        u"\u0D00",u"\u0D80",u"\u0E00",u"\u0E80",u"\u0F00",u"\u1000",
                        u"\u10A0",u"\u1100",u"\u1200",u"\u1380",u"\u13A0",u"\u1400",
                        u"\u1680",u"\u16A0",u"\u1700",u"\u1720",u"\u1740",u"\u1760",
                        u"\u1780",u"\u1800",u"\u18B0",u"\u1900",u"\u1950",u"\u1980",
                        u"\u19E0",u"\u1A00",u"\u1A20",u"\u1AB0",u"\u1B00",u"\u1B80",
                        u"\u1BC0",u"\u1C00",u"\u1C50",u"\u1C80",u"\u1CC0",u"\u1CD0",
                        u"\u1D00",u"\u1D80",u"\u1DC0",u"\u1E00",u"\u1F00",u"\u2000",
                        u"\u2070",u"\u20A0",u"\u20D0",u"\u2100",u"\u2150",u"\u2190",
                        u"\u2200",u"\u2300",u"\u2400",u"\u2440",u"\u2460",u"\u2500",
                        u"\u2580",u"\u25A0",u"\u2600",u"\u2700",u"\u27C0",u"\u27F0",
                        u"\u2800",u"\u2900",u"\u2980",u"\u2A00",u"\u2B00",u"\u2C00",
                        u"\u2C60",u"\u2C80",u"\u2D00",u"\u2D30",u"\u2D80",u"\u2DE0",
                        u"\u2E00",u"\uA000",u"\uA490",u"\uA4D0",u"\uA500",u"\uA640",
                        u"\uA6A0",u"\uA700",u"\uA720",u"\uA800",u"\uA830",u"\uA840",
                        u"\uA880",u"\uA8E0",u"\uA900",u"\uA930",u"\uA960",u"\uA980",
                        u"\uA9E0",u"\uAA00",u"\uAA60",u"\uAA80",u"\uAAE0",u"\uAB00",
                        u"\uAB30",u"\uABC0",u"\uAC00",u"\uD7B0",u"\uD800",u"\uDC00",
                        u"\uE000",u"\uF900",u"\uFB00",u"\uFB50",u"\uFE00",u"\uFE10",
                        u"\uFE20",u"\uFE30",u"\uFE50",u"\uFE70",u"\uFF00",u"\uFFF0",
                        u"\u10000",u"\u10080",u"\u10100",u"\u10140",u"\u10190",u"\u101D0",
                        u"\u10280",u"\u102A0",u"\u102E0",u"\u10300",u"\u10330",u"\u10350",
                        u"\u10380",u"\u103A0",u"\u10400",u"\u10450",u"\u10480",u"\u10500",
                        u"\u10530",u"\u10600",u"\u10800",u"\u10840",u"\u10860",u"\u10880",
                        u"\u10900",u"\u10920",u"\u10980",u"\u109A0",u"\u10A00",u"\u10A60",
                        u"\u10A80",u"\u10AC0",u"\u10B00",u"\u10B40",u"\u10B60",u"\u10B80",
                        u"\u10C00",u"\u10E60",u"\u11000",u"\u11080",u"\u110D0",u"\u11100",
                        u"\u11150",u"\u11180",u"\u111E0",u"\u11200",u"\u112B0",u"\u11300",
                        u"\u11480",u"\u11580",u"\u11600",u"\u11680",u"\u118A0",u"\u11AC0",
                        u"\u12000",u"\u12400",u"\u13000",u"\u16800",u"\u16A40",u"\u16AD0",
                        u"\u16B00",u"\u16F00",u"\u1B000",u"\u1BC00",u"\u1BCA0",u"\u1D000",
                        u"\u1D100",u"\u1D200",u"\u1D300",u"\u1D360",u"\u1D400",u"\u1E800",
                        u"\u1EE00",u"\u1F000",u"\u1F030",u"\u1F0A0",u"\u1F100",u"\u1F200",
                        u"\u1F300",u"\u1F600",u"\u1F650",u"\u1F680",u"\u1F700",u"\u1F780",u"\u1F800"]'''
        
        unicode_str = random.choice(unicode_list)
        print "*INFO* unicode is %s"%repr(unicode_str)
        return unicode_str
    
    def modify_koala_input_file(self, file_name, attribute_name):
        local_file_input = ""
        local_file_output = ""
        regex_start = ur".*<\bCounter\b"
        regex_end = ur".*</\bCounter\b"
        return_list = []
        counter = 0
        flag = False
        
        local_file_input = self._fetch_file_from_remote(file_name)
        local_file_output = "%s%s%s"%(SpecialUtf8.local_kola_input_dir,os.path.sep,os.path.basename(file_name))
        
        fh_in = codecs.open(r"%s"%local_file_input, "r", "utf-8")
        fh_out = codecs.open(r"%s"%local_file_output, "a", "utf-8")        
        
        in_str = fh_in.read()
        in_str = in_str.split('\n')
        
        unicode_str = self._get_unicode()
        
        if attribute_name == "OMeSName":
            regex = ur".*\bOMeSName\b\s*=\".*\""
            
        elif attribute_name == "RBName":
            regex = ur".*\RBName\b\s*=\".*\""
            
        elif attribute_name == "Description":
            regex = ur".*<Description>.*"
        elif attribute_name == "ID":
            regex = ur".*\bID\b\s*=\".*\""
        else:
            raise AssertionError("*ERROR* Invalid attribute name. Must be [ID/OMeSName/RBName/Description]")
            
        for i in in_str:
            if re.search(regex_start, i) or flag is True:
                flag = True
                if attribute_name == "OMeSName":
                    if re.search(regex, i):
                        p = re.compile(r'(.*\bOMeSName\b\s*=)\"(.*?)\"(.*)')
                        i = p.sub(r'\1"\2%sMEA%d"\3'%(unicode_str, counter), i)
                        counter +=1
                elif attribute_name == "RBName":
                    if re.search(regex, i):
                        p = re.compile(r'(.*\bRBName\b\s*=)\"(.*?)\"(.*)')
                        i = p.sub(r'\1"\2%sMEA%d"\3'%(unicode_str, counter), i)
                        counter +=1
                elif attribute_name == "ID":
                    if re.search(regex, i):
                        p = re.compile(r'(.*\bID\b\s*=\")(.*?)(\".*)')
                        i = p.sub(r'\1\2%sMEA%d\3'%(unicode_str, counter), i)
                        counter +=1                        
                elif attribute_name == "Description":
                    if re.search(ur".*<Description>.*</Description>.*", i):
                        p = re.compile(r'(.*<Description>)(.*)(</Description>.*)')
                        i = p.sub(r'\1\2%sMEA%d\3'%(unicode_str, counter), i)
                        counter +=1
                    elif re.search(ur".*<Description>.*", i) and not re.search(ur".*</Description>.*", i):
                        i = "%s%sMEA%d"%(i, unicode_str, counter)  
                        counter +=1
                        
            if re.search(regex_end, i):
                flag = False
                
            fh_out.write(i)
            fh_out.write("\n")             
        fh_in.close()
        fh_out.close()
        
        local_file_input = self._upload_file_to_remote(local_file_output, file_name)
        
        unicode_str = repr(unicode_str)
        return_list.append(unicode_str[2:-1])
        return_list.append(counter)
        
        print "*INFO* %d places of [%s] have been modified with unicode - [%s]"%(counter, attribute_name, unicode_str[1:])
        return return_list
        
        
    def koala_ouput_with_special_char_check(self, attribute_name, unicode, counter, ssname):
        base_path = "/var/tmp/rtekoa/integrationTool/"
        file_path = ""
        file_count = 0
        file_count_return = 0
        counter_return = 0
        flag = True
        
        if attribute_name == "OMeSName" or attribute_name == "RBName":
            file_path = "%s%s/conf/%s.model"%(base_path, ssname.lower(), ssname.lower())
            file_count = 1
        elif attribute_name == "Description":
            file_path = "%s%s/doc/*"%(base_path, ssname.lower())
            file_count = 4
            
        print "*INFO* Download the files to local directory"
        self.ssh.get_file(file_path,SpecialUtf8.local_file_dir)
        
        file_count_return = self._list_dir()
        if file_count_return != file_count:
            raise AssertionError("*ERROR* File missing, must include %d files"%file_count)
        else:
            print "*INFO* %d files have downloaded to local directory successful!"%file_count_return
            
        file_list = os.listdir(SpecialUtf8.local_file_dir)
        for file in file_list:
            file_name = "%s%s"%(SpecialUtf8.local_file_dir, file)
            counter_return = self._encode_special_char(file_name, unicode)
            if attribute_name == "Description":
                if counter_return == 0:
                    flag = False
                    print "*ERROR* %s include %d special chars [%s], must be more than 1 char"%(file, counter_return, unicode)
                else:
                    print "*INFO* %s include %d special chars [%s]"%(file, counter_return, unicode)
            else:
                if counter_return == counter:
                    print "*INFO* %s include %d special chars [%s]"%(file, counter_return, unicode)
                else:
                    flag = False
                    print "*ERROR* %s include %d special chars [%s], actually must be %d chars"%(file, counter_return, unicode, counter)
            
        return flag
    
    def _list_dir(self):
        file_num = 0
        list = os.listdir(SpecialUtf8.local_file_dir)
        print "*INFO* The files as below:\n"
        for file in list:
            file_num +=1
            print "\t%s"%file
            
        return file_num
    
    def _fetch_file_from_remote(self,fn_remote):
        local_file = "%s/in_%s"%(SpecialUtf8.local_kola_input_dir,os.path.basename(fn_remote))
        self.ssh.get_file(fn_remote,local_file)
        return local_file
    
    def _upload_file_to_remote(self,fn_local, fn_remote):
        self.ssh.put_file(fn_local, fn_remote)

        
    def _encode_special_char(self, file_name, unicode):
        counter = 0
        fh_encode = codecs.open(r"%s"%file_name, "r", "utf-8")
        encode_block = fh_encode.read()
        encode_block = encode_block.split('\n')

        for i in encode_block:
            print repr(i)
            if re.search(unicode, repr(i)):
                counter +=1
        print counter
        return counter
        
    def clear_local_tmp_env(self):
        if os.path.exists(SpecialUtf8.local_file_dir):
            shutil.rmtree(SpecialUtf8.local_file_dir)
            
        if os.path.exists(SpecialUtf8.local_kola_input_dir):
            shutil.rmtree(SpecialUtf8.local_kola_input_dir)
            
    
    def close_ssh_sessions(self):
        print "***INFO*** Execute to close all the ssh connection session\n"
        self.ssh.close_all_connections()
    
#su = SpecialUtf8()
##su.modify_koala_input_file(r"D:\NOKKDD\nokkddKoala.xml", "OMeSName")
#su._encode_special_char(r"D:\nokkddKoala.xml", '\u311e')
#    
