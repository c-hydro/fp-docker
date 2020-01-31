#!/usr/bin/python3

"""
Flood-Proofs Docker Tool - Entrypoint App

__date__ = '20200131'
__version__ = '1.0.0'
__author__ = 'Fabio Delogu (fabio.delogu@cimafoundation.org'
__library__ = 'docker'

General command line:
python fp_docker_entrypoint_app_main.py -settings_file configuration.json
"""

# -------------------------------------------------------------------------------------
# Complete library
import logging
import os
import subprocess
import time
import datetime
import json
import pandas as pd

from copy import deepcopy
from argparse import ArgumentParser
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Algorithm information
alg_name = 'FP DOCKER TOOL - ENTRYPOINT APP'
alg_version = '1.0.0'
alg_release = '2020-01-31'
# Algorithm parameter(s)
time_format = '%Y-%m-%d %H:%M'
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Script Main
def main():

    # -------------------------------------------------------------------------------------
    # Get algorithm settings
    file_settings = get_args()

    # Get settings configuration file
    run_settings_default = read_file_json(file_settings)

    # Get environment variable(s)
    run_variable = get_variable(var_group_envs=run_settings_default['variable']['env_variable'],
                                var_group_local=run_settings_default['variable']['local_variable'],
                                run_path_root_default=os.path.dirname(os.path.realpath(__file__)))

    # Get file and folder(s)
    run_tags = run_settings_default['tags']
    run_folders = set_tags(run_settings_default['folder'], tags={'run_path_root': run_variable['run_path_root']})
    run_files = run_settings_default['file']
    run_apps = run_settings_default['app']
    run_cmd = run_settings_default['cmd']
    # Join file(s) and folder(s) using defined path(s)
    run_files = join_folder2file(run_folders, run_files)
    # Join app(s) and folder(s) using  defined path(s)
    run_apps = join_folder2file(run_folders, run_apps)
    # Make folder (is not exist)
    make_folder(list(run_folders.values()))

    # Set algorithm logging
    set_logging(logger_file=run_files['file_app_docker_log'])

    # Get parameters and data configuration file
    file_parameters = run_files['file_app_runner_configuration_parameters_default']
    file_data = run_files['file_app_runner_configuration_data_default']

    run_parameters_default = read_file_json(file_parameters)
    run_data_default = read_file_json(file_data)

    run_lookup_table = run_settings_default['lookup_table']
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Info algorithm
    logging.info(' ============================================================================ ')
    logging.info(' ==> ' + alg_name + ' (Version: ' + alg_version + ' Release_Date: ' + alg_release + ')')
    logging.info(' ==> START ... ')
    logging.info(' ')

    # Time algorithm information
    start_time = time.time()
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Fill parameters file with run information
    logging.info(' ===> Define parameters file ... ')
    run_parameters_def = merge_dict([run_variable, run_files, run_folders])
    run_parameters_upd = fill_structure(run_parameters_default, run_parameters_def,
                                        look_up_table=run_lookup_table['file_parameters'])
    logging.info(' ===> Define parameters file ... OK')

    # Fill datasets file with run information
    logging.info(' ===> Define datasets file ... ')
    run_data_def = merge_dict([run_variable, run_files, run_folders])
    run_data_upd = fill_structure(run_data_default, run_data_def,
                                  look_up_table=run_lookup_table['file_data'])
    logging.info(' ===> Define datasets file ... OK')
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Fill datasets file with run information
    logging.info(' ===> Define command-line process ... ')
    run_cmd_def = compose_cmd(run_cmd, run_apps, run_files, time=run_variable['run_time_now'])
    run_cmd_upd = join_cmd(run_cmd_def)
    logging.info(' ===> Define command-line process ... OK')
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Write parameters file in json format
    logging.info(' ===> Write parameters structure ... ')
    file_run_app_parameters = run_files['file_app_runner_configuration_parameters_custom']
    write_file_json(file_run_app_parameters, run_parameters_upd)
    logging.info(' ===> Write parameters structure ... OK')

    # Write datasets file in json format
    logging.info(' ===> Write datasets file ... ')
    file_run_app_data = run_files['file_app_runner_configuration_data_custom']
    write_file_json(file_run_app_data, run_data_upd)
    logging.info(' ===> Write datasets file ... OK')
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Run command-line list
    logging.info(' ===> Run command-line ... ')
    for run_cmd_id in run_cmd_upd:
        execute_cmd(run_cmd_id)
    logging.info(' ===> Run command-line ... OK')
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Info algorithm
    time_elapsed = round(time.time() - start_time, 1)

    logging.info(' ')
    logging.info(' ==> ' + alg_name + ' (Version: ' + alg_version + ' Release_Date: ' + alg_release + ')')
    logging.info(' ==> TIME ELAPSED: ' + str(time_elapsed) + ' seconds')
    logging.info(' ==> ... END')
    logging.info(' ==> Bye, Bye')
    logging.info(' ============================================================================ ')
    # -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to join cmd
