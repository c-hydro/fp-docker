#!/bin/bash

# ----------------------------------------------------------------------------------------
# Script Info
# Convenience script for running the FP Docker container.
# Example:
# docker run --env-file=fp-docker_variables_hmc.env -it --entrypoint bash c-hydro/fp_framework_hmc
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Script information
script_name='FP Docker Runner - HMC Framework'
script_version='1.0.1'
script_date='2020/04/23'

# Define coitainer envaironmente file (default)
container_env_file_default='fp-docker_variables_hmc.env'

# Set script Help messages
container_help_text="\
Usage of docker runner:
./fp-docker_runner.sh <options>
  	-h	display this help message;
	-f	script environment filename;		
  	-i	run the docker container interactively;"
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Info script start
echo " ==================================================================================="
echo " ==> "$script_name" (Version: "$script_version" Release_Date: "$script_date")"
echo " ==> START ..."

# Define script option(s)
echo " ===> Get script parameters ... "
while [ -n "$1" ]; do
	case "$1" in
		-i) 	# script runs the container interactively:
      		container_extra_opts='-it --entrypoint=bash'
			flag_mode_interactive=true
      		;;
    	-h) 	# script calls help comment
      		echo "$container_help_text"			
      		exit 0
      		;;
		-f)  
			container_env_file_pass=$2
			#shift # past argument
    		shift # past value		
			flag_env_file=true
			;;
		*)  
			echo " ===> ERROR: container option $1 not recognized" 
			exit 1
			;;
	esac
	shift
done
echo " ===> Get script parameters ... OK"
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Get environment filename
echo " ===> Set container mode ... "
if [ $flag_mode_interactive ] ; then
	echo " ===> Set container mode ... INTERACTIVE"
else
	echo " ===> Set container mode ... AUTOMATIC"
fi

# Get environment filename
echo " ===> Get environment filename ... "
if [ $flag_env_file ] ; then
	container_env_file=$container_env_file_pass
	echo " ===> Get environment filename [$container_env_file] ... OK (command-line definition)"
else
	container_env_file=$container_env_file_default
	echo " ===> Get environment filename [$container_env_file] ... OK (default definition)"
fi
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Source environment filename
echo " ===> Source environment filename  ... "
if [ -f "$container_env_file" ]; then
    source $container_env_file
	while IFS= read -r container_env_line
	do
  		echo " ====> ENV VAR :: $container_env_line"
	done < "$container_env_file"
	echo " ===> Source environment filename ... OK"
else
	echo " ===> Source environment filename ... FAILED. Environment file is not available!"
	exit 1
fi
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Define full name of image
image_full_name="${image_base_name}/${image_app_name}"
# Info 
echo echo " ===> Run $image_full_name "

# Run docker
docker run ${container_extra_opts}\
 	--workdir ${container_workdir}\
 	--name ${container_name}\
 	-e APP_MAIN=${image_app_entrypoint_main} -e APP_CONFIG=${image_app_entrypoint_configuration}\
 	--rm\
 	--env-file ${container_env_file}\
 	--mount type=bind,source=${SOURCE_DATA_STATIC_LAND},target=${TARGET_DATA_STATIC_LAND}\
	--mount type=bind,source=${SOURCE_DATA_STATIC_POINT},target=${TARGET_DATA_STATIC_POINT}\
 	--mount type=bind,source=${SOURCE_DATA_DYNAMIC_RESTART},target=${TARGET_DATA_DYNAMIC_RESTART}\
	--mount type=bind,source=${SOURCE_DATA_DYNAMIC_SOURCE},target=${TARGET_DATA_DYNAMIC_SOURCE}\
 	--mount type=bind,source=${SOURCE_DATA_DYNAMIC_ARCHIVE},target=${TARGET_DATA_DYNAMIC_ARCHIVE}\
 	${image_full_name}:${image_version}
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Info script end
echo " ==> "$script_name" (Version: "$script_version" Release_Date: "$script_date")"
echo " ==> ... END"
echo " ==> Bye, Bye"
echo " ==================================================================================="
# ----------------------------------------------------------------------------------------
