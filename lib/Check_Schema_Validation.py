'''
Created on Aug 26, 2014

@author: danting
'''

import lxml.etree as ET
import os,sys
from StringIO import StringIO

class xml_schema:
    def compare_input_with_schema(self,schema_file,xml_input_file):

        koala_input_path="metadata"
        schema_folder="Check_Schema"
        
        koala_schema_path = "%s%s%s%s%s%s%s" % (os.path.dirname(os.path.dirname(__file__)), os.path.sep, koala_input_path, os.path.sep, schema_folder, os.path.sep, schema_file)
        
        koala_xml_path = "%s%s%s%s%s%s%s" % (os.path.dirname(os.path.dirname(__file__)), os.path.sep, koala_input_path, os.path.sep, schema_folder, os.path.sep, xml_input_file)

        #open schema_file
        f1=open(koala_schema_path)
        koala_schema=StringIO(f1.read())

        #open koala input
        f2=open(koala_xml_path)
        koala_input=StringIO(f2.read())

        schema_doc=ET.parse(koala_schema)
        schema=ET.XMLSchema(schema_doc)
        
        xml=ET.parse(koala_input)

        print "-----------------------------------------------"
        print xml_input_file
        print schema.validate(xml)
        print schema.error_log

	validate = schema.validate(xml)
	return str(validate)

xs=xml_schema()
xs.compare_input_with_schema("MVI.xsd","Koala3.xml")
