# -*- coding: cp936 -*-
'''
Created on Aug 11, 2014

@author: l2sun
'''
import re
import itertools
from SSHLibrary import SSHLibrary
#coding=utf-8
from xml.dom import minidom
class MeasurementStorageTimeChecker:
        _ssh = None
        @property
        def ssh(self):
                return MeasurementStorageTimeChecker._ssh
        def set_ssh(self, value):
                MeasurementStorageTimeChecker._ssh = value
                print("*DEBUG* ssh set")
        def mon_check(self,storage_time_string_input,storage_time_string_output):
                """Helper keyword that returns the checking result of storage time. If the busyhour is setted in metadata,don't check the detailed value in 
                output when the value is not *.
        @var :  The storage time list which should be, and the finnal storage time after build koala
        @return: True or False
        """
                result=True
                storage_time_string_output_dict=dict(storage_time_string_output)
                if len(storage_time_string_input)!=len(storage_time_string_output):
                    print "lenght of input is %s" %len(storage_time_string_input)
                    result=False
                    print "*INFO* the measurement count is wrong after converted"                
                else:
                    for k in storage_time_string_input:
                        print "keys in input are %s" %k
                        for m in storage_time_string_output:
                            print "keys in output %s" %m
                            if re.match(r'\w+\.'+(str(k).lower().split('.')[0])+'\.'+(str(k).lower().split('.')[1]),m):
                                print "k is %s, value is %s" %(k,storage_time_string_input[k])
                                print "m is %s, value is %s-----" %(m,storage_time_string_output[m])
                                if storage_time_string_input[k]==storage_time_string_output[m]:
                                    next
                                else:
                                    a=storage_time_string_input[k]
                                    b=storage_time_string_output[m]
                                    if dict(set(a.iteritems())-set(b.iteritems())).has_key('BH') or dict(set(a.iteritems())-set(b.iteritems())).has_key('WeekBH') or dict(set(a.iteritems())-set(b.iteritems())).has_key('MonBH'):
                                        next
                                    else:
                                        result=False
                                        print "*INFO* Exists LIFECYCLE item having storage time not followed the correct rule; The correct result should be :the object level is %s and value is %s,but it is : the object level is %s and value is %s" %(k,a,m,b)                                        
                return result
        def get_mx_cf_file_after_installation(self,sc,ss):
            '''Fabricate the output file($ss[0:3]sys__mx.cf) path'''
            filepath=""
            filepath="/etc/opt/nokia/oss/"+sc+"/conf/"
            output_file_name=ss[0:3]
            suffix= "sys__mx.cf"
            filepath+=output_file_name+suffix
            return filepath
            
        def get_mx_cf_file_without_installation(self,ss):
            '''Fabricate the output file($ssrapsysrcmx.cf.cf) path'''
            filepath=""
            filepath="/var/tmp/rtekoa/integrationTool/"+ss+"/"+ss+"rap/"
            output_file_name=ss+"rapsysrcmx.cf"
            filepath+=output_file_name
            return filepath
        
        def mon_and_monbh(self,storage_file,storage_time_string_input,alias='onepm_cs1_root'):
            self.ssh.switch_connection(alias)
            output_dict=dict()
            grep_command="ls |grep '^LIFECYCLE\\.\\w*\\.\\w*'"
            sed_and_awk="|sed 's/LIFECYCLE\\.\\(\\w*\\)\\.\\(\\w*\\)/LIFECYCLE.\\1 .\\2/'|awk 'BEGIN {printf(\"{\")} {printf(\"'\"'%s%s'\"':{'\"'Hour'\"':'\"'%s'\"','\"'Day'\"':'\"'%s'\"','\"'BH'\"':'\"'%s'\"','\"'Week'\"':'\"'%s'\"','\"'WeekBh'\"':'\"'%s'\"','\"'Mon'\"':'\"'%s'\"','\"'MonBH'\"':'\"'%s'\"'},\\n\",$1,$2,$5,$6,$7,$8,$9,$10,$11)} END {print \"}\"}'"
            cmd = '%s %s%s' %(grep_command,storage_file,sed_and_awk)
            rs = self.ssh.execute_command(cmd)
            output_dict=eval(rs)
            print " Enter the function mon_check"
            print "output content is %s,type is %s" %(rs,type(output_dict))
            print "input content is %s" %storage_time_string_input
            rc = self.mon_check(storage_time_string_input,output_dict)
            print "rc is ",rc
            return rc
        def extract_time_levels_and_busy_hour(self,meas_ele):
             '''extract time levels and busy hour for every measurement
              Parameter:The list of measurement node
             Return Value: The time levels' value,busyhourValue and TopologyRef value'''
             ts=meas_ele.getElementsByTagName('Time')
             t=ts[0] if len(ts)>0 else None
             rls=t.getElementsByTagName('RawLevel') if t is not None else []
             rl='\n'.join(map(lambda x:x.nodeValue,rls[0].childNodes)) if len(rls)>0 else ''
             fls=t.getElementsByTagName('FirstLevel') if t is not None else []
             fl='\n'.join(map(lambda x:x.nodeValue,fls[0].childNodes)) if len(rls)>0 else ''
             lls=t.getElementsByTagName('LastLevel') if t is not None else []
             ll='\n'.join(map(lambda x:x.nodeValue,lls[0].childNodes)) if len(rls)>0 else ''
             #print rl,fl,ll
             '''retrive the BusyHourDefinition value'''
             bs=meas_ele.getElementsByTagName('BusyHourDefinition')
             b=bs[0] if len(bs)>0 else None
             BusyHour=b.getElementsByTagName('Formula') if b is not None else []
             BusyHourValue='\n'.join(map(lambda x:x.nodeValue,BusyHour[0].childNodes)) if len(BusyHour)>0 else ''
             '''retrive the TopologyRef value'''
             tr=meas_ele.getElementsByTagName('TopologyRef')
             list_SkipAggregationChoice_ID=[]
             input_settings=[]
             #TopologyRef=[]
             for x in range(len(tr)):
                 rc=""
                 print type(input_settings)
                 input_settings.append([])         # Create a list with length of x
                 input_settings[x].append([])
                 print "check the object level"
                 trvalue=tr[x] if len(tr)>0 else None
                 RawLevelRef=trvalue.getElementsByTagName('RawLevelRef')
                 RawLevelRefValue='\n'.join(map(lambda x:x.nodeValue,RawLevelRef[0].childNodes)) if len(RawLevelRef)>0 else ''
                 List_RawLevelRefValue=str(RawLevelRefValue).split('.')
                 FirstLevelRef=trvalue.getElementsByTagName('FirstLevelRef')
                 FirstLevelRefValue='\n'.join(map(lambda x:x.nodeValue,FirstLevelRef[0].childNodes)) if len(FirstLevelRef)>0 else ''
                 List_FirstLevelRefValue=str(FirstLevelRefValue).split('.')
                 LastLevelRef=trvalue.getElementsByTagName('LastLevelRef')
                 LastLevelRefValue='\n'.join(map(lambda x:x.nodeValue,LastLevelRef[0].childNodes)) if len(LastLevelRef)>0 else ''
                 List_LastLevelRefValue=str(LastLevelRefValue).split('.')
                 #TopologyRef[x][0]={'TopologyRefID':tr[x].getAttribute("ID"),'List_RawLevelRefValue':List_RawLevelRefValue,'List_FirstLevelRefValue':List_FirstLevelRefValue,'List_LastLevelRefValue':List_LastLevelRefValue}
                 input_settings[x]={'measure ID':meas_ele.getAttribute("ID"),'TopologyRefID':tr[x].getAttribute("ID"),'RawLevel':rl,'FirstLevel':fl,'LastLevel':ll,'BusyHourValue':BusyHourValue,'List_RawLevelRefValue':List_RawLevelRefValue,'List_FirstLevelRefValue':List_FirstLevelRefValue,'List_LastLevelRefValue':List_LastLevelRefValue}
                 list_SkipAggregationChoice_ID={'measure ID':meas_ele.getAttribute("ID"),'TopologyRefID':tr[x].getAttribute("ID"),'SkipAggregation':tr[x].getAttribute("SkipAggregation")}
                 #input_settings.append(list_SkipAggregationChoice_ID)
                 input_settings[x]['measure ID']=meas_ele.getAttribute("ID")
                 input_settings[x]['SkipAggregation']=tr[x].getAttribute("SkipAggregation")

             return input_settings
        def storage_time_value_table(self,measurement):
             '''Create a storage time list
             Parameter:The list of measurement's ID,time_levels,busy_hour
             Return Value: A storage time list'''
             ms=measurement;
             storageTablelist=[]
             text = {}
             test1={}
             m=0
             '''seting storage time without TopologyRef'''
             for x in range(len(ms)):    # x is the count of measurements
                 storageTablelist.append([])         # Create a list with length of x
                 storageTablelist[x].append(ms[x][0])
                 a=len(ms)
                 for y in range(len(ms[x])):      # y is the length of every measurement(contain time level and maybe BusyHour"
                     b=len(ms[x])
                     print type(ms[x][1])
                     for z in range(len(ms[x][1])):
                         for k,v in zip(ms[x][1][z].iterkeys(),ms[x][1][z].itervalues()):
                             if k=='LastLevel':
                                 if v=='hour':
                                     text = {"Hour":"8","Day":"*","BH":"*","Week":"*","WeekBh":"*","Mon":"*","MonBH":"*"}
                                 elif v=='week':
                                     text = {"Hour":"8","Day":"15","BH":"15","Week":"15","WeekBh":"15","Mon":"*","MonBH":"*"}
                                 elif v=='month':
                                     text = {"Hour":"8","Day":"40","BH":"40","Week":"15","WeekBh":"15","Mon":"40","MonBH":"40"}
                             elif k=='BusyHourValue':
                                 text1={"BH":"*","WeekBh":"*","MonBH":"*"}
                                 text.update(text1)
                     storageTablelist[x].append(text)
             '''set storage time with TopologyRef'''
             return storageTablelist
        
        def storage_time_value_table_topologyRef(self,measurement):
             '''Create a storage time list contain topologyRef"
             Parameter:The list of measurement's ID,time_levels,busy_hour
             Return Value: A storage time list'''
             ms=measurement;
             storageTablelist=[]  #contain the measurement id and the topologyRef D-values
             text = []  # the topologyRef D-values
             list_top = [] # the topologyRef D-values other than first measurement's
             storageTimeIndex=[]  # The index of the storageTimes
             meas=[]
             element={}
             '''seting storage time without TopologyRef'''
             for x in range(len(ms)):    # x is the count of measurements
                 text.append([])         # Create a list with length of x
                 if type(text[x])==str:
                     #list_top.append([]) 
                     #print "list_top is %s" %list_top
                     list_top.append([ms[x][0]])
                     text=list_top
                 else:
                     text[x].append(ms[x][0])
                 storageTablelist.append([])         # Create a list with length of x
                 a=len(ms)
                 '''for y in range(len(ms[x])):      # y is the length of every measurement(contain time level and maybe BusyHour"
                     b=len(ms[x])
                     print type(ms[x][1])'''
                 for y in range(len(ms[x][1])):
                         for k,v in zip(ms[x][1][y].iterkeys(),ms[x][1][y].itervalues()):
                             if k=='di_first_lastLevel':
                                 print "Measurement name is %s,the value of ms[%s][1][%s]'s %s number value=%s" %(ms[x][0],x,y,k,v)
                                 diff_first_lastLevel=v
                                 for i in range(len(v)):
                                     text.append(diff_first_lastLevel[i])
                                 #for i in range(len(v)):                                    
                 print "text is %s" %text
                 storageTablelist[x]+=text
             for m in range(len(storageTablelist)): #Fabricate the storageTable list index as this formular : object.measurementID][0])
                 storageTimeIndex.append([])
                 meas= storageTablelist[m][0]
                 del storageTablelist[m][0]
                 storageTimeIndex[m]=map(lambda x:"%s.%s"%(x[1],x[0]),itertools.product(meas,storageTablelist[m]))
             print "storageTimeIndex is %s" %storageTimeIndex
             
             return storageTimeIndex
        
        def storage_time_table(self,time_list,measu_list):
            '''Convert the storage_time list and measurement_list to storage time value table
              parameter:
              ------------------------
              time_list:[[u'TRAFFICT', {'Week': '15', 'WeekBh': '15', 'Hour': '8', 'BH': '40', 'MonBH': '40', 'Mon': '40', 'Day': '40'}],
              [u'RESAVAIL', {'Week': '15', 'WeekBh': '15', 'Hour': '8', 'BH': '15', 'MonBH': '*', 'Mon': '*', 'Day': '15'}]]
              measu_list:[[u'KCF.TRAFFICT', u'KTS.TRAFFICT', u'KSC.TRAFFICT', u'SEG.TRAFFICT', u'TTP.TRAFFICT'],
              [u'KCF.RESAVAIL', u'KTS.RESAVAIL', u'KSC.RESAVAIL', u'SEG.RESAVAIL', u'TTP.RESAVAIL']]
              -------------------------
              Return value:
              -------------------------
              {u'TTP.RESAVAIL': {'Week': '15', 'WeekBh': '15', 'Hour': '8', 'BH': '15', 'MonBH': '*', 'Mon': '*', 'Day': '15'},
              u'KSC.TRAFFICT': {'Week': '15', 'WeekBh': '15', 'Hour': '8', 'BH': '40', 'MonBH': '40', 'Mon': '40', 'Day': '40'},
              u'KTS.RESAVAIL': {'Week': '15', 'WeekBh': '15', 'Hour': '8', 'BH': '15', 'MonBH': '*', 'Mon': '*', 'Day': '15'},
              u'KCF.RESAVAIL': {'Week': '15', 'WeekBh': '15', 'Hour': '8', 'BH': '15', 'MonBH': '*', 'Mon': '*', 'Day': '15'},
              u'SEG.TRAFFICT': {'Week': '15', 'WeekBh': '15', 'Hour': '8', 'BH': '40', 'MonBH': '40', 'Mon': '40', 'Day': '40'},
              u'KCF.TRAFFICT': {'Week': '15', 'WeekBh': '15', 'Hour': '8', 'BH': '40', 'MonBH': '*', 'Mon': '40', 'Day': '40'},
              u'SEG.RESAVAIL': {'Week': '15', 'WeekBh': '15', 'Hour': '8', 'BH': '15', 'MonBH': '*', 'Mon': '*', 'Day': '15'},
              u'KTS.TRAFFICT': {'Week': '15', 'WeekBh': '15', 'Hour': '8', 'BH': '40', 'MonBH': '40', 'Mon': '40', 'Day': '40'},
              u'KSC.RESAVAIL': {'Week': '15', 'WeekBh': '15', 'Hour': '8', 'BH': '15', 'MonBH': '*', 'Mon': '*', 'Day': '15'},
              u'TTP.TRAFFICT': {'Week': '15', 'WeekBh': '15', 'Hour': '8', 'BH': '40', 'MonBH': '40', 'Mon': '40', 'Day': '40'}}
              '''
            storage_time_table=dict()
            for m in range(len(measu_list)):
                print "m is %s" %map
                for n in range (0,m+1):
                    print "n is %s" %n
                    pattern=str(time_list[m][0])
                    string=str(measu_list[n][0])
                    flag=re.match(r'\w+\.'+pattern,string)
                    if flag:
                        for i in range(len(measu_list[n])):
                            storage_time_table[measu_list[n][i]]=time_list[m][1]
            return storage_time_table
        def Switch_input_to_storage_time_list(self,xml_content):
            '''Convert the input data to storage time value table
               Parameter:MetaDataFile
               Return Value: A sorage time list'''
            storage_time_table_dict=[]
            MSTCE=MeasurementStorageTimeChecker()
            #f=open(r'C:\Work\Koala TA Code\robot\src\metadata\sunlii\sunliiKoala.xml')
            #xml_content=f.read()
            d=minidom.parseString(xml_content)
            ms=d.getElementsByTagName('Measurement')
            time_level_and_busy_hour=map(lambda x:(x.getAttribute('ID'),MSTCE.extract_time_levels_and_busy_hour(x)),ms)
            for x in range(len(time_level_and_busy_hour)):
                measurement=time_level_and_busy_hour[x][1]
                ret=()
                for y in range(len(measurement)):
                    if  measurement[y]["SkipAggregation"]=="false":
                        ret=list(set(measurement[y]["List_FirstLevelRefValue"])^set(measurement[y]["List_LastLevelRefValue"]))
                        ret.append(measurement[y]["List_LastLevelRefValue"][-1])
                    else:
                        ret=()
                    time_level_and_busy_hour[x][1][y]["di_first_lastLevel"]=ret
            storage_time_list=MSTCE.storage_time_value_table(time_level_and_busy_hour)
            storage_time_list_topologyRef=MSTCE.storage_time_value_table_topologyRef(time_level_and_busy_hour)
            storage_time_table_dict=MSTCE.storage_time_table(storage_time_list,storage_time_list_topologyRef)
            print storage_time_table_dict
            return storage_time_table_dict

            
            


