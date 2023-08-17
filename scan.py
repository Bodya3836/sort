import sys
from pathlib import Path


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

registered_extensions = {
    "JPEG": jpeg_files,
    "PNG": png_files,
    "JPG": jpg_files,
    "SVG" : svg_files,
    "AVI" : avi_files,
    "MP4" : mp4_files,
    "MOV" : mov_files,
    "MKV" : mkv_files,
    "TXT": txt_files,
    "DOCX": docx_files,
    "ZIP": archives
}


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


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    scan(arg)

    print(f"jpeg: {jpeg_files}\n")
    print(f"jpg: {jpg_files}\n")
    print(f"png: {png_files}\n")
    print(f"svg: {svg_files}\n")
    print(f"avi: {svg_files}\n")
    print(f"mp4: {mp4_files}\n")
    print(f"mov: {mov_files}\n")
    print(f"mkv: {mkv_files}\n")
    print(f"mp3: {mp3_files}\n")
    print(f"ogg: {ogg_files}\n")
    print(f"wav: {wav_files}\n")
    print(f"amr: {amr_files}\n")
    print(f"txt: {txt_files}\n")
    print(f"docx: {docx_files}\n")
    print(f"archive: {archives}\n")
    print(f"unknown: {others}\n")
    print(f"All extensions: {extensions}\n")
    print(f"Unknown extensions: {unknown}\n")