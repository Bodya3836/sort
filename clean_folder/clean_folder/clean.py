import re
import shutil
import sys
from pathlib import Path

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")


TRANS = {}

jpeg_files = list()
png_files = list()
jpg_files = list()
svg_files = list()
txt_files = list()
docx_files = list()
avi_files = list()
mp4_files = list()
mov_files = list()
mkv_files = list()
mp3_files = list()
ogg_files = list()
wav_files = list()
amr_files = list()
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()

registered_extensions = {"JPEG": jpeg_files, "PNG": png_files, "JPG": jpg_files, "SVG" : svg_files,
                         "AVI" : avi_files, "MP4" : mp4_files, "MOV" : mov_files, "MKV" : mkv_files,
                         "TXT": txt_files, "DOCX": docx_files, "ZIP": archives}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def normalize(name):
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ("JPEG", "JPG", "PNG", "SVG", "AVI", "MP4", "MOV", "MKV", "MP3", "OGG", "WAV", "AMR", "TXT", "DOCX", "OTHER", "ARCHIVE"):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)

def hande_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize(path.name))


def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize(path.name.replace(".zip", ''))

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

def main():
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