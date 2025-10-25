import os
import shutil
import hashlib
from rich.progress import Progress
from datetime import datetime
import argparse
from collections import defaultdict
import json

BUFF_SIZE = 65536
PROGRESSBAR_COLOR = "cyan"
FILE_CATEGORIES = {}

# Loading file categories
try:
    with open("./file_categories.json", "r") as file_categories:
        FILE_CATEGORIES = json.loads(file_categories.read())
except FileNotFoundError:
    print("file_categories.json not found")
    exit(1)
except Exception as e:
    print("Some unknown error occurred")
    print(e)
    exit(1)


# Used to create folder at path
def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

# Used to move file safely to the destination


def move_file(src, dest_folder):
    base, ext = os.path.splitext(os.path.basename(src))
    dest = os.path.join(dest_folder, os.path.basename(src))

    counter = 1
    renamed = False
    previous_filename = dest
    while os.path.exists(dest):
        renamed = True
        dest = os.path.join(dest_folder, f"{base}_{counter}{ext}")
        counter += 1

    if renamed == True:
        print(
            f"⚠️ File already exists at destination: {previous_filename}, renamed to {dest}")

    shutil.move(src, dest)

# Separate unique copy of file


def separate_unique(folder_path):
    seen_hashes = set()
    unique_folder = create_folder(os.path.join(folder_path, "Unique Files"))
    unique_files = 0
    duplicate_files = 0

    all_files = os.listdir(folder_path)
    with Progress() as progress:
        task = progress.add_task(
            f"[{PROGRESSBAR_COLOR}]Separating unique files...", total=len(all_files))

        for file in all_files:
            file_path = os.path.join(folder_path, file)

            if not os.path.isfile(file_path):
                progress.update(task, advance=1)
                continue

            try:
                # Creating file hash and checking if it is in hash table
                hasher = hashlib.sha256()
                with open(file_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(BUFF_SIZE), b""):
                        hasher.update(chunk)
                file_hash = hasher.hexdigest()

                if file_hash not in seen_hashes:
                    seen_hashes.add(file_hash)
                    unique_files += 1
                    move_file(file_path, unique_folder)
                else:
                    duplicate_files += 1
            except FileNotFoundError:
                progress.console.print(f"🚫 File not found: {file}")
            except Exception as e:
                progress.console.print(f"🚫 Error processing {file}: {e}")

            progress.update(task, advance=1)

    print(f"✅ All unique files moved to {unique_folder}")
    print(f"Unique Files: {unique_files}")

    return {"Unique Files": unique_files, "Duplicate Files (Files Not Moved)": duplicate_files}

# Organize files based on their extension


def organize_files(folder_path):
    organized_files = defaultdict(list)
    all_files = os.listdir(folder_path)
    fileswext_count = {}

    for file in all_files:
        # Collecting file types
        full_path = os.path.join(folder_path, file)
        if not os.path.isfile(full_path):
            continue
        ext = file.rsplit(".", 1)[-1].lower() if "." in file else "other"
        organized_files[ext if ext in FILE_CATEGORIES else "other"].append(
            file)

    with Progress() as progress:
        task = progress.add_task(f"[{PROGRESSBAR_COLOR}]Organizing files by extension...", total=sum(
            len(v) for v in organized_files.values()))

        for ext, files in organized_files.items():
            folder_name = FILE_CATEGORIES.get(ext, "Other")
            target_folder = create_folder(
                os.path.join(folder_path, folder_name))

            for file in files:
                src = os.path.join(folder_path, file)

                try:
                    if folder_name not in fileswext_count.keys():
                        fileswext_count[folder_name] = 0

                    move_file(src, target_folder)
                    fileswext_count[folder_name] += 1
                except FileNotFoundError:
                    progress.console.print(f"🚫 File not found: {file}")
                except Exception as e:
                    progress.console.print(f"🚫 Error moving {file}: {e}")
                progress.update(task, advance=1)

    print("✅ All files are successfully organized by their extension")
    print(f"Different File Types Found: {len(organized_files)}")

    result = {}
    for key, value in fileswext_count.items():
        print(f"{key}: {value} Files")
        result[key] = value

    return result

# Organize file based on their creation time


