#!/usr/bin/python3

"""
Flood-Proofs Docker Tool - Entrypoint App

__date__ = '20200422'
__version__ = '1.5.0'
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
import numpy as np

from copy import deepcopy
from argparse import ArgumentParser
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Algorithm information
alg_name = 'FP DOCKER TOOL - ENTRYPOINT APP'
alg_version = '1.6.0'
alg_release = '2020-06-29'
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
    # Get app name list
    app_list = run_settings_default['apps_name']
    # Organize app(s) env
    app_obj, log_obj = organize_apps(app_list, run_settings_default)

    # Set algorithm logging
    make_folder([log_obj['folder_docker_log']])
    set_logging(logger_file=os.path.join(log_obj['folder_docker_log'], log_obj['file_docker_log']))
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
    # Iterate over application(s)
    for app_name in app_list:

        # -------------------------------------------------------------------------------------
        # Starting information
        logging.info(' ===> Application Name: ' + app_name + ' ... ')

        # Get application frame
        app_frame = app_obj[app_name]

        # Get environment variable(s)
        run_variable = get_variable(var_group_envs=app_frame['variable']['env_variable'],
                                    var_group_local=app_frame['variable']['local_variable'],
                                    run_path_root_default=os.path.dirname(os.path.realpath(__file__)))
        # Get lookup table
        run_lookup_table = app_frame['lookup_table']

        # Get file and folder(s)
        run_tags = app_frame['tags']
        run_folders = set_tags(app_frame['folder'], tags={'run_path_root': run_variable['run_path_root']})
        run_files = app_frame['file']
        run_apps = app_frame['app']
        run_cmd = app_frame['cmd']
        # Join file(s) and folder(s) using defined path(s)
        run_files = join_folder2file(run_folders, run_files)
        # Join app(s) and folder(s) using  defined path(s)
        run_apps = join_folder2file(run_folders, run_apps)
        # Make folder (is not exist)
        make_folder(list(run_folders.values()))

        # Get configuration file
        file_configuration = run_files['file_app_configuration_default']
        run_configuration_default = read_file_json(file_configuration)
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Fill parameters file with run information
        logging.info(' ====> Define parameters file ... ')
        run_configuration_def = merge_dict([run_variable, run_files, run_folders])
        run_configuration_upd = fill_structure(run_configuration_default, run_configuration_def,
                                               look_up_table=run_lookup_table)
        logging.info(' ====> Define parameters file ... OK')
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Fill datasets file with run information
        logging.info(' ====> Define command-line process ... ')
        run_cmd_def = compose_cmd(run_cmd, run_apps, run_files, time=run_variable['run_time_now'])
        run_cmd_upd = join_cmd(run_cmd_def)
        logging.info(' ====> Define command-line process ... OK')
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Write configuration file in json format
        logging.info(' ====> Write configuration structure ... ')
        file_run_app_configuration = run_files['file_app_configuration_custom']
        write_file_json(file_run_app_configuration, run_configuration_upd)
        logging.info(' ====> Write configuration structure ... OK')
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Run command-line list
        logging.info(' ====> Set process execution ... ')
        execute_cmd(run_cmd_upd)
        logging.info(' ====> Set process execution ... OK')
        # -------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------
        # Ending information
        logging.info(' ===> Application Name: ' + app_name + ' ... DONE')
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
    cmd_join = cmd_sep.join(cmd_parts_list)
    return cmd_join
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to compose cmd
def compose_cmd(cmd, apps, files, time=None, interpreter="python"):

    cmd_scripts = cmd['script']
    cmd_args = cmd['args']

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

    return cmd_line_app
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to execute cmd
def execute_cmd(command_line):

    try:
        # Info start
        logging.info(' ====> Process execution [' + command_line + '] ... ')

        # Check command-line calling
        subprocess.check_call(command_line, shell=True)
        # Execute command-line calling
        return_code = subprocess.call(command_line, shell=True)

        if return_code != 0:
            logging.warning(' ====> Process execution [' + command_line + '] ... RETURN ERROR(S)!')
            logging.warning(' ====> Return Code: ' + str(return_code))
        else:
            logging.info(' ====> Process execution [' + command_line + '] ... OK')

    except subprocess.CalledProcessError as err:
        logging.error(' ====> Process execution [' + command_line + '] ... FAILED!')
        logging.error(' ====> Process error(s): ' + str(err))
        raise subprocess.CalledProcessError("Process execution FAILED!")
    except OSError as err:
        logging.error(' ====> Process execution [' + command_line + '] ... FAILED!')
        logging.error(' ====> Process error(s): ' + str(err))
        raise OSError("Process execution FAILED!")

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
        if info_value is not None:
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

                if struct_keys_list is not None:
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
        if name_value is not None:
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
        if path_folder is not None:
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
                    env_value = env_value.strip("'\\'")
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
# Safe dict for unfilled keys
class SafeDict(dict):
    def __missing__(self, key):
        key = '{' + key + '}'
        return key


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
                    var_value_raw = os.environ[var_name]
                    var_value_def = var_value_raw.strip("'\\'")
                    var_def[var_key] = var_value_def
                else:
                    logging.info(' WARNING: environment variable ' + var_name + ' needed but not found!')
    else:
        logging.info(' WARNING: environment variables return None')

    if 'run_domain' not in list(var_def.keys()):
        logging.warning(' WARNING: environment variables of domain name in not defined.')
        run_domain_envs = False
    else:
        run_domain_envs = True

    # Add different definition of run_domain, $DOMAIN ...
    if 'run_domain' in list(var_def.keys()):
        var_def['$DOMAIN'] = var_def['run_domain']

    if var_group_local:
        for var_key, var_name in var_group_local.items():

            if run_domain_envs and not var_key == 'run_domain':

                if isinstance(var_name, str):
                    if 'run_domain' in var_name:
                        var_tmp = var_name.format_map(SafeDict(run_domain=var_def['run_domain']))
                        var_name_def = var_tmp
                    else:
                        var_name_def = var_name
                else:
                    var_name_def = var_name
                var_def[var_key] = var_name_def

            elif not run_domain_envs:
                var_def[var_key] = var_name_def

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
# Method to organize app(s) configuration
def organize_apps(app_list, app_configuration, tag_path_root='run_path_root'):

    if isinstance(app_list, str):
        app_list = [app_list]

    log_obj = None
    app_obj = {}
    for app_name in app_list:
        app_frame = {}
        for config_key, config_data in app_configuration.items():
            if config_key == 'log':
                log_obj = config_data

            if isinstance(config_data, dict):
                if app_name in list(config_data.keys()):
                    app_field = config_data[app_name]
                    app_frame[config_key] = app_field
        app_obj[app_name] = app_frame

    app_path_list = []
    for app_name, app_data in app_obj.items():
        for app_key, app_field in app_data.items():
            app_path_step = get_dict_value(app_field, tag_path_root, [])
            if not isinstance(app_path_step, list):
                app_path_step = [app_path_step]
            if app_path_step.__len__() > 0:
                app_path_step = app_path_step[0]
                if os.path.isdir(app_path_step):
                    app_path_list.append(app_path_step)

    if app_path_list.__len__() > 0:
        app_path_root = list(set(app_path_list))
        if app_path_root.__len__() > 1:
            app_path_root = app_path_root[0]
        app_path_root = app_path_root[0]
    else:
        app_path_root = os.environ.get('HOME')

    log_obj_filled = {}
    for log_key, log_value in log_obj.items():
        if log_key != '_comment':
            log_filled = log_value.format(run_path_root=app_path_root)
            log_obj_filled[log_key] = log_filled

    return app_obj, log_obj_filled
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to get nested value
def get_dict_value(d, key, value=[]):

    for k, v in iter(d.items()):
        if isinstance(v, dict):
            if k == key:
                for kk, vv in iter(v.items()):
                    temp = [kk, vv]
                    value.append(temp)
            else:
                vf = get_dict_value(v, key, value)
                if isinstance(vf, list):
                    if vf:
                        vf_end = vf[0]
                    else:
                        vf_end = None
                elif isinstance(vf, np.ndarray):
                    vf_end = vf.tolist()
                else:
                    vf_end = vf
                if vf_end not in value:
                    if vf_end:
                        if isinstance(value, list):
                            value.append(vf_end)
                        elif isinstance(value, str):
                            value = [value, vf_end]
                    else:
                        pass
                else:
                    pass
        else:
            if k == key:
                if isinstance(v, np.ndarray):
                    value = v
                else:
                    value = v
    return value
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
    logging.basicConfig(level=logging.DEBUG, format=logger_format, filename=logger_file, filemode='w')

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

# -------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Call script from external library
if __name__ == "__main__":
    main()
# ----------------------------------------------------------------------------
