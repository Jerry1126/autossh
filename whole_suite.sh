#!/bin/bash
#
# FILE: whole_suite.sh
#
VERSION="6.1"

#OWNER="Warlock team ---- BSO OSS Mediation Warlock Team List"
#SCM="https://svne1.access.nokiasiemensnetworks.com/isource/svnroot/nas_system/trunk/AutoIntegrationFramework/robot/"
#export SC="AutoIntegrationFramework"

# Tell system our SC name...
CURDIR=$(dirname $0)
if [ $CURDIR == "." ]; then
  CURDIR=$(pwd)
fi
# Remove everything from the beginning until the last '/' char...
TAR_NAME=`echo $CURDIR | sed 's/^.*\///'`
#
## ... then split tar-name to array, using '-remote-test-' as a delimiter,
declare -a TMP_ARR
TMP_ARR=(`echo $TAR_NAME | sed 's/-remote-test-/ /'`)
#
## ... and the component name should be as the array's 1st item.
echo "TMP_ARR is: $$TMP_ARR"
SC=${TMP_ARR[0]}
export SC

###test#

# - - - - - - - - - - - - - - - - - - - - - - - - -  th- - - - - - -

##############added for TEX TA testing mode#################
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ----[ Setup basic arg parsing (provided by TEX) ]---------------------
SETUP_DEFAULT_ARGS="/opt/tex/lib/scripts/setup_default_args.sh"
if [ -x "$SETUP_DEFAULT_ARGS" ]; then
    . $SETUP_DEFAULT_ARGS
fi
# ----[ Setup Default Variables ]---------------------------------------
SDV="/opt/tex/lib/scripts/sdv.sh"
if [ ! -e "$SDV" ]; then
    echo "ERROR: Unable to find \"$SDV\" (Setup Default Variables), check your TEX environment!" >&2
    exit 1
else
    echo "sourcing: $SDV"
    source $SDV
fi

# ----[ Setup Default Variables ]---------------------------------------
SDVpy="./sdv.py"
if [ ! -e "$SDVpy" ]; then
    echo "Warnning: Unable to find \"$SDVpy\" (Setup sdv.py Variables), check your TEX environment!" >&2
else
    echo "sourcing: $SDVpy"
    source $SDVpy
fi


####test ${SDV_WEBSPHERE_APPSERVER_PRIMARY_IP}###

echo "Check if SDV_WEBSPHERE_APPSERVER_PRIMARY_IP is sourced: ${SDV_WEBSPHERE_APPSERVER_PRIMARY_IP}"


# abort on errors and undeclared variables
# set -u -e

##
##All JAVA stuff commented out as currently not using Java to run test cases
##
#export ROBOT_JAVA=/opt/robot/lib/java/jdk1.5.0_15/bin/java
# Updated from jdk1.5.0_15 --> jdk1.6.0_29 (02.08.2012 Silvius)
setup_env TEX_JAVA "$SDV_JAVA_HOME/jdk1.6.0_35/bin/java"  
#setup_env TEX_JAVA "$SDV_JAVA_HOME/jdk1.6.0_35/bin/java"  comment because nac8tex01 no such folder
#setup_env TEX_JAVA "$SDV_JAVA_HOME/jdk1.5.0_15/bin/java"



# export the settings needed by pybot
#export ROBOT_PYTHON="/opt/robot/lib/python/python-2.6.2/bin/python";
#export ROBOT_RUNNER="/opt/robot/robotframework-2.5.3/robot/runner.py";
setup_env TEX_PYTHON_VERSION "python-2.7.3"
setup_env TEX_PYTHON "$SDV_PYTHON_HOME/$TEX_PYTHON_VERSION/bin/python"
#setup_env TEX_JYTHON "$SDV_JYTHON_HOME/jython-2.5.2/jython"


