import os

list_of_dir = []
list_of_files = []

def get_file_dir(path):
    for dir in os.listdir(path):
        cur_path = os.path.join(path,dir)

        if(os.path.isdir(cur_path)):
            list_of_dir.append(cur_path)
            get_file_dir(cur_path)
        
        else:
            list_of_files.append(cur_path)
            print(cur_path)

