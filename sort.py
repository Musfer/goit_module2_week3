import pathlib
import os
import shutil
import sys


TRANS = {
        1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D',
        1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I',
        1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N',
        1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T',
        1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS', 1095: 'ch', 1063: 'CH',
        1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '',
        1101: 'e', 1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i', 1030: 'I',
        1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'
        }

file_names_dict = {
                    "images":[],
                    "documents":[],
                    "audio":[],
                    "video":[],
                    "archives":[],
                    "others":[],
                    }

def main():
    """
    the main function
    """
    dir_list, file_list = [], []
    
    if len(sys.argv) < 2:  # checking if an argument was passed
        user_path = ""
    else:
        user_path = sys.argv[1]

    path = check_path(user_path)

    dir_list, file_list = iter_files_on_dirs(path, dir_list, file_list)

    dir_list.pop(0)  # delete the root folder

    file_dict, known_extension_set, unknown_extension_set  = check_file_extension(file_list)

    create_folders(file_dict, path)

    file_names_dict = move_files(file_dict, path)

    unpacking_archive(file_dict, path)

    delate_folders(dir_list)

    return known_extension_set, unknown_extension_set, file_names_dict


def check_file_extension(file_list):
    """
    checks the file extension
    creates a dictionary with a set of files divided into groups
    returns a dictionary with absolute file addresses and a set with lists of known and unknown formats
    """
    file_dict = {
                    "images":[],
                    "documents":[],
                    "audio":[],
                    "video":[],
                    "archives":[],
                    "others":[],
                }

    extension_types = {
                    "images":['JPEG', 'PNG', 'JPG', 'SVG','BMP', "TIF", "TIFF"],
                    "documents":['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
                    "audio":['MP3', 'OGG', 'WAV', 'AMR'],
                    "video":['AVI', 'MP4', 'MOV', 'MKV'],
                    "archives":['ZIP', 'GZ', 'TAR'],
                    }

    unknown_extension_set = set()
    known_extension_set = set()
    
        
    for file_p in file_list:
        file_s = str(file_p)
        idx_extension = file_s.rfind(".")  # find the file extension
        extension = file_s[idx_extension+1:]
        known_extension_set.add(extension)

        if extension.upper() in extension_types["images"]:  # assigning files to the appropriate categories
            file_dict['images'].append(file_p)
        elif extension.upper() in extension_types["documents"]:
            file_dict["documents"].append(file_p)
        elif extension.upper() in extension_types["audio"]:
            file_dict["audio"].append(file_p)
        elif extension.upper() in extension_types["video"]:
            file_dict["video"].append(file_p)
        elif extension.upper() in extension_types["archives"]:
            file_dict["archives"].append(file_p)
        else:
            file_dict["others"].append(file_p)
            unknown_extension_set.add(extension)

        known_extension_set = known_extension_set - unknown_extension_set

    return file_dict, known_extension_set, unknown_extension_set
        

def check_path(user_path):
    """
    check the path to the file folder
    returns the path to the root folder
    """
    path = pathlib.Path(user_path)

    if path.exists():
        if path.is_dir():
            return path
        else:
            print(f"{path} is file")
    else:
        print(f"path {path.absolute()} not exists")


def create_folders(file_dict,path): 
    """
    creates folders to transfer found files according to formats
    """
    
    for category, files in file_dict.items():
        if not file_dict[category]:
            continue

        try:  # the block skips creating a folder if a folder with that name exists
            pathlib.Path(str(path) + "/" + category).mkdir()
        except FileExistsError:
            continue


def delate_folders(dir_list):
    """
    delate empty folders
    """
    for dir_path in dir_list:
        try:            
            pathlib.Path(dir_path).rmdir()
            dir_list.remove(dir_path)
        except OSError:
            continue
        
        if len(dir_list) == 0:
            break
        else:
            delate_folders(dir_list)


def iter_files_on_dirs(path, dir_list, file_list):
    """
    the function iterates files and folders through the parent folder
    returns a list of file addresses and a list of folder addresses
    """
    if path.is_dir():

        dir_list.append(path.absolute())
        for element in path.iterdir():
            iter_files_on_dirs(element, dir_list, file_list)
    else:
        file_list.append(path.absolute())
    
    return dir_list, file_list


def move_files(file_dict,path):
    """
    move files of different types to appropriate folders
    """
    for category, files_path in file_dict.items():
        
        if category == "archives":  # files in this category are processed through the function unpacking_archive
            continue

        for file_path in files_path:
            file_name_full = pathlib.Path(file_path).name
            idx_extension = file_name_full.rfind(".")
            file_name = file_name_full[:idx_extension]
            extension = file_name_full[idx_extension+1:]

            if category == "others":  # files in this category are processed without renaming (normalize)
                norm_file_name = file_name

                if norm_file_name in file_names_dict["others"]:  # checking whether such a file name already exists
                    norm_file_name = rename(norm_file_name, category, file_names_dict)
                    file_names_dict["others"].append(norm_file_name)
                else:
                    file_names_dict["others"].append(norm_file_name)

            else:
                norm_file_name = normalize(file_name)

                if norm_file_name in file_names_dict[category]:  # checking whether such a file name already exists
                    norm_file_name = rename(norm_file_name, category, file_names_dict)
                    file_names_dict[category].append(norm_file_name)
                else:
                    file_names_dict[category].append(norm_file_name)

            dst = pathlib.Path(str(path) + "/" + category + "/" + norm_file_name + "." + extension)

            shutil.move(file_path, dst)

    return file_names_dict


def normalize(file_name):
    """
    returns the normalized filename
    replaces other characters and spaces with an underscore
    replaces all Cyrillic characters with Latin characters
    """

    for char in file_name:
        if not char.isalnum() and char != "_":
            file_name = file_name.replace(char, '_')

    return file_name.translate(TRANS)


def rename(norm_file_name, category, file_names_dict):
    """
    rename file
    """
    while norm_file_name in file_names_dict[category]:
        norm_file_name = norm_file_name + "_"  
    
    else:
        return norm_file_name


def unpacking_archive(file_dict, path):
    """
    moves the archive to the appropriate folder and unpacks it
    """

    for category, files_path in file_dict.items():
        
        if category == "archives":
            for file_path in files_path:
                file_name_full = pathlib.Path(file_path).name
                idx_extension = file_name_full.rfind(".")
                file_name = file_name_full[:idx_extension]

                norm_file_name = normalize(file_name)

                if norm_file_name in file_names_dict["archives"]:  # checking whether such a file name already exists
                    norm_file_name = rename(norm_file_name, category, file_names_dict)
                    file_names_dict["archives"].append(norm_file_name)
                else:
                    file_names_dict["archives"].append(norm_file_name)

                extract_directory = pathlib.Path(str(path) + "/" + category+ "/" + norm_file_name)
                pathlib.Path(extract_directory).mkdir()

                shutil.unpack_archive(file_path, extract_directory)

                os.unlink(file_path)


if __name__ == "__main__":
    main()