def join_cmd(cmd_parts_list, cmd_sep=' '):
    cmd_join = []
    for cmd_parts_tmp in cmd_parts_list:
        cmd_join.append(cmd_sep.join(cmd_parts_tmp))
    return cmd_join
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to compose cmd
def compose_cmd(cmd, apps, files, time=None, interpreter="python"):

    cmd_line_all = []
    for cmd_tag, cmd_part in cmd.items():
        cmd_scripts = cmd_part['script']
        cmd_args = cmd_part['args']

        cmd_line_app = []
        for script, args in zip(cmd_scripts, cmd_args):
            if script in list(apps.keys()):
                app_def = apps[script]

                cmd_line_app = [interpreter, app_def]
                for arg_key, arg_value in args.items():

                    if arg_key != '-time':
                        if arg_value in list(files.keys()):
                            arg_tmp = files[arg_value]
                            arg_def = arg_key + ' ' + arg_tmp

                            cmd_line_app.extend([arg_def])
                    else:
                        if time is not None:
                            arg_time = time
                            arg_def = arg_key + ' ' + arg_time
                            cmd_line_app.extend([arg_def])

        cmd_line_all.append(cmd_line_app)

    return cmd_line_all
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to execute cmd
def execute_cmd(command_line):

    try:
        # Info start
        logging.info(' ====> Process execution: ' + command_line + ' ... ')
        # Execute command-line
        proc_handle = subprocess.Popen(command_line,
                                       shell=True,
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Read standard output
        while True:
            std_out = proc_handle.stdout.readline()
            if isinstance(std_out, bytes):
                std_out = std_out.decode('UTF-8')

            if std_out == '' and proc_handle.poll() is not None:
                if proc_handle.poll() == 0:
                    logging.warning(' ====> WARNING: process execution ' + str(proc_handle.poll()) + ' KILLED!')
                    break
                else:
                    logging.error(' ====> ERROR: process execution FAILED! ')
                    raise ValueError("Check your settings")
            if std_out:
                logging.info(str(std_out.strip()))

        # Collect stdout and stderr and exitcode
        std_out, std_error = proc_handle.communicate()
        std_exit = proc_handle.poll()

        if std_out == b'' or std_out == '':
            std_out = None
        if std_error == b'' or std_error == '':
            std_error = None

        # Info end
        logging.info(' ====> Process execution: ' + command_line + ' ... DONE')
        return std_out, std_error, std_exit

    except subprocess.CalledProcessError:
        # Exit code for process error
        logging.error(' ====> ERROR: process execution FAILED!')
        raise SystemExit("Errors in calling executable")

    except OSError as os_error:
        # Exit code for os error
        logging.error(' ====> ERROR: process execution FAILED!')
        raise OSError("Executable not found " + str(os_error))

# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to join folder and file
def join_folder2file(folders, files, folder_tag='folder', file_tag='file'):

    for folder_key, folder_value in folders.items():
        if folder_key.startswith(folder_tag):
            file_key = folder_key.replace(folder_tag, file_tag)
            if file_key in list(files.keys()):
                file_value = files[file_key]
                file_path = os.path.join(folder_value, file_value)
                files[file_key] = file_path

    return files
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to merge dict(s)
def merge_dict(dict_list, excluded_keys=['_comment']):
    dict_merge = {}
    for dict_wf in dict_list:
        for dict_key, dict_value in dict_wf.items():
            if dict_key not in excluded_keys:
                dict_merge[dict_key] = dict_value
    return dict_merge
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to fill structure with information
def fill_structure(structure, information, look_up_table=None, time_format='%Y%m%d%H%M'):
    for info_key, info_value in information.items():
        if info_key in list(look_up_table.keys()):
            struct_keys_list = look_up_table[info_key]

            if isinstance(info_value, str):

                try:
                    datetime.datetime.strptime(info_value, time_format)
                    date_check = True
                except ValueError:
                    date_check = False

                if (info_value.isnumeric()) and (date_check is False):
                    if info_value.isdigit():
                        info_value = int(info_value)
                    else:
                        info_value = float(info_value)

            structure = nested_set(structure, struct_keys_list, info_value, False)
    return structure
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
#  Method to set nested value in a dictionary
def nested_set(dic, keys, value, create_missing=True):
    d = dic
    for key in keys[:-1]:
        if key in d:
            d = d[key]
        elif create_missing:
            d = d.setdefault(key, {})
        else:
            return dic
    if keys[-1] in d or create_missing:
        d[keys[-1]] = value
    return dic
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to set name using tags
def set_tags(names, tags, excluded_keys=['_comment']):

    names_del = deepcopy(names)
    for name_key, name_value in names_del.items():
        if name_key in excluded_keys:
            names.pop(name_key, None)

    for name_key, name_value in names.items():
        for tag_key, tag_value in tags.items():
            if tag_key in name_value:
                name_value = name_value.replace(tag_key, ':')
                name_value = name_value.format(tag_value)
                name_value = name_value.replace("//", "/")
                names[name_key] = name_value
    return names
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to make folder
def make_folder(path_folder_list, sep_string='%'):

    if isinstance(path_folder_list, str):
        path_folder_list = [path_folder_list]

    for path_folder in path_folder_list:
        if sep_string in path_folder:
            path_folder_root, path_dyn = path_folder.split(sep_string, 1)
        else:
            path_folder_root = path_folder

        if not os.path.exists(path_folder_root):
            os.makedirs(path_folder_root)
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to write file json
def write_file_json(file_name, file_data, indent_print=4):
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, 'w') as file_handle:
        json.dump(file_data, file_handle, indent=indent_print)
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to read file json
def read_file_json(file_name):

    env_ws = {}
    for env_item, env_value in os.environ.items():
        env_ws[env_item] = env_value

    with open(file_name, "r") as file_handle:
        json_block = []
        for file_row in file_handle:

            for env_key, env_value in env_ws.items():
                env_tag = '$' + env_key
                if env_tag in file_row:
                    file_row = file_row.replace(env_tag, env_value)
                    file_row = file_row.replace('//', '/')

            # Add the line to our JSON block
            json_block.append(file_row)

            # Check whether we closed our JSON block
            if file_row.startswith('}'):
                # Do something with the JSON dictionary
                json_dict = json.loads(''.join(json_block))
                # Start a new block
                json_block = []

    return json_dict
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to get environment and local variable(s)
def get_variable(var_group_envs=None, var_group_local=None,
                 run_path_root_default=None, run_time_now_format='%Y%m%d%H%M'):

    global log_stream_init

    from io import StringIO
    log_stream_init = StringIO()
    logging.basicConfig(stream=log_stream_init, level=logging.INFO)

    var_def = {}
    if var_group_envs:
        for var_key, var_name in var_group_envs.items():
            if not var_key == 'run_path_root':
                if var_name in list(os.environ.keys()):
                    var_def[var_key] = os.environ[var_name]
                else:
                    logging.info(' WARNING: environment variable ' + var_name + ' needed but not found!')
    else:
        logging.info(' WARNING: environment variables return None')

    if var_group_local:
        for var_key, var_name in var_group_local.items():
            var_def[var_key] = var_name
    else:
        logging.warning(' WARNING: local variables return None')

    if 'run_path_root' not in list(var_group_local.keys()) or var_group_local['run_path_root'] is None:
        var_def['run_path_root'] = os.environ.get('HOME', run_path_root_default)
    else:
        var_def['run_path_root'] = var_group_local['run_path_root']

    if 'run_time_now' in list(var_def.keys()):
        run_time_now = var_def['run_time_now']
        run_timestamp_now = pd.Timestamp(run_time_now)
        run_timestr_now = run_timestamp_now.strftime(run_time_now_format)
        var_def['run_time_now'] = run_timestr_now
    else:
        logging.warning(' WARNING: variable run_time_now is not defined!')

    return var_def
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to get script argument(s)
def get_args():
    parser_handle = ArgumentParser()
    parser_handle.add_argument('-settings_file', action="store", dest="file_settings")
    parser_values = parser_handle.parse_args()

    if parser_values.file_settings:
        file_settings = parser_values.file_settings
    else:
        file_settings = 'configuration.json'

    return file_settings
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to set logging information
def set_logging(logger_file='log.txt', logger_format=None):

    if logger_format is None:
        logger_format = '%(asctime)s %(name)-12s %(levelname)-8s ' \
                        '%(filename)s:[%(lineno)-6s - %(funcName)20s()] %(message)s'

    # Remove old logging file
    if os.path.exists(logger_file):
        os.remove(logger_file)

    # Set level of root debugger
    logging.root.setLevel(logging.DEBUG)

    # Open logging basic configuration
    logging.basicConfig(level=logging.DEBUG, format=logger_format, filename=logger_file, filemode='w',
                        disable_existing_loggers=False)

    # Set logger handle
    logger_handle_1 = logging.FileHandler(logger_file, 'w')
    logger_handle_2 = logging.StreamHandler()
    # Set logger level
    logger_handle_1.setLevel(logging.DEBUG)
    logger_handle_2.setLevel(logging.DEBUG)
    # Set logger formatter
    logger_formatter = logging.Formatter(logger_format)
    logger_handle_1.setFormatter(logger_formatter)
    logger_handle_2.setFormatter(logger_formatter)

    # Add handle to logging
    logging.getLogger('').addHandler(logger_handle_1)
    logging.getLogger('').addHandler(logger_handle_2)

    # Redirect logging message(s) of the configuration part
    log_stream = log_stream_init.getvalue()
    log_list = log_stream.split('\n')
    for log_msg in log_list:
        logging.info(log_msg)

# -------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Call script from external library
if __name__ == "__main__":
    main()
# ----------------------------------------------------------------------------
