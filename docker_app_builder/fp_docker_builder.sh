#!/bin/bash

# ----------------------------------------------------------------------------------------
# Script Info
# Convenience script for building a docker image
# Example: docker build -t c-hydro/fp_framework .

# Explore the content of image (using bash interpreter)
# Example: docker run -it --entrypoint bash c-hydro/fp_framework
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Script information
script_name='FP Docker Builder - Packages Framework'
script_version='1.5.0'
script_date='2022/10/14'

# Define coitainer envaironmente file (default)
container_env_file_default='fp_docker_variables_builder.env'
container_no_cache_default=0
container_remove_default=1

# Set script Help messages
container_help_text="\
Usage of docker builder:
./fp-docker_builder.sh <options>
  	-h	display this help message;
	-f	script environment filename [default: ${container_env_file_default} ];
	-container-remove	remove oldest container  [default: ${container_remove_default} ];
	-container-no-cache	set no-cache container condition [default: ${container_no_cache_default}]"
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
			flag_container_env_file=true
			;;
		-container-remove)  
			container_remove_pass=$2
			#shift # past argument
    		shift # past value		
			flag_container_remove=true
			;;
		-container-no-cache)  
			container_no_cache_pass=$2
			#shift # past argument
    		shift # past value		
			flag_container_no_cache=true
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
echo " ===> Get container environment filename ... "
if [ $flag_container_env_file ] ; then
	container_env_file=$container_env_file_pass
	echo " ===> Get container environment filename [$container_env_file] ... OK (command-line definition)"
else
	container_env_file=$container_env_file_default
	echo " ===> Get container environment filename [$container_env_file] ... OK (default definition)"
fi

# Source environment filename
echo " ===> Source container environment filename  ... "
if [ -f "$container_env_file" ]; then
    source $container_env_file
	while IFS= read -r container_env_line
	do
  		echo " ====> ENV VAR :: $container_env_line"
	done < "$container_env_file"
	echo " ===> Source container environment filename ... OK"
else
	echo " ===> Source container environment filename ... FAILED. Environment file is not available!"
	exit 1
fi
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Set no-cache condition
echo " ===> Set container no-cache condition ... "
if [ $flag_container_no_cache ] ; then
	container_no_cache=$container_no_cache_pass
	echo " ===> Set container no-cache condition [$container_no_cache] ... OK (command-line definition)"
else
	container_no_cache=$container_no_cache_default
	echo " ===> Set container no-cache condition [$container_no_cache] ... OK (default definition)"
fi
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Set no-cache condition
echo " ===> Remove container condition ... "
if [ $flag_container_remove ] ; then
	container_remove=$container_remove_pass
	echo " ===> Remove container condition [$container_no_cache] ... OK (command-line definition)"
else
	container_remove=$container_remove_default
	echo " ===> Remove container condition [$container_no_cache] ... OK (default definition)"
fi
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
# Define full name of image
image_docker_reference="${image_docker_name}/${image_docker_tag}"

# Check image
echo " ===> Check container '${image_docker_reference}' ... "

if [[ "$(docker images inspect ${image_docker_reference} >/dev/null 2>&1)" ]] ; then
	if [[ "${container_remove}" -eq 1 ]] ; then
		docker rmi ${image_docker_reference}
		echo " ===> Check container '${image_docker_reference}' ... FOUND. IMAGE WAS REMOVED ACCORDING WITH RELATED FLAG"
	else
		echo " ===> Check container '${image_docker_reference}' ... FOUND. IMAGE WAS NOT REMOVED ACCORDING WITH RELATED FLAG"
	fi
else
	echo " ===> Check container '${image_docker_reference}' ... NOT FOUND."
fi

# Build image
echo " ===> Build container '$image_docker_reference' ... "

# Building conditions
if [[ "${container_no_cache}" -eq 1 ]] ; then
	echo " ===> Build as: docker build "${image_docker_repository}" -f ${image_docker_file} -t "${image_docker_reference}:${image_docker_version}" . [CACHE FALSE]"
	docker build --no-cache ${image_docker_repository} -f ${image_docker_file} -t ${image_docker_reference}:${image_docker_version} .
	echo " ===> Build container '$image_docker_reference' ... OK"
elif [[ "${container_no_cache}" -eq 0 ]] ; then
	echo " ===> Build as: docker build "${image_docker_repository}" -f ${image_docker_file} -t "${image_docker_reference}:${image_docker_version}" . [CACHE TRUE]"
	docker build ${image_docker_repository} -f ${image_docker_file} -t ${image_docker_reference}:${image_docker_version} .
	echo " ===> Build container '$image_docker_reference' ... OK"
else
	echo " ===> Condition to cache container must be 0/1 [False/True]. Actual value is: ${container_no_cache}. Change the argument value."
	echo " ===> Build container '$image_docker_reference' ... FAILED"
	exit 1
fi
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Info script end
echo " ==> "$script_name" (Version: "$script_version" Release_Date: "$script_date")"
echo " ==> ... END"
echo " ==> Bye, Bye"
echo " ==================================================================================="
# ----------------------------------------------------------------------------------------