#export ROBOT_RUNNER="/opt/robot/robotframework-2.5.3/robot/runner.py";
# Updated from 2.5.3 --> 2.7.3 (02.08.2012 Silvius). Also changed $SDV_ROBOT_RUNNER --> $SDV_ROBOT_RUN
setup_env TEX_ROBOT_VERSION "robotframework-2.7.5"
setup_env TEX_ROBOT "$SDV_ROBOT_HOME/$TEX_ROBOT_VERSION/$SDV_ROBOT_RUN"  
#setup_env TEX_PYBOT "$SDV_ROBOT_HOME/$TEX_ROBOT_VERSION/bin/pybot"


setup_env TEX_SELENIUM_VERSION "SeleniumLibrary-2.8.1"
setup_env TEX_SELENIUM "${SDV_SELENIUM_HOME}/$TEX_SELENIUM_VERSION"


# export SSHLibrary settings and its siblings to robot
#SSHLibrary="/opt/robot/lib/SSHLibs/SSHLibrary-0.9";
# Updated 0.9 --> 1.0 (21.09.2012 Silvius)
export TEX_SSHLIBS="$SDV_LIB_DIR/sshlibs/SSHLibrary-1.1"
#Paramiko="/opt/robot/lib/SSHLibs/paramiko-1.7.6";
# Updated 1.7.6 --> 1.7.7.1 (21.09.2012 Silvius)
export TEX_PARAMIKO="$SDV_LIB_DIR/sshlibs/paramiko-1.7.7.1"
#Pycrypto="/opt/robot/lib/SSHLibs/pycrypto-2.0.1";
# Updated 2.0.1 --> 2.6 (21.09.2012 Silvius)
export TEX_PYCRYPTO="$SDV_LIB_DIR/sshlibs/pycrypto-2.6"

#SQLAlchemy="/opt/robot/lib/DBLibs/sqlalchemy-0.5.5";
export TEX_SQLALCHEMY="$SDV_LIB_DIR/dblibs/sqlalchemy-0.5.5" 

#cx_Oracle="/opt/robot/lib/DBLibs/cx_Oracle-5.0.2";
export TEX_CXORACLE="$SDV_LIB_DIR/dblibs/cx_Oracle-5.0.2"

# export omniORB libraries to Robot
#omnilib="/opt/robot/lib/CommonLibs/omniORB/omniORBpy-3.4/lib/python2.6/site-packages";
TEX_OMNILIB="$SDV_LIB_DIR/commonlibs/omniORB/omniORBpy-3.4/lib/python2.6/site-packages"

#omniclib="/opt/robot/lib/CommonLibs/omniORB/omniORB-4.1.4/lib";
TEX_OMNICLIB="$SDV_LIB_DIR/commonlibs/omniORB/omniORB-4.1.4/lib"

# export suds library to robot
#sudsLibrary="/opt/robot/lib/CommonLibs/python-suds/python-suds-0.3.9"
TEX_SUDSLIBRARY="$SDV_LIB_DIR/commonlibs/python-suds/python-suds-0.3.9"

# export NWI3 additional libraries for mediation testing where exists
NWI3IDL="./lib/nwi3-idl/"
NWI3="./lib/NWI3TestLibrary/:./lib/NWI3TestLibrary/core/:./lib/NWI3TestLibrary/keywords/:./lib/NWI3TestLibrary/services/:./lib/NWI3TestLibrary/utils/"

#ExcelParser libraries
#XLRD="/opt/robot/lib/CommonLibs/ExcelParser/xlrd-0.7.1";
TEX_XLRD="$SDV_LIB_DIR/commonlibs/ExcelParser/xlrd-0.7.1"

#XLUTILS="/opt/robot/lib/CommonLibs/ExcelParser/xlutils-1.4.1";
TEX_XLUTILS="$SDV_LIB_DIR/commonlibs/ExcelParser/xlutils-1.4.1"

#XLWT="/opt/robot/lib/CommonLibs/ExcelParser/xlwt-0.7.2";
TEX_XLWT="$SDV_LIB_DIR/commonlibs/ExcelParser/xlwt-0.7.2"

