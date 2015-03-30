import os
#
# Give here a relative directory path to PM test data folder containing
# test data for PM metadata testing.
# See format from:
#   https://confluence.inside.nokiasiemensnetworks.com/display/Unify60/KOALA+Based+PM+Metadata+TA+Specification+for+OnePM
#
TEST_DATA_FOLDER = "%s%s%s%s%s" % (os.path.dirname(os.path.dirname(__file__)), os.path.sep, 'metadata', os.path.sep, 'fetameta')

#list of Lightweight Objects
LWO_LIST=['TTP','SEG']
#LWO and Koala ID mapping, it used to handle the duplication in dimensions
#When there are duplication in dimension, the second LWO should be replaced with Koala ID
#Mostly it can be empty
LWO_LEVEL_MAP_IN_KOALA={}

#List all supported suffix of object column names 
LIST__SUPPORTED_SUFFIXES=["ID", "GID"]

#As some counters may have same suffix  as object column name, this variable could be used
#to define these counters which have same suffix, and it will be ignored and do object column check
#LIST__IGNORED_COLUMN_NAMES=['FREQ_GROUP_ID','CELL1_ID','CELL2_ID','CELL3_ID','CELL4_ID','CELL5_ID','CELL6_ID','CELL7_ID','CELL8_ID',
#                            'CELL9_ID','FREQUENCY_GROUP_ID','CELL_ID','CELL10_ID','DLCI_1_ID','DLCI_2_ID','DLCI_3_ID','DLCI_4_ID',
#                            'DLCI_5_ID','DLCI_6_ID','DLCI_7_ID','DLCI_8_ID','DLCI_9_ID','DLCI_10_ID','DLCI_11_ID','DLCI_12_ID','DLCI_13_ID',
#                            'DLCI_14_ID','DLCI_15_ID','DLCI_16_ID']

LIST__IGNORED_COLUMN_NAMES=[]

MO_COLUMN_NAME_MAPPING = {}