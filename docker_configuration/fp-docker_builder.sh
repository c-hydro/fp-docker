
#!/bin/bash

# ----------------------------------------------------------------------------------------
# Script Info
# Convenience script for building a docker image
# Example: docker build -t c-hydro/fp_framework .
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Script information
script_name='FP Docker Builder - HMC Framework'
script_version='1.0.0'
script_date='2020/01/31'

# Define coitainer envaironmente file (default)
container_env_file_default='fp-docker_variables.env'

# Set script Help messages
container_help_text="\
Usage of docker builder:
./fp-docker_builder.sh <options>
  	-h	display this help message;
	-f	script environment filename"
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Info script start
echo " ==================================================================================="
echo " ==> "$script_name" (Version: "$script_version" Release_Date: "$script_date")"
echo " ==> START ..."

# Get the script folder
folder_root=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Define script option(s)
echo " ===> Get script parameters ... "
while [ -n "$1" ]; do
	case "$1" in
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
echo " ===> Get environment filename ... "
if [ $flag_env_file ] ; then
	container_env_file=$container_env_file_pass
	echo " ===> Get environment filename [$container_env_file] ... OK (command-line definition)"
else
	container_env_file=$container_env_file_default
	echo " ===> Get environment filename [$container_env_file] ... OK (default definition)"
fi

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
# Info start
echo echo " ===> BUILD $image_full_name ... "

# Build docker
echo " ===> Build as: docker build "${image_repository}" -f ${image_app_file} -t "${image_full_name}:${image_version}" . "
docker build ${image_repository} -f ${image_app_file} -t ${image_full_name}:${image_version} .

# Info end
echo echo " ===> BUILD $image_full_name ... OK"
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Info script end
echo " ==> "$script_name" (Version: "$script_version" Release_Date: "$script_date")"
echo " ==> ... END"
echo " ==> Bye, Bye"
echo " ==================================================================================="
# ----------------------------------------------------------------------------------------

