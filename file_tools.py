from tinydb import TinyDB, Query
import os
import uuid
import config
import zipfile

databases_db_path = os.path.abspath("./databases")
catalogues_db_path = os.path.abspath("./databases/catalogues.json")
volume_path = config.path_to_volume

def get_parent_path(relative_path):
    path = os.path.normpath(relative_path)
    split_path = path.split(os.sep)
    del split_path[-1]
    if len(split_path) == 0:
        return None
    else:
        return os.path.join(*split_path)
    

def split_path(relative_path):
    path = os.path.normpath(relative_path)
    split_path = path.split(os.sep)
    result = []
    for i in range(len(split_path)):
        entry = ""
        for j in range(i+1):
            entry = os.path.join(entry, split_path[j])
        result.append([ split_path[i] ,entry])
    return result

def get_catalogues_db():
    return TinyDB(catalogues_db_path)

def translate_relative_path(relative_path:str):
    path_arr = relative_path.split('/')
    return os.path.join(*path_arr)

def get_complete_path(catalogue,relative_path=None):
    cat_path = get_catalogue_path(catalogue)
    if relative_path is None:
        return cat_path
    relative_path = translate_relative_path(relative_path)
    return os.path.join(cat_path, relative_path)

def get_size_str(fsize:int):
    GB = 1000000000
    MB = 1000000
    KB = 1000
    if fsize // GB>0:
        return str(fsize // GB) + " GB"
    if fsize // MB>0:
        return str(fsize // MB) + " MB"
    if fsize // KB>0:
        return str(fsize // KB) + " KB"
    return str(fsize) + " B"

def get_file_info(file):
    ftype = file.content_type.value
    sys_file = file.file.raw
    sys_file.seek(0, os.SEEK_END)
    fsize = sys_file.tell()
    size_display = get_size_str(fsize)
    return { "size" : fsize, "file_type" : ftype, "size_display" : size_display }

def get_catalogue_name(id):
    catalogue= Query()
    catalogues = TinyDB(catalogues_db_path)
    result = catalogues.get(catalogue.id == id)['name']
    catalogues.close()
    return result

def get_file(filename,catalogue,relative_path=None):
    path = get_complete_path(catalogue,relative_path)
    index = get_index(path)
    ##TO-DO: check if directory exists
    file = Query()
    result = index.get((file.type == 'file') & (file.name == filename))
    index.close()
    return result

def get_download_file_path(filename, catalogue, relative_path = None):
    file_data = get_file(filename, catalogue, relative_path)
    return file_data['path']

def get_multiple_files_zip(filenames, catalogue, relative_path = None):
    paths = [ get_download_file_path(x,catalogue,relative_path) for x in filenames ]
    tmp_name =  catalogue + ".zip"
    ZipFile = zipfile.ZipFile(tmp_name, "w" )
    for path in paths:
        ZipFile.write(path, os.path.basename(path), compress_type=zipfile.ZIP_DEFLATED)
    ZipFile.close()
    return os.path.abspath(tmp_name)


def insert_file(file, catalogue, relative_path=None):
    path = get_complete_path(catalogue,relative_path)
    file_path = os.path.join(path, file.filename)
    _ , extension = os.path.splitext(file_path)
    extension = extension.replace('.', '')
    with open(file_path, 'wb') as out:
        while True:
            data = file.file.read(8192)
            if not data:
                break
            out.write(data)
    index = get_index(path)
    file_info = get_file_info(file)
    file_entry = { 'type' : 'file', 'name' : file.filename, 'path' : file_path, 'extension' : extension, **file_info}
    index.insert(file_entry)
    index.close()

def remove_file(filename,catalogue,relative_path=None):
    path = get_complete_path(catalogue, relative_path)
    file_path = os.path.join(path, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        return "Plik {0} nie istenieje!".format(filename)
    
    index = get_index(path)
    file = Query()
    index.remove((file.name == filename) & (file.type == 'file') )
    index.close()


def get_all_files(catalogue, relative_path=None, sort_field = None, sort_reverse=False):
    path = get_complete_path(catalogue,relative_path)
    index = TinyDB(os.path.join(path,"index.json"))
    file = Query()
    files = index.search(file.type == 'file')
    print(files, sort_reverse)
    if sort_field is not None:
        files.sort(reverse=sort_reverse, key= lambda x: x[sort_field])
    index.close()
    return files


def get_all_directories(catalogue, relative_path=None):
    path = get_complete_path(catalogue,relative_path)
    index = TinyDB(os.path.join(path,"index.json"))
    file = Query()
    dirs = index.search(file.type == 'directory')
    index.close()
    return dirs


def create_index(catalogue, relative_path=None):
    path = get_complete_path(catalogue,relative_path)
    index = TinyDB(os.path.join(path,"index.json"))
    index.close()


def get_index(complete_path):
    return TinyDB(os.path.join(complete_path,"index.json"))


def create_catalogue(id, name = None):
    path_to_catalogue = os.path.join(volume_path, id)
    if name is None: name = id
    catalogue = { 'id' : id, 'name' : name, 'path' : path_to_catalogue}
    
    if not os.path.exists(path_to_catalogue):
        os.makedirs(path_to_catalogue, mode=0o777, exist_ok=False)
    catalogues = get_catalogues_db()        
    catalogues.insert(catalogue)
    catalogues.close()
    #create_index(name)


def get_catalogue(id):
    catalogue = Query()
    catalogues = get_catalogues_db()
    result = catalogues.get(catalogue.id == id)
    catalogues.close()
    return result

def get_catalogue_path(id):
    return get_catalogue(id)['path']


def create_directory(name,catalogue, relative_path = None):
    directory_path = get_complete_path(catalogue,relative_path)
    created_directory_path = os.path.join(directory_path,name)
    if relative_path is not None:
        relative_path = os.path.join(relative_path, name)
    else:
        relative_path = name
    if not os.path.exists(created_directory_path):
        os.makedirs(created_directory_path, mode=0o777, exist_ok=False)
        create_index(catalogue, relative_path)

    index = get_index(directory_path)
    directory = { 'type': 'directory', 'name': name, 'relative_path' : relative_path, 'path': created_directory_path }
    index.insert(directory)
    index.close()

def remove_directory(directory_name, catalogue="common", relative_path=None):
    path = get_complete_path(catalogue,relative_path)
    deleted_directory_path = os.path.join(path,directory_name)
    if not os.path.isdir(deleted_directory_path):
        return 'Folder ' + directory_name + ' nie istnieje.'
    if len(os.listdir(deleted_directory_path))>1:
        return 'Można usuwać tylko puste foldery.'
    os.remove(os.path.join(deleted_directory_path, 'index.json'))
    os.rmdir(deleted_directory_path)
    directory = Query()
    index = get_index(path)
    index.remove((directory.type=='directory') & (directory.name==directory_name))
    index.close()
