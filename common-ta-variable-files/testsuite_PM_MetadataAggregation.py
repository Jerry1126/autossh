import os
#
# Give here a relative directory path to PM test data folder containing
# test data for PM metadata testing.
# See format from:
#   https://confluence.inside.nokiasiemensnetworks.com/display/Unify60/KOALA+Based+PM+Metadata+TA+Specification+for+OnePM
#
TEST_DATA_FOLDER = "%s%s%s%s%s" % (os.path.dirname(os.path.dirname(__file__)), os.path.sep, 'metadata', os.path.sep, 'fetameta')

#
#This file has the expected / possible content for providing Adaptation "Extension" or customization Metadata details on top of OnePM Test Data.
ADAPTATION_EXTENSION_FILE = "%s%s%s%s%s%s%s" % (os.path.dirname(os.path.dirname(__file__)), os.path.sep, 'metadata', os.path.sep, 'extensionFile',os.path.sep, 'adaptationMetadataExtensionKSC.xml')

#
# GENERATE_KOALA_RAW_ID can be enabled (un-comment) and set to True if wanted
# to generate KOALA Raw Ids from Object class names.
# See more details from MetadataTester's library documentation
# `KOALA Raw ID based View Names` section.
#
# GENERATE_KOALA_RAW_ID = "True"

#
# use it to exclude those can not compare exactly due to special case BH criteria.
# list all measurement type in following variable. like ['AMRXQ', 'EQOS', 'M3UAS']
#IGNORED_MEASUREMENTS_FOR_BH_VERIFICATION = []