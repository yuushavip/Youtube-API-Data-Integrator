import configparser
import yaml
import os

def get_api_config():
    config = configparser.ConfigParser()
    file_name = 'youtube_api.ini'
    file_path = f"config/{file_name}"
    
    if os.environ.get('CONFIG_DIR_PATH'):
        file_path = f"{os.environ['CONFIG_DIR_PATH']}{file_name}"
        
    config.read(file_path)
    
    return config

def get_task_config(main_key):
    file_name = 'youtube_task.yaml'
    file_path = f"config/{file_name}"
    
    if os.environ.get('CONFIG_DIR_PATH'):
        file_path = f"{os.environ['CONFIG_DIR_PATH']}{file_name}"
    
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    
    task_config = config.get(main_key, {})
    
    return task_config

def get_data_api_config():
    config = get_api_config()
    data_api_config = config['DATA_API']
    
    return data_api_config

def get_analytics_api_config():
    config = get_api_config()
    data_api_config = config['ANALYTICS_API']
    
    return data_api_config

def get_task_channel_ids(task_main_key):
    config = get_task_config('task_list')
    channel_ids = config.get(task_main_key, [])
    
    return channel_ids

def get_columns(task_main_key):
    job_config = get_task_config(task_main_key)
    columns = job_config.get('columns', {})
    
    return columns

def get_params(task_main_key):
    job_config = get_task_config(task_main_key)
    params = job_config.get('params', {})
    
    return params