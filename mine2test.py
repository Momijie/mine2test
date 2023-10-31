import json
import zipfile
import shutil
import os

tmp = "./tmp"
out = "./out"


def delete_directory(directory_path):
    shutil.rmtree(directory_path)


def get_json(file_location):
    with open(file_location, 'r') as f:
        parsed_json = json.load(f)
    return parsed_json


def unzip_file(file_location):
    with zipfile.ZipFile(file_location, 'r') as zip_ref:
        zip_ref.extractall(tmp)


def if_directory_exists(source_path, root):
    source_path_ready = source_path.strip('/')
    check_directory = os.path.join(root, source_path_ready)
    if os.path.exists(check_directory):
        return check_directory
    return None


def prepare():
    if os.path.exists(out):
        delete_directory(out)
    if os.path.exists(tmp):
        delete_directory(tmp)


prepare()

json_data = get_json("data.json")

# For now, just testing with this since it's what I want to convert
unzip_file("faithful.zip")


success = 0
fail = 0
for obj in json_data:

    skip = False
    default_target = False

    source_path = None
    source_file = None
    target_path = None
    target_file = None

    if "source_path" in obj:
        source_path = obj["source_path"]
    if "source_file" in obj:
        source_file = obj["source_file"]

    if "target_path" in obj:
        target_path = obj["target_path"]

    if "target_file" in obj:
        target_file = obj["target_file"]

    if source_path == None:
        print("We need a source path.")
        skip = True

    if source_file == None:
        print("We need a source file, skipping!")
        skip = True

    if target_path == None:
        print("We need a target path, using default", out, " .")
        default_target = True
        skip = True

    if target_file == None:
        print("We need a target file.")
        skip = True

    if not skip:
        checked_source_directory = if_directory_exists(source_path, tmp)
        if not checked_source_directory == None:
            source_texture = os.path.join(
                checked_source_directory, source_file)

            if os.path.exists(source_texture):
                target_directory = os.path.join(
                    out, target_path.strip('/'))
                if not os.path.exists(target_directory):

                    os.makedirs(target_directory)
                    target_texture = os.path.join(
                        target_directory, target_file)
                    shutil.copy(source_texture, target_texture)
                    # print(source_texture, "->", target_texture)
                else:
                    target_texture = os.path.join(
                        target_directory, target_file)
                    shutil.copy(source_texture, target_texture)

        #     # delete_directory(out)

print("fail:", fail, ","+"success", success)
