import shutil
import sys
import scan
import normalize
from pathlib import Path
from files_generator import file_generator



def hande_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.normalize(path.name))


def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize.normalize(path.name.replace(".zip", ''))

    archive_folder = root_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(path.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def get_folder_objects(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass

def main(folder_path):
    if len(sys.argv) != 2:
        print("Usage: file_sorted <folder_path>")
        return
    
    folder_path = sys.argv[1]
    sort_folder = sys.argv[1]
    Known_extensions = sys.argv[1]
    Unknown_extensions = sys.argv[1]

    known_extensions, unknow_extensios = sort_folder(folder_path)

    print("Known extensions",Known_extensions)
    print("Unknown extensions",Unknown_extensions)
    print("Folders names",folder_path)

if __name__ == '__main__':
    main()