def organize_by_creation(folder_path):
    all_files = os.listdir(folder_path)
    different_groups = 0
    files_in_year_count = {}
    files_moved = 0
    files_not_moved = 0

    with Progress() as progress:
        task = progress.add_task(
            f"[{PROGRESSBAR_COLOR}]Organizing files by creation year...", total=len(all_files))

        for file in all_files:
            file_path = os.path.join(folder_path, file)
            if not os.path.isfile(file_path):
                progress.update(task, advance=1)
                continue

            creation_year = datetime.fromtimestamp(
                os.stat(file_path).st_birthtime).year
            year_folder = os.path.join(folder_path, str(
                creation_year))

            if creation_year not in files_in_year_count.keys():
                files_in_year_count[creation_year] = 0
            files_in_year_count[creation_year] += 1
            if not os.path.isdir(year_folder):
                different_groups += 1
                create_folder(year_folder)

            try:
                move_file(file_path, year_folder)
                files_moved += 1
            except FileNotFoundError:
                progress.console.print(f"🚫 File not found:{file}")
            except Exception as e:
                files_not_moved += 1
                progress.console.print(f"🚫 Error moving {file}: {e}")

            progress.update(task, advance=1)

    print("✅ All files are successfully organized by creation year")
    print(f"Total Years Folder: {different_groups}")
    print(f"Files Moved: {files_moved}")
    print(f"Files Not Moved: {files_not_moved}")

    return {"Total Years Folder": different_groups, "Files Moved": files_moved, "Files Not Moved": files_not_moved, "Files In Year": files_in_year_count}

# Move files from sub folders into parent folder


def flatten_folder(folder_path, remove_folders=False):
    parent_folder = folder_path
    all_files = []
    files_not_moved = 0
    files_moved = 0

    for root, dirs, files in os.walk(parent_folder, topdown=False):
        if root != parent_folder:
            # Collecting all files with path
            for file in files:
                all_files.append((root, file))

    with Progress() as progress:
        task = progress.add_task(
            f"[{PROGRESSBAR_COLOR}]Extracting files from sub folders...", total=len(all_files))

        for file in all_files:
            src_path = os.path.join(file[0], file[1])
            dest_path = parent_folder

            try:
                move_file(src_path, dest_path)
                files_moved += 1
            except FileNotFoundError:
                progress.console.print(f"🚫 File not found: {src_path}")
            except Exception as e:
                progress.console.print(f"Some unknown error occurred: {e}")
                files_not_moved += 1
            progress.update(task, advance=1)

    print("✅ Folder successfully flatted")

    # Removing empty sub folders
    if remove_folders:
        folders = []

        for root, dirs, file in os.walk(folder_path, topdown=False):
            for folder in dirs:
                os.rmdir(os.path.join(root, folder))

        for file in os.listdir(folder_path):
            if os.path.isdir(os.path.join(folder_path, file)):
                folders.append(file)

        with Progress() as progress:
            remove_folders_task = progress.add_task(
                f"[{PROGRESSBAR_COLOR}]Deleting empty folders...", total=len(folders))

            for folder in folders:
                path = os.path.join(folder_path, folder)

                try:
                    # os.rmdir(path)
                    pass
                except FileNotFoundError:
                    progress.console.print(f"🚫 Folder not found: {folder}")
                except Exception as e:
                    progress.console.print(f"Some unknown error occurred: {e}")

                progress.update(remove_folders_task, advance=1)
        print("✅ Folders successfully deleted")

    return {"Files Moved": files_moved, "Files Not Moved": files_not_moved}


def main():
    parser = argparse.ArgumentParser(description="File Organizer CLI Tool")
    parser.add_argument(
        "folder", help="Path of folder to organize (quote if it has spaces)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--unique", action="store_true",
                       help="Move only unique files")
    group.add_argument("-e", "--extension", action="store_true",
                       help="Organize files by extension")
    group.add_argument("-c", "--creation", action="store_true",
                       help="Organize files by creation year")
    group.add_argument("-f", "--flatten", action="store_true",
                       help="Flatten all folders")
    parser.add_argument("-r", "--remove_folder", action="store_true",
                        help="Remove empty folders after flattening")

    args = parser.parse_args()

    folder_path = args.folder
    if not os.path.isdir(folder_path):
        print(f"🚫 Error: '{folder_path}' is not a valid folder.")
        return

    if args.unique:
        separate_unique(folder_path)
    elif args.extension:
        organize_files(folder_path)
    elif args.creation:
        organize_by_creation(folder_path)
    elif args.flatten:
        flatten_folder(folder_path, args.remove_folder)


if __name__ == "__main__":
    main()
