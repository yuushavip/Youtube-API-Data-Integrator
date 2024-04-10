import csv
import os

def get_data_path(file_name):
    if os.environ.get('DATA_DIR_PATH'):
        data_path = f"{os.environ['DATA_DIR_PATH']}{file_name}"
        
        return data_path
    
    return f"data/{file_name}"

def write_to_csv(data_items, file_name, mode, keys=None):
    file_path = get_data_path(file_name)
    
    if not data_items:
        return
    
    if not keys:
        keys = data_items[0].keys()
    
    with open(file_path, mode, newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        
        if os.path.getsize(file_path) == 0:
            writer.writeheader()
        
        writer.writerows(data_items)
        
def fetch_and_write(func, file_name):
    data_items = func()
    
    if data_items:
        write_to_csv(data_items, file_name, 'w')