Flood PROOFS Virtualization
===========================

Welcome to the **FloodPROOFS Modelling System** GitHub repository. This is a Modelling System supported by the Italian 
Civil Department (DPC) and is used for preventing and reducing hydrogeological risk.

Background
**********

Flood-PROOFS 
------------

**Flood-PROOFS** (Flood PRObabilistic Operative Forecasting System) is a system designed by CIMA Research Foundation 
to support decision makers during the operational phases of flood forecasting and monitoring. The goal is to protect 
the population and infrastructure from damage caused by intense precipitation events.

The Flood-PROOFS system manages the data flow deriving from various modelling tools developed by the CIMA Research 
Foundation to return a quantitative assessment of the effects that precipitation can have on the territory in terms of 
flow and probability to overcome the critical thresholds in the different basins. 

The system has been operating since 2008 at various Functional Centers (Autonomous Region of Valle d'Aosta and Marche) 
where it is used for the issue of hydro-meteorological warnings for civil protection purposes. At the technical offices of 
tùhe Valle d'Aosta Water Company (CVA) it is instead useful to study and implement strategies to mitigate flood events or 
to secure facilities in the event of flooding.

Virtualization
--------------

In computing, **virtualization** refers to the act of creating a virtual (rather than actual) version of something, including 
virtual computer hardware platforms, storage devices, and computer network resources. Virtualization began in the 1960s, 
as a method of logically dividing the system resources provided by mainframe computers between different applications. 
Since then, the meaning of the term has broadened.

The virtualization of Flood-PROOFS modelling system, is performed by using the **Docker framework**. In fact, Docker_ is an 
open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your 
infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you 
manage your applications. 

.. _Docker: http://www.python.org/

Prerequisites
*************

In order to use the Docker framework, the users have to perform the following steps:

1. Uninstall old Docker version:

    .. code-block:: bash
    
    	>> sudo apt-get remove docker docker-engine docker.io containerd runc

2. Update the apt package index:

    .. code-block:: bash
    
    	>> sudo apt-get update

3. Install packages to allow apt to use a repository over HTTPS:
   
    .. code-block:: bash
    
    	>> sudo apt-get install apt-transport-https 
    	>> sudo apt-get install ca-certificates 
    	>> sudo apt-get install curl 
    	>> sudo apt-get install gnupg2
    	>> sudo apt-get install software-properties-common

4. Add Docker’s official GPG key:

    .. code-block:: bash
    
    	>> curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -

5. Verify that you now have the key with the fingerprint 9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88, by searching for the last 8 characters of the fingerprint:

    .. code-block:: bash
    
    	>> sudo apt-key fingerprint 0EBFCD88
    
6. Use the following command to set up the stable repository:

    .. code-block:: bash
    
    	>> sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

7. Install the latest version of Docker Engine - Community and containerd:

    .. code-block:: bash
    
    	>> sudo apt-get install docker-ce docker-ce-cli containerd.io

8. Manage Docker as a non-root user:

	- Create the docker group:

	.. code-block:: bash

		>> sudo groupadd docker

	- Add your user to the docker group:

	.. code-block:: bash

		>> sudo usermod -aG docker $USER

	- Activate the changes to groups:

	.. code-block:: bash

		>> newgrp docker 

If this error happens:
	
    .. code-block:: bash
    
    	>> WARNING: Error loading config file: /home/user/.docker/config.json - stat /home/user/.docker/config.json: permission denied

users can solve it applying the following commands:

    .. code-block:: bash
    
    	>> sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
    	>> sudo chmod g+rwx "$HOME/.docker" -R		

Docker components
*****************

The github repository contains different folders for storing all Docker components in order to allow the virtualization of
the Flood-PROOFS modelling system. The structure of the repository is reported below [1_]:

::
	
	fp-docker
	├── docker_configuration
	│   ├── fp-docker_builder.sh
	│   ├── fp-docker_file
	│   ├── fp-docker_runner.sh
	│   └── fp-docker_variables.env
	├── docker_entrypoint
	│   ├── fp_docker_entrypoint_app_configuration.json
	│   ├── fp-docker_entrypoint_app_interface.sh
	│   └── fp_docker_entrypoint_app_main.py
	├── AUTHORS.rst
	├── CHANGELOG.rst
	├── LICENSE.rst
	└── README.rst

Particularly:

    • **docker_configuration**: tools to build and run the Flood-PROOFS dockers.
    • **docker_entrypoint**: tools to configure the entrypoints of the Flood-PROOFS dockers.
    • **docker_testcase**: datasets to test the Flood-PROOFS dockers.

All codes and datasets are freely available and users can be get them from our github repository [2_].

First, let's cover some important points about Docker that will help explain the scripts and tools in the following parts. 
In Dockerland, there are images and containers. The two are closely related, but distinct; grasping this dichotomy clarifies
Docker immensely.
An **image** is an inert, immutable, file that's essentially a snapshot of a container. Images are created with the build 
command, and they'll produce a container when started with run. Images are stored in a Docker registry such as 
registry.hub.docker.com. Because they can become quite  large, images are designed to be composed of layers of other images, 
allowing a minimal amount of data to be sent when transferring images over the network.
To use a programming metaphor, if an image is a class, then a **container** is an instance of a class—a runtime object. 
Containers are hopefully why you're using Docker; they're lightweight and portable encapsulations of an environment in which 
to run applications.

The major difference between Docker containers and images is that containers have a writable layer. When you create a Docker 
container, you’re adding a writable layer on top of the Docker image. You can run many Docker containers from the same Docker 
image. You can see a Docker container as an instance of a Docker image.

Build dockers
*************

The docker **build command** builds images from a Dockerfile and a “context”. A build’s context is the set of files 
located in the specified PATH or URL. The build process can refer to any of the files in the context. For example, your build 
can use a COPY instruction to reference a file in the context.

In order to build the Dockers, in the **docker_configuration** and in **docker_entrypoint** folders, bash and python3 scripts, 
Dockerfiles and environment variable files are provided. The generic command-line to invoke the building of the Docker file is the following:

    .. code-block:: bash
    
    	>> ./fp-docker_builder.sh -f fp-docker_variables.env

where the -f flag is used to pass the Environment variable file to the building script.

Environment variable file
-------------------------

The Docker **environment variable file** (.env) is crucial when you're creating complex container deployments. As you might 
expect from the name, this file allows you to declare environment variables for your containers. This comes in quite handy, 
as the .env file can be reused for other containers or quickly edited.
For the Flood-PROOFS virtualization an example of .env file is reported below:

    :: 
    
    	# Docker static argument(s)
    	image_version='latest'
    	image_base_name='c-hydro'
    	image_app_name='fp_framework'
    	image_app_file='fp-docker_file'
    	image_repository=''
    	container_workdir='/home/fp/fp_entrypoint/'
    	container_name='lexis'
    
    	image_app_entrypoint_main='fp_docker_entrypoint_app_main.py'
    	image_app_entrypoint_configuration='fp_docker_entrypoint_app_configuration.json'
    
    	# Docker dynamic argument(s) [SOURCE::local, TARGET::container]
    	SOURCE_DATA_STATIC='$HOME/docker-ws/data/data_static/'
    	SOURCE_DATA_DYNAMIC_SOURCE='$HOME/docker-ws/data/dynamic_data/source/'
    	SOURCE_DATA_DYNAMIC_ARCHIVE='$HOME/docker-ws/data/dynamic_data/archive/'
    	TARGET_DATA_STATIC='/home/fp/fp_mount/data/data_static/'
    	TARGET_DATA_DYNAMIC_SOURCE='/home/fp/fp_mount/data/data_dynamic/source/'
    	TARGET_DATA_DYNAMIC_ARCHIVE='/home/fp/fp_mount/data/data_dynamic/archive/'
    	RUN_TIME_NOW=2019-05-12 11:00					
    	RUN_TIME_STEPS_OBS=4
    	RUN_TIME_STEPS_FOR=0
    	RUN_NAME='fp_run'
    	RUN_ENS=false

All the information are used in building and running parts. To achive a correct settings of Flood-PROOFS Dockers
all the fields must be filled. In the following lines, an example of fields of docker envariable file.

Generally, the first part is for the building section:

* image_version: version of the image [string];
* image_base_name: base name of the image [string];
* image_app_name: application name of the image [string]; 
* image_app_file: filename of the image Dockerfile [string];
* image_repository: source root of the image (e.g. in GitHub) [string];
* container_workdir: absolute path of the working directory referred to the container [string];
* container_name: name of the container [string];
* image_app_entrypoint_main: application filename for configuring entrypoint activities [string];
* image_app_entrypoint_configuration: configuring filename of the entrypoint activities [string].

In the second part, users can found the running section:

* SOURCE Folders: absolute paths referred to the host folders [string]:

	- SOURCE_DATA_STATIC: folders for static datasets;
	- SOURCE_DATA_DYNAMIC: folders for dynamic datasets.

* TARGET folders: absolute paths referred to the container folders [string];

	- TARGET_DATA_STATIC: folders for static datasets;
	- TARGET_DATA_DYNAMIC: folders for dynamic datasets;

* RUN_TIME_NOW: reference time of the simulation (e.g. time reference for a test case or for a real-time simulation) [yyyy-mm-dd HH:MM];
* RUN_TIME_STEPS_OBS: time steps in the simulation observed part [integer];
* RUN_TIME_STEPS_FOR: time steps in the simulation forecasting part [integer];
* RUN_NAME: name of the simulation [string];
* RUN_ENS: simulation mode (deterministic/probabilistic) [boolean: false/true].

Other environment variables can be listed for different dockers and procedures.

Dockerfile
----------

Docker can build images automatically by reading the instructions from a **Dockerfile**. A Dockerfile is a text document that 
contains all the commands a user could call on the command line to assemble an image. Using docker build users can create an 
automated build that executes several command-line instructions in succession.

In Flood-PROOFS virtualization, Dockers are set on 64 bit Linux Debian/Ubuntu distribution (e.g. 18.04, 18.10) and the building part uses the tools downloaded from the github c-hydro repository for installing libraries, packages and applications [3_].
The default build of Docker images provides the configuration of:

* system libraries needed by the modelling system (e.g. ZLIB, HDF5, NetCDF4) [4_];
* python3_ virtual environment based on miniconda_ framework;
* python3 packages for processing data, runnning model and postprocessing or visualizing results (e.g fp-hyde, hmc, fp-hat);
* an entrypoint script to configure processes and applications according with the run options. 						

An example of Dockerfile is reported below:

.. _python3: https://www.python.org
.. _miniconda: https://conda.io/miniconda.html

    :: 
    
    	# start from base -- builder
    	FROM ubuntu:18.10 as builder
    
    	# label(s)
    	LABEL maintainer="Fabio Delogu"
    	LABEL email="fabio.delogu@cimafoundation.org"
    	LABEL version="1.0.0"
    	LABEL release_date="2020/02/04"
    
    	# change default shell (from sh to bash)
    	SHELL ["/bin/bash", "-c"]
    
    	# install system-wide deps 
    	RUN apt-get update && apt-get install -y \
    		git \
    		gfortran \
    		gcc \
    		m4 \
    		g++ \
    		make \
    		mc \
    		curl \
    		build-essential \
    		wget \
    		cmake \
    		libcurl4-openssl-dev \
    		openjdk-8-jdk \
    		bash-completion
    
    	# set user and workdir check
    	RUN useradd -m -p fp -s /bin/bash fp
    	WORKDIR /home/fp/
    	USER fp
    	RUN pwd
    
    	# set environment folder(s)
    	ENV fp_folder_entrypoint /home/fp/fp_entrypoint/
    	ENV fp_folder_libs_installer /home/fp/fp_envs/fp_libs_installer/
    	ENV fp_folder_libs_system /home/fp/fp_envs/fp_libs_system/
    	ENV fp_folder_libs_python /home/fp/fp_envs/fp_libs_python/
    	ENV fp_folder_package_hmc /home/fp/fp_package/fp_hmc/
    	ENV fp_folder_mount /home/fp/fp_mount/
    
    	# set environment filename(s)
    	ENV fp_file_env_system fp_env_system
    	ENV fp_file_env_python fp_env_python
    
    	# create folder
    	RUN mkdir -p ${fp_folder_libs_installer}
    	RUN mkdir -p ${fp_folder_package_hmc}
    	RUN mkdir -p ${fp_folder_entrypoint}
    	RUN mkdir -p ${fp_folder_mount}
    
    	# get fp envs from github repository
    	RUN git clone https://3a99fb49454e54c836f69cca7b1c6034c32f798a:x-oauth-basic@github.com/c-hydro/fp-envs.git --branch v1.5.2 --single-branch /tmp/fp-envs
    	# copy files from tmp to container folder(s)
    	RUN cp -r /tmp/fp-envs/. ${fp_folder_libs_installer} 
    
    	...

Entrypoint
----------

The **ENTRYPOINT instruction** define what command gets executed when running a container. Dockerfile should specify an ENTRYPOINT command in order to define when the container will be run as an executable. It is possible to set a CMD command to define the default arguments for an ENTRYPOINT command or for executing an ad-hoc command in a container. In this case, CMD will be overridden when running the container with alternative arguments.

In the Flood-PROOFS virtualization the ENTRYPOINT is defined by three elements:

* a **bash script** to interface the host machine and the container [fp-docker_entrypoint_app_interface.sh];
* a **python3 script** to run all the configured application [fp_docker_entrypoint_app_main.py];
* a **json file** to configure the python3 script [fp_docker_entrypoint_app_configuration.json].

In the building part, the bash script is set using the ENTRYPOINT keyword; during the running part (if set in automatic mode),
the container executes the bash script to run the python3 script with its configuration file.

Run dockers
***********

The docker **run command** first creates a writeable container layer over the specified image, and then starts it using the 
specified command. A stopped container can be restarted with all its previous changes intact using docker start.
When an operator executes docker run, the container process that runs is isolated in that it has its own file system, its own 
networking, and its own isolated process tree separate from the host.

In Flood-PROOFS virtualization, the running part can be activated in two configuration:

* Executable mode:

	.. code-block:: bash

		>> ./fp-docker_runner.sh -f fp-docker_variables.env 

* Debug mode:

	.. code-block:: bash

		>> ./fp-docker_runner.sh -i -f fp-docker_variables.env 

where the -f flag is used to pass the Environment variable file to the building script.
An example, of the container structure is reported below:

    ::
    
    	fp
    	├── fp_entrypoint
    	│   ├── fp_docker_entrypoint_app_configuration.json
    	│   ├── fp-docker_entrypoint_app_interface.sh
    	│   └── fp_docker_entrypoint_app_main.py
    	├── fp_envs
    	│   ├── fp_libs_installer
    	│   │   ├── miniconda.sh
    	│   │   ├── setup_fp_env_hmc.sh
    	│   │   ├── setup_fp_env_python.sh
    	│   │   └── setup_fp_env_system.sh
    	│   ├── fp_libs_python
    	│   └── fp_libs_system
    	│       ├── fp_env_system
    	│       ├── hdf5
    	│       ├── hmc
    	│       ├── nc4
    	│       ├── source
    	│       └── zlib
    	├── fp_logs
    	│   ├── hmc_adapter_log_docker.txt
    	│   └── hmc_runner_log_docker.txt
    	├── fp_mount
    	│   ├── archive
    	│   │   └── 2019
    	│   └── data
    	│       ├── forcing
    	│       └── static
    	├── fp_package
    	│   └── fp_hmc
    	│       ├── apps
    	│       ├── AUTHORS.rst
    	│       ├── bin
    	│       ├── CHANGELOG.rst
    	│       ├── docs
    	│       ├── hmc
    	│       ├── LICENSE.rst
    	│       ├── README.rst
    	│       └── readthedocs.yml
    	└── fp_run
    	    ├── cache
    	    ├── data
    	    │   ├── forcing
    	    │   ├── outcome
    	    │   ├── restart
    	    │   └── state
    	    ├── exec
    	    │   ├── hmc.log
    	    │   ├── HMC_Model_V2_wrf_deterministic.x
    	    │   └── marche.info.txt
    	    └── tmp

Flood-PROOFS Applications
*************************

LEXIS project
-------------

The Flood-PROOFS virtualization is applied in **LEXIS project**; the main goal is organize an 
operational chain using the computing resources available in a cloud framework. The simulations
that will be implemented are defined as follow:

* **fp_state_ws_observed**

	Simulation based on the weather station observations to generate the initial conditions of the 
	Hydrological Model Continuum. The simulation covers the observed period.

	- simulation_length_obs: 10 days
	- simulation_length_for: 0 days
	- simulation_domain_n: NA
	- simulation_type: deterministic
	- simulation_n: 1/day * simulation_domain	

* **fp_run_ws_observed**

	Simulation based on the weather station observations to compute the time-series datasets (e.g discharge, 
	dams volume and level) and the spatial information (e.g. soil moisture, evapotranspiration and snow cover) 
	using the Hydrological Model Continuum. The simulation covers the observed period.

	- simulation_length_obs: 2 days
	- simulation_length_for: 0 days
	- simulation_domain_n: NA
	- simulation_type: deterministic
	- simulation_n: 1/day * simulation_domain

* **fp_run_nwp_deterministic**

	Simulation based on the weather station observations and on the nwp datasets to compute the time-series datasets (e.g discharge, 
	dams volume and level) and the spatial information (e.g. soil moisture, evapotranspiration and snow cover) 
	using the Hydrological Model Continuum. The simulation covers both the observed and the forecasting periods.

	- simulation_length_obs: 2 days
	- simulation_length_for: 2 days
	- simulation_domain_n: NA
	- simulation_type: deterministic
	- simulation_n: 1/day * simulation_domain

* **fp_run_nwp_probabilistic**	
  
	Simulation based on the weather station observations and on the perturbed and disaggregated nwp datasets to compute the 
	time-series datasets (e.g discharge, dams volume and level) and the spatial information (e.g. soil moisture, evapotranspiration 
	and snow cover) using the Hydrological Model Continuum. The simulation covers both the observed and the forecasting periods.

	- simulation_length_obs: 2 days
	- simulation_length_for: 2 days
	- simulation_domain_n: NA
	- simulation_type: probabilistic
	- simulation_n: 30/day * simulation_domain

* **fp_test_nwp_deterministic**

    For testing each components of the operational chain, the users have to set the test case based on an
	example of nwp deterministic run.
	The test case is based on two different procedures:

	1. The **Hyde Docker**: to collect the observed datasets and the nwp wrf outcome; finally, to prepare datasets for the hydrological model;
	2. The **HMC Docker**: to run the Continuum hydrological model using the data previously collected.

	The dockers have to be prepared following the steps below: 

    * download the **docker_testcase** folders from the github repository [1_];
    * create and update the **fp-docker_variables_hmc.env** and **fp-docker_variables_hyde.env** files according with the host, the containers and the simulation features.

	The **Hyde Docker** has to be prepared and run following the steps below:

	a) configuring the folders and the parameters in the fp-docker_variables_hyde.env file:

	- SOURCE_DATA_STATIC='/docker_testcase/datasets_hyde/data/static_data/land/'
	- SOURCE_DATA_DYNAMIC_RAW='/docker_testcase/datasets_hyde/dynamic_data/'
	- SOURCE_DATA_DYNAMIC_PROCESSED='/docker_testcase/datasets_hyde/processed_data/'
	- RUN_TIME_NOW=2020-06-17 00:00					
	- RUN_TIME_STEPS_OBS=10
	- RUN_TIME_STEPS_FOR=24
	- RUN_NAME='fp_hyde_wrf'
	- RUN_DOMAIN='marche'
	- RUN_ENS=false
	
	b) building the image:
	
	.. code-block:: bash
	
		>> 	./fp-docker_builder.sh -f fp-docker_variables_hyde.env

	c) Put the observed datasets and the nwp wrf datasets in the SOURCE_DATA_DYNAMIC_RAW folder; the structure of datasets will be as follows:

	.. code-block:: bash

		docker datasets
		├── dynamic_data
		│   ├── anag-ANEMOMETRO.json
		│   ├── anag-IGROMETRO.json
		│   ├── anag-PLUVIOMETRO.json
		│   ├── anag-RADIOMETRO.json
		│   ├── anag-TERMOMETRO.json
		│   ├── ANEMOMETRO.json
		│   ├── auxhist23_d03_2020-06-17_00:00:00
		│   ├── auxhist23_d03_2020-06-17_01:00:00
		│   ├── ...
		│   ├── ...
		│   ├── auxhist23_d03_2020-06-18_00:00:00
		│   ├── IGROMETRO.json
		│   ├── PLUVIOMETRO.json
		│   ├── RADIOMETRO.json
		│   └── TERMOMETRO.json
		├── processed_data
		└── static_data
		    └── land
			├── marche.aspect.txt
			├── marche.dem.txt
			├── marche.hillshade.txt
			├── marche.roughness.txt
			└── marche.slope.txt
		
	c) running the container in executable mode:
	
	.. code-block:: bash
	
		>> 	./fp-docker_runner_hyde.sh -f fp-docker_variables_hyde.env 

	d) collecting the datasets in the SOURCE_DATA_DYNAMIC_PROCESSED folder of the Hyde docker and copy it to the source folder SOURCE_DATA_DYNAMIC_SOURCE of the HMC docker:

	.. code-block:: bash

		>> 	cp /docker_testcase/datasets_hmc/dynamic_data/wrf_{date_outcome_string}_{domain_string}.nc.gz /docker_testcase/datasets_hmc/dynamic_data/'
		
	If the users need to open the Hyde Docker in interctive mode, they can use the follow command-line:

	.. code-block:: bash

		>> 	docker run --workdir /home/fp/fp_entrypoint/\ 
			-e APP_MAIN=fp_docker_entrypoint_app_main_hyde.py -e APP_CONFIG=fp_docker_entrypoint_app_configuration_hyde.json\
			--rm  --env-file fp-docker_variables_hyde.env\
			-it --entrypoint bash  
			--mount type=bind,source=${SOURCE_DATA_STATIC},target=${TARGET_DATA_STATIC}\
			--mount type=bind,source=${SOURCE_DATA_DYNAMIC_RAW},target=${TARGET_DATA_DYNAMIC_RAW}\
			--mount type=bind,source=${SOURCE_DATA_DYNAMIC_PROCESSED},target=${TARGET_DATA_DYNAMIC_PROCESSED}\  
			c-hydro/fp_framework_hyde

	The **HMC Docker** has to be prepared and run following the steps below:

	a) configuring the folders and the parameters in the fp-docker_variables_hmc.env file:

	- SOURCE_DATA_STATIC_LAND='/docker_testcase/datasets_hmc/static_data/land/'
	- SOURCE_DATA_STATIC_POINT='/docker_testcase/datasets_hmc/static_data/point/'
	- SOURCE_DATA_DYNAMIC_SOURCE='/docker_testcase/datasets_hmc/dynamic_data/'
	- SOURCE_DATA_DYNAMIC_RESTART='/docker_testcase/datasets_hmc/dynamic_restart/'
	- SOURCE_DATA_DYNAMIC_ARCHIVE='/docker_testcase/datasets_hmc/docker_data/'
	- RUN_TIME_NOW=2020-03-20 00:00					
	- RUN_TIME_STEPS_OBS=10
	- RUN_TIME_STEPS_FOR=15
	- RUN_NAME='fp_run'
	- RUN_ENS=false
		
	The users have to be check that the dynamic datasets are in the SOURCE_DATA_DYNAMIC_SOURCE. Particularly:

	- the wrf datasets elaborated by the Hyde Docker;
	- the observed datasets for the previous 24 hours available on the **docker_testcase** folders hosted by github.

	b) building the image:
	
	.. code-block:: bash
	
		>>	./fp-docker_builder.sh -f fp-docker_variables_hmc.env
		
	c) running the container in executable mode:
	
	.. code-block:: bash
	
		>>	./fp-docker_runner_hmc.sh -f fp-docker_variables_hmc.env 

	d) collecting the results of the Continuum hydrological model in the SOURCE_DATA_DYNAMIC_ARCHIVE.

	If the users need to open the HMC Docker in interctive mode, they can use the follow command-line:

	.. code-block:: bash

		>> 	docker run --workdir /home/fp/fp_entrypoint/\ 
			-e APP_MAIN=fp_docker_entrypoint_app_main_hmc.py -e APP_CONFIG=fp_docker_entrypoint_app_configuration_hmc.json\
			--rm  --env-file fp-docker_variables_hmc.env\
			-it --entrypoint bash\
			--mount type=bind,source=${SOURCE_DATA_STATIC_LAND},target=${TARGET_DATA_STATIC_LAND}\
			--mount type=bind,source=${SOURCE_DATA_STATIC_POINT},target=${TARGET_DATA_STATIC_POINT}\
			--mount type=bind,source=${SOURCE_DATA_DYNAMIC_RESTART},target=${TARGET_DATA_DYNAMIC_RESTART}\
			--mount type=bind,source=${SOURCE_DATA_DYNAMIC_SOURCE},target=${TARGET_DATA_DYNAMIC_SOURCE}\ 
			--mount type=bind,source=${SOURCE_DATA_DYNAMIC_ARCHIVE},target=${TARGET_DATA_DYNAMIC_ARCHIVE}\ 
			c-hydro/fp_framework_hmc