# export String Library settings to robot
#StringLibrary="/opt/robot/lib/StringLibrary";
TEX_STRINGLIBRARY="$SDV_LIB_DIR/stringLibrary"

# export instantclient_10_2 to LD_LIBRARY_PATH
#instantclient="/opt/robot/lib/DBLibs/instantclient_10_2";
TEX_INSTANCLIENT="$SDV_LIB_DIR/dblibs/instantclient_10_2"

setup_env TEX_REPORTS_DIR "$SDV_REPORTS_DIR"
export TEX_REPORTS_TMP_DIR="$TEX_REPORTS_DIR"_TMP

# export LD_LIBRARY_PATH
#export LD_LIBRARY_PATH=${instantclient}:${omniclib}
export LD_LIBRARY_PATH=${TEX_INSTANCLIENT}:${TEX_OMNICLIB}

# launch robot
log_dir="$SDV_REPORTS_DIR"
#shift 1




# export String Library settings to robot
#StringLibrary="/opt/robot/lib/StringLibrary";

# export the settings needed by jybot
#export ROBOT_JYTHON="/opt/robot/lib/jython/jython-2.2/jython";

# export trilead Library settings to robot
#TrileadLibrary="/opt/robot/lib/SSHLibrary-0.8/libs/trilead/trilead-ssh2-build213.jar";

# export default classpath
#export CLASSPATH=${TrileadLibrary}:${CLASSPATH}

# launch robot
#log_dir=$1
#shift 1

#exporting syslog info
export ROBOT_SYSLOG_FILE=$log_dir/syslog.log
export ROBOT_SYSLOG_LEVEL=DEBUG



export XML="${SC}_output.xml"
export LOG="${SC}_log.html"
export REPORT="${SC}_report.html"


####test####
export SC_PYTHON_LIB="./lib"
PYTHONPATH=.:$SDV_ROBOT_HOME/$TEX_ROBOT_VERSION:$SC_PYTHON_LIB
PYTHONPATH=$PYTHONPATH:$TEX_SSHLIBS:$TEX_PARAMIKO:$TEX_PYCRYPTO:$TEX_STRINGLIBRARY:$TEX_SUDSLIBRARY:$TEX_SELENIUM
PYTHONPATH=$PYTHONPATH:$SC_HOME/lib/python:$TEX_SQLALCHEMY:$TEX_CXORACLE:$TEX_XLRD:$TEX_XLWT
export PYTHONPATH

# If no specific tests where given, run whole SC, else just run the given ones...
if [ $# -eq 0 ]; then
    TESTSUITE="testcases"
else
    TESTSUITE="$@"
fi

$TEX_PYTHON scripts/pyxbgen.py -u USS/USDescriptor.xsd -m USDescriptor
mv USDescriptor.py lib/UserStory/
##here it will export TEX_SELENIUM_PORT
#selenium_start

#####test#####


$TEX_PYTHON\
    $TEX_ROBOT \
    --pythonpath $PYTHONPATH \
    --variablefile sdv.py \
    --outputdir "$TEX_REPORTS_TMP_DIR" \
    --output "$XML" \
    --log "$LOG" \
    --report "$REPORT" \
    --name "TA_Runner" \
	--variable KOARTE_DIR:xxx \
    "scripts/TA_Runner.html"
#selenium_stop
#cp -rf `pwd` /root/test_bak/
zip -r $TEX_REPORTS_TMP_DIR $TEX_REPORTS_TMP_DIR
mv $TEX_REPORTS_TMP_DIR.zip $TEX_REPORTS_DIR
$SDV_ROBOT_HOME/$TEX_ROBOT_VERSION/bin/rebot --outputdir $TEX_REPORTS_DIR --name KoalaRTE_TASuites --output "$XML" --log "$LOG" --report "$REPORT"  $TEX_REPORTS_TMP_DIR/*.xml
#rm -rf $TEX_REPORTS_TMP_DIR

