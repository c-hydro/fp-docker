#!/bin/bash -e

# ----------------------------------------------------------------------------------------
# Script information
script_name='FP Docker Entrypoint - HMC Framework'
script_version='1.0.0'
script_date='2020/02/04'

# Argument(s) default definition(s)
file_entrypoint_app_main='fp_docker_entrypoint_app_main.py'
file_entrypoint_app_configuration='fp_docker_entrypoint_app_configuration.json'

# Default script folder
script_folder=$PWD

# Default filename(s)
path_entrypoint_app_main=$script_folder/$file_entrypoint_app_main
path_entrypoint_app_configuration=$script_folder/$file_entrypoint_app_configuration

# Set script Help messages
container_help_text="\
Usage of docker runner:
./fp-docker_entrypoint_app_interface.sh <options>
  	-h	display this help message;
		-m	filename of entrypoint app main;		
  	-c	filename of entrypoint app configuration;"
#-----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Info script start
echo " ==================================================================================="
echo " ==> "$script_name" (Version: "$script_version" Release_Date: "$script_date")"
echo " ==> START ..."

# Source profile environment(s)
source /home/fp/.profile

# Define script option(s)
echo " ===> Get script parameters ... "
while [ -n "$1" ]; do
	case "$1" in
		-m) # filename of entrypoint app main
      	path_entrypoint_app_main=$2
      	;;
  	-c) # filename of entrypoint app configuration
      	path_entrypoint_app_configuration=$2		
      	;;
		*)  # exit message for unknown option
				echo " ===> ERROR: entrypoint app interface option $1 not recognized" 
				exit 1
			;;
	esac
	shift
done
echo " ===> Get script parameters ... OK"
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Check availability of file(s) 
echo " ===> Check entrypoint app main [$path_entrypoint_app_main] ... "
if [ $path_entrypoint_app_main ] ; then
	echo " ===> Check entrypoint app main ... OK"
else
	echo " ===> Check entrypoint app main ... FAILED" 
	exit 1
fi
echo " ===> Check entrypoint app configuration [$path_entrypoint_app_configuration] ... "
if [ $path_entrypoint_app_configuration ] ; then
	echo " ===> Check entrypoint app configuration ... OK"
else
	echo " ===> Check entrypoint app configuration ... FAILED" 
	exit 1
fi
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Info 
echo echo " ===> ENTRYPOINT INTERFACE ... "

# Run interface application 
#python /home/fp/fp_entrypoint/fp_docker_entrypoint_app_main.py -settings_file /home/fp/fp_entrypoint/fp_docker_entrypoint_app_configuration.json
python $path_entrypoint_app_main -settings_file $path_entrypoint_app_configuration

echo echo " ===> ENTRYPOINT INTERFACE ... DONE"
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Info script end
echo " ==> "$script_name" (Version: "$script_version" Release_Date: "$script_date")"
echo " ==> ... END"
echo " ==> Bye, Bye"
echo " ==================================================================================="
# ----------------------------------------------------------------------------------------