Potential Users
***************

The Flood-PROOFS Modelling System and the Docker virtualization have been released to enable different applications (for example local/regional scenario assessment) and further development by external users.

Potential users are anticipated to predominately be interested in the ability to run the system with local data (including scenario modelling) and to 
modify the system with new capabilities. The potential collaborators have expressed a range of potential goals for their use of the modelling system, 
including performing comparisons with existing models, tailoring the hydrological performance to specific land uses and cropping types.

Broadly speaking, there are four potential user categories:

    • **Data user**: who accessing the model outputs.
    • **Case study user**: who work to evaluate his/her case using data over a selected time period.
    • **Applying users**: who would primarily be interested in applying the current model to a region of interest using localised and/or scenario data where available.
    • **Contributor users**: who will extend the capabilities of the model with new research and coding (modify the system with new capabilities)

It is expected that the majority of early adopters of the FloodPROOFS modelling system will be Applying users looking to apply the system with local data/scenarios, with more Contributor users adopting the system as it becomes well known and established.

Contribute and Guidelines
*************************

We are happy if you want to contribute. Please raise an issue explaining what is missing or if you find a bug. We will also gladly accept pull requests against our master branch for new features or bug fixes.

If you want to contribute please follow these steps:

    • fork the one of the Flood-PROOFS repositories to your account;
    • clone the repository, make sure you use "git clone --recursive" to also get the test data repository;
    • make a new feature branch from the repository master branch;
    • add your feature;
    • please include tests for your contributions in one of the test directories;
    • submit a pull request to our master branch.

Authors
*******

All authors involved in the library development for Flood-PROOFS modelling system are reported in this authors_ file.

License
*******

By accessing or using the Flood-PROOFS modelling system, code, data or documentation, you agree to be bound by the Flood-PROOFS license available. See the license_ for details. 

Changelog
*********

All notable changes and bugs fixing to this project will be documented in this changelog_ file.

References
**********
| [1_] c-hydro - Flood-PROOFS docker github repository 
| [2_] c-hydro - github repository
| [3_] c-hydro - Continuum github repository
| [4_] c-hydro - Flood-PROOFS venv tools github repository
| [5_] Python programming language
| [6_] Miniconda framework

.. _1: https://github.com/c-hydro/fp-docker
.. _2: https://github.com/c-hydro
.. _3: https://github.com/c-hydro/hmc
.. _4: https://github.com/c-hydro/fp-envs
.. _5: https://www.python.org/
.. _6: https://conda.io/miniconda.html

.. _license: LICENSE.rst
.. _changelog: CHANGELOG.rst
.. _authors: AUTHORS.rst
