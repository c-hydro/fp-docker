=========
Changelog
=========

Version 1.0.5 [2021-01-08]
**************************
FIX: 
    - update of fp environments for the python packages;
    - build of hyde package with a new version of the conda environment and with a new settings of the conda repositories (pkgs, conda-forge, pip);
    - build of hmc package with a new version of the conda environment and with a new settings of the conda repositories (pkgs, conda-forge, pip);

Version 1.0.4 [2020-09-20]
**************************
APP: **fp_docker_entrypoint_app_main_hyde.py**
	- Added the customization for using application over different domains by using {run_domain} tag
	- Added the options to dynamically change the names of input and output of all applications
APP: **fp_docker_entrypoint_app_main_hmc.py**
	- Added the customization for using application over different domains by using {run_domain} tag
	- Added the options to dynamically change the names of input and output of all applications

Version 1.0.3 [2020-06-30]
**************************
APP: **fp_docker_entrypoint_app_main_hyde.py**
	- WS Downloader and GROUND NETWORK WS application(s)

Version 1.0.2 [2020-04-20]
**************************
APP: **fp_docker_entrypoint_app_main_hyde.py**
	- Docker configuration tool for Hydrological Data Engines python3 package
	- NWP WRF and DataSplitting application(s)

FIX:
	- Update of Debian/Ubuntu system from 19.04 to 18.04 version

Version 1.0.1 [2020-03-18]
**************************
FIX:
	- Update of Debian/Ubuntu system from 18.10 to 19.04 version
	- Update of miniconda python environment version [4.6.14] to avoid issue in installing Python3.6 interpreter

Version 1.0.0 [2020-02-04]
**************************
APP: **fp_docker_entrypoint_app_main_hmc.py**
	- Docker configuration tool for Hydrological Model Continuum python3 package

GENERIC RELEASE:
	- Beta release for LEXIS project
  	- Development of docker file to generate containers
  	- Development of docker utilities to build and run containers
  	- Development of docker utilities to configure entrypoints	
