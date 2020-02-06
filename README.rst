.. _license_label: LICENSE.rst

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

In computing, virtualization refers to the act of creating a virtual (rather than actual) version of something, including 
virtual computer hardware platforms, storage devices, and computer network resources. Virtualization began in the 1960s, 
as a method of logically dividing the system resources provided by mainframe computers between different applications. 
Since then, the meaning of the term has broadened.

The virtualization of Flood-PROOFS modelling system, is performed by using the **Docker** framework. In fact, Docker is an 
open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your 
infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you 
manage your applications. 

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

5. Verify that you now have the key with the fingerprint 9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88, 
	 by searching for the last 8 characters of the fingerprint:

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

.. code-block:: bash

	>> sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
	>> sudo chmod g+rwx "$HOME/.docker" -R		

Docker components
*****************

The github repository contains different folders for storing all Docker components in order to allow the virtualization of
the Flood-PROOFS modelling system. The structure of the repository is reported below:

::
	
	**fp-docker**
	├── **docker_configuration**
	│   ├── fp-docker_builder.sh
	│   ├── fp-docker_file
	│   ├── fp-docker_runner.sh
	│   └── fp-docker_variables.env
	├── **docker_entrypoint**
	│   ├── fp_docker_entrypoint_app_configuration.json
	│   ├── fp-docker_entrypoint_app_interface.sh
	│   └── fp_docker_entrypoint_app_main.py
	├── AUTHORS.rst
	├── CHANGELOG.rst
	├── LICENSE.rst
	└── README.rst

Particularly:
    • **docker_configuration**: tools to build and run the Flood-PROOFS dockers;
    • **docker_entrypoint**: tools to configure the entrypoints of the Flood-PROOFS dockers.

All codes and datasets are freely available and users can be get them from our github repository [1_].

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

The docker **build** command builds Docker images from a Dockerfile and a “context”. A build’s context is the set of files 
located in the specified PATH or URL. The build process can refer to any of the files in the context. For example, your build 
can use a COPY instruction to reference a file in the context.

In order to build the dockers, in the **docker_configuration** scripts, Dockerfiles and environment variable files are provided.
The generic command-line to invoke the building of the Docker file is the following:

.. code-block:: bash

	>> ./fp-docker_builder.sh -f fp-docker_variables.env

where the -f flag is used to pass the Environment variable file to the building script.

Environment variable file
-------------------------

The Docker environment variable file (.env) is crucial when you're creating complex container deployments. As you might 
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
	SOURCE_DATA_STATIC='$HOME/docker-ws/data/static_data/'
	SOURCE_DATA_RESTART='$HOME/docker-ws/restart/'
	SOURCE_DATA_DYNAMIC_OBS='$HOME/docker-ws/data/dynamic_data/observation/'
	SOURCE_DATA_DYNAMIC_FOR='$HOME/docker-ws/data/dynamic_data/nwp/'
	SOURCE_DATA_ARCHIVE='$HOME/docker-ws/results/'
	TARGET_DATA_STATIC='/home/fp/fp_mount/data/static/'
	TARGET_DATA_RESTART='/home/fp/fp_mount/data/restart/'
	TARGET_DATA_DYNAMIC_OBS='/home/fp/fp_mount/data/forcing/obs/'
	TARGET_DATA_DYNAMIC_FOR='/home/fp/fp_mount/data/forcing/for/'
	TARGET_DATA_ARCHIVE='/home/fp/fp_mount/archive/'
	RUN_TIME_NOW=2019-05-12 11:00					
	RUN_TIME_STEPS_OBS=4
	RUN_TIME_STEPS_FOR=0
	RUN_NAME='fp_run'
	RUN_ENS=false

All the information are used in building and running parts. To achive a correct settings of Flood-PROOFS Dockers
all the fields must be filled. The SOURCE folders are referred to the host machine, whilst the TARGET folders are
intended the folders of the containers

Dockerfile
----------

Docker can build images automatically by reading the instructions from a Dockerfile. A Dockerfile is a text document that 
contains all the commands a user could call on the command line to assemble an image. Using docker build users can create an 
automated build that executes several command-line instructions in succession.


here

Run dockers
***********

The docker **run** command first creates a writeable container layer over the specified image, and then starts it using the 
specified command. That is, docker run is equivalent to the API /containers/create then /containers/(id)/start. A stopped 
container can be restarted with all its previous changes intact using docker start.
When an operator executes docker run, the container process that runs is isolated in that it has its own file system, its own 
networking, and its own isolated process tree separate from the host.

.. code-block:: bash

	>> ./fp-docker_runner.sh -f fp-docker_variables.env 

.. code-block:: bash

	>> ./fp-docker_runner.sh -i -f fp-docker_variables.env 

where the -f flag is used to pass the Environment variable file to the building script.

LEXIS
*****

LEXIS workflow using Docker ...

Potential Users
***************

The Flood-PROOFS Modelling System and the Docker virtualization have been released to enable different applications (for example local/regional scenario assessment) 
and further development by external users.

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

All authors involved in the docker development for FloodPROOFS system are reported in this authors_ file.

License
*******

By accessing or using the FloodPROOFS modelling system, code, data or documentation, you agree to be bound by the FloodPROOFS license available. See the license_ for details. 

Changelog
*********

All notable changes and bugs fixing to this project will be documented in this changelog_ file.

References
**********
| [1_] CIMA Hydrology and Hydraulics GitHub Repository
| [2_] Python programming language
| [3_] Fortran programming language
| [4_] QGIS project
| [5_] R programming language
| [6_] FloodPROOFS virtual environment tools
| [7_] Conda environment manager
| [8_] ZLIB compression library
| [9_] HDF5 data software library 
| [10_] NetCDF4 data software library 
| [11_] Hydrological Model Continuum codes

.. _1: https://github.com/c-hydro
.. _2: https://www.python.org/
.. _3: https://en.wikipedia.org/wiki/Fortran
.. _4: https://qgis.org/en/site/
.. _5: https://www.r-project.org/
.. _6: https://github.com/c-hydro/fp-env
.. _7: https://conda.io/miniconda.html
.. _8: https://zlib.net/
.. _9: https://www.hdfgroup.org/solutions/hdf5/
.. _10: https://www.unidata.ucar.edu/
.. _11: https://github.com/c-hydro/hmc-dev
.. _license: LICENSE.rst
.. _changelog: CHANGELOG.rst
.. _authors: AUTHORS.rst
