"""
Library Features:

Name:          lib_utils_entrypoint_variable
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20221019'
Version:       '2.0.0'
"""
# -------------------------------------------------------------------------------------
# Library
import logging
import os

from copy import deepcopy

import pandas as pd

from lib_info_args import logger_name

# Logging
log_stream = logging.getLogger(logger_name)
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Safe dict for unfilled keys
class SafeDict(dict):
    def __missing__(self, key):
        key = '{' + key + '}'
        return key
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to organize entrypoint variables (env and local)
def organize_entrypoint_variable(
        obj_entrypoint_settings,
        tag_variable_template='application_variable_template',
        tag_variable_group_env='application_variable_env', tag_variable_group_local='application_variable_local',
        tag_run_domain='run_domain', tag_run_path_root='run_path_root', tag_run_time_now='run_time_now',
        run_path_root_default=None):

    template_workspace = None
    if tag_variable_template in list(obj_entrypoint_settings.keys()):
        template_workspace = obj_entrypoint_settings[tag_variable_template]

    var_workspace_env, var_workspace_local = None, None
    if tag_variable_group_env in list(obj_entrypoint_settings.keys()):
        var_workspace_env = obj_entrypoint_settings[tag_variable_group_env]
    if tag_variable_group_local in list(obj_entrypoint_settings.keys()):
        var_workspace_local = obj_entrypoint_settings[tag_variable_group_local]

    if var_workspace_env and var_workspace_local:
        var_workspace_check = {**var_workspace_env, **var_workspace_local}
    elif var_workspace_env is None and var_workspace_local:
        var_workspace_check = deepcopy(var_workspace_local)
    elif var_workspace_env and var_workspace_local is None:
        var_workspace_check = deepcopy(var_workspace_env)
    elif var_workspace_env is None and var_workspace_local is None:
        var_workspace_check = None
    else:
        log_stream.error(' ===> Variable checking is not correctly ended')
        raise NotImplementedError('Case not implemented yet')

    var_boolean_check = True
    if var_workspace_check:
        for template_key, template_value in template_workspace.items():
            if template_key not in list(var_workspace_check.keys()):
                var_boolean_check = False
                logging.warning(' ===> Template "' + template_key +
                                '" must have a definition in the variable workspace')
        if not var_boolean_check:
            log_stream.error(' ===> Some template(s) and variable(s) is/are not correctly defined and linked.')
            raise RuntimeError('Each template must be defined by the env or local variable(s)')
    else:
        log_stream.warning(' ===> All variable(s) are defined by NoneType')

    obj_entrypoint_variable = {}
    if var_workspace_env is not None:
        for var_name, var_field_env in var_workspace_env.items():

            if var_name in list(template_workspace.keys()):
                var_type = template_workspace[var_name]

                if var_field_env in list(os.environ.keys()):

                    var_value_raw = os.environ[var_field_env]
                    var_value_def = check_var_type(var_value_raw, var_type)
                    obj_entrypoint_variable[var_name] = var_value_def

                else:
                    log_stream.warning(' ===> Environment variable "' + var_field_env +
                                       '" needed but not found! The related key "' + var_name +
                                       '" is defined by NoneType')
                    obj_entrypoint_variable[var_name] = None

    else:
        log_stream.warning(' ===> All environment variables are defined by NoneType')

    run_domain_envs = True
    if tag_run_domain not in list(obj_entrypoint_variable.keys()):
        logging.warning(' ===> Variable "' + tag_run_domain + '" is not defined')
        run_domain_envs = False

    if var_workspace_local is not None:
        for var_name, var_field_local in var_workspace_local.items():

            if var_name in list(template_workspace.keys()):

                var_type = template_workspace[var_name]

                var_field_app = None
                if var_name not in list(obj_entrypoint_variable.keys()):
                    obj_entrypoint_variable[var_name] = None
                else:
                    var_field_app = obj_entrypoint_variable[var_name]

                if var_field_app is None:

                    if run_domain_envs and not var_name == tag_run_domain:
                        if isinstance(var_name, str):
                            if tag_run_domain in var_name:
                                var_tmp = var_name.format_map(SafeDict(
                                    run_domain=obj_entrypoint_variable[tag_run_domain]))
                                var_value_def = var_tmp
                            else:
                                var_value_def = check_var_type(var_field_local, var_type)
                        else:
                            var_value_def = check_var_type(var_field_local, var_type)
                        obj_entrypoint_variable[var_name] = var_value_def

                    elif not run_domain_envs:
                        var_value_def = check_var_type(var_field_local, var_type)
                        obj_entrypoint_variable[var_name] = var_value_def

    # Add different definition of run_domain, $DOMAIN ...
    if tag_run_domain in list(obj_entrypoint_variable.keys()):
        obj_entrypoint_variable['$DOMAIN'] = obj_entrypoint_variable[tag_run_domain]

    if tag_run_path_root not in list(var_workspace_local.keys()) or var_workspace_local[tag_run_path_root] is None:
        if os.environ.get('HOME') is not None:
            obj_entrypoint_variable[tag_run_path_root] = os.environ.get('HOME')
        else:
            obj_entrypoint_variable[tag_run_path_root] = os.environ.get('HOME', run_path_root_default)
            log_stream.warning(' ===> Variable "HOME" is not defined! Use a default value "' +
                            str(run_path_root_default) + '"')
    else:
        obj_entrypoint_variable[tag_run_path_root] = var_workspace_local[tag_run_path_root]

    if tag_run_time_now not in list(obj_entrypoint_variable.keys()):
        log_stream.warning(' ===> Variable "' + tag_run_time_now + '" is not defined!')

    return obj_entrypoint_variable
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to check variable type
def check_var_type(var_value_raw, var_type='string_name'):

    if check_time_format(var_type):
        var_value_tmp = pd.Timestamp(var_value_raw)
        var_value_def = var_value_tmp.strftime(var_type)
    elif var_type == 'string_name':
        var_value_def = var_value_raw.strip("'\\'")
    elif var_type == 'string_path':
        var_value_def = os.path.normpath(deepcopy(var_value_raw))
    elif var_type == 'boolean':
        var_value_def = deepcopy(var_value_raw)
    elif var_type == 'integer':
        var_value_def = str(int(var_value_raw))
    elif var_type == 'float':
        var_value_def = str(float(var_value_raw))
    else:
        log_stream.error(' ===> Variable type "' + var_type + '" is not defined!')
        raise NotImplementedError('Case not implemented yet')

    return var_value_def
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to check if string is a time format
def check_time_format(value):
    check_value = False
    if isinstance(value, str):
        if value.startswith('%'):
            check_value = True
    return check_value
# -------------------------------------------------------------------------------------

