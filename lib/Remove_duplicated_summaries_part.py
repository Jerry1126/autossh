# -*- coding: cp936 -*-
'''
Created on Sep 4, 2014

@author: l2sun
'''
from SSHLibrary import SSHLibrary
import time,os,re
from os import listdir
class RemoveDuplicateSummaries:
        _ssh = None
        ss_registry = set()
        @property
        def ssh(self):
                return RemoveDuplicateSummaries._ssh
        def set_ssh(self, value):
                RemoveDuplicateSummaries._ssh = value
                print("*DEBUG* ssh set")
        def retrieve_rpm_version(self,rpm):
            print type(rpm)
            m=re.search(r'(-(.+)-)',rpm[0])
            print m.group()
            if m is not None:
                x=m.group()
                f=x.split('-')
                ret=[i for i in f if i is not '']
            scname=ret[0]
            ssname=ret[1]
            fixed_number=ret[2]
            rpm_version=ret[3]
            return [scname,ssname,fixed_number,rpm_version]
        def get_summaries_in_ssmeta_file(self,version=['UMACUS', 'CUSKTT', '5.0', '1.0.0']):
            sc=version[0].lower()
            ss=version[1].lower()
            fixed_number=version[2]
            rpm_version=version[3]
            rs=self.ssh.execute_command('grep  -i \'^SUMMARIES\' /opt/nokia/oss/%s-%s-%s-%s/conf/%smeta_mx.cf' %(sc,fixed_number,ss,rpm_version,ss))
            return rs
        
        def check_summaries_unique_or_not(self,summaries):
            print type(summaries)
            print summaries
            myList=[]            
            summaries_index=summaries.split('\n')
            for e in summaries_index:
                if e not in myList:
                    myList.append(e)
            if summaries_index==myList:
                print "it's true"
                flag=True;
            else:
                flag=False;
                print "it's false"
            return flag;
            

        




