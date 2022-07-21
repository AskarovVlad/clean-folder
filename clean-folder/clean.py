import re
import shutil
import sys
from pathlib import Path

RU_EN_DICT = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
              'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
              'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'u', 'ь': '', 'э': 'e',
              'ю': 'yu', 'я': 'ya', 'ё': 'yo', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ж': 'Zh',
              'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
              'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'C', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': '',
              'Ы': 'U', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya', 'І': 'I', 'Ї': 'I', 'Є': 'E', 'є': 'e', 'і': 'i',
              'ї': 'i', 'Ґ': 'G', 'ґ': 'g', 'Ё': 'Yo'}

DIR_EXT = {('.jpeg', '.jpg', '.png', '.svg'): "image",
           ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'): "document",
           ('.mp3', '.ogg', '.wav', '.amr'): "audio",
           ('.avi', '.mp4', '.mov', '.mkv'): "video",
           ('.zip', '.gz', '.tar'): "archive",
           }

DEFAULT_DIR_NAMES = ('image', 'video', 'audio', 'document', 'archive', 'others')


def get_cmd_args():

    if len(sys.argv) != 2:
        print("Path must have only 1 argument")
    else:
        return sys.argv[1]


def check_extension(extension):

    for ext in DIR_EXT:
        if extension in ext:
            return DIR_EXT[ext]
    return 'others'


def split_file_name(file_name):

    return file_name.stem, file_name.suffix


def normalize(name):

    table = name.maketrans(RU_EN_DICT)
    name = name.translate(table)
    symbols = re.compile(r"[^\w_]")
    return symbols.sub('_', name)


def rename_files(files):

    for category in files:

        for file in category:
            filename = normalize(split_file_name(file)[0]) + split_file_name(file)[1]
            file.rename(file.parent / filename)
            files[files.index(category)][category.index(file)] = file.parent / filename

    return files


def sort_files(path, files):

    for file in path:

        if file.is_file():
            folder = check_extension(split_file_name(file)[1].lower())
            files[DEFAULT_DIR_NAMES.index(folder)].append(file)
        elif file.name not in DEFAULT_DIR_NAMES:
            inside_dirs = sort_files(file.iterdir(), files)
            files = inside_dirs

    return files


def check_is_dir(path):
    if path.exists():
        return path

    return False


def make_folders(path):
    sort_folders = []

    for name in DEFAULT_DIR_NAMES:
        if not check_is_dir(path / name):
            (path / name).mkdir()
        sort_folders.append(check_is_dir(path / name))

    return sort_folders


def unpack_archives(archive, new_dir_path):
    shutil.unpack_archive(archive, new_dir_path)


def move_files(files, dirs):

    for file_type in files:

        for file_path in file_type:
            file_path.replace(dirs[files.index(file_type)] / file_path.name)
            files[files.index(file_type)][files[files.index(file_type)].index(file_path)] = \
                dirs[files.index(file_type)] / file_path.name

    for archive in files[4]:
        path_to_archive_dir = dirs[4] / split_file_name(archive)[0]
        archive_path = path_to_archive_dir / archive.name
        path_to_archive_dir.mkdir()
        archive.replace(archive_path)
        files[4][files[4].index(archive)] = path_to_archive_dir
        unpack_archives(archive_path, path_to_archive_dir)
        archive_path.unlink()

        for file in path_to_archive_dir.iterdir():
            filename = normalize(split_file_name(file)[0].encode('IBM437').decode('IBM866')) + split_file_name(file)[1]
            file.rename(file.parent / filename)

    return files


def remove_empty_dirs(path):

    for content in path:
        if content.is_file():
            continue
        if content.is_dir() and len(list(content.iterdir())) > 0:
            remove_empty_dirs(content.iterdir())
        if content.is_dir() and len(list(content.iterdir())) == 0:
            content.rmdir()


def main():
    path = Path(r'C:\Users\DESKTOP-65L32PF\Desktop\Test')
    # path = Path(get_cmd_args())
    if path.is_dir():
        all_files = rename_files(sort_files(path.iterdir(), [[], [], [], [], [], []]))
        new_files = move_files(all_files, make_folders(path))
        remove_empty_dirs(path.iterdir())
        print(new_files)
    else:
        print('It is not a directory , please insert a valid directory path')


if __name__ == '__main__':
    main()
