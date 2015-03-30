'''
Created on Aug 16, 2014

@author: danting
'''

class special_chars:
    def get_koala_input(self,input_str):
        input_list=input_str.split('"')
        special_chars_list=[]
        for element in input_list:
            if "&amp;" in element or "&lt;" in element or "&gt;" in element or "&apos;" in element or "&quot;" in element:
                special_chars_list.append(element)
        return special_chars_list

    def check_koala_output(self,output_str,special_chars_list):
        ERR=[]
        for element in special_chars_list:
            if element in output_str:
                print "Pass:",element," is exist"
            else:
                print "ERROR:",element," is not exist"
                ERR.append(element)
        return ERR

