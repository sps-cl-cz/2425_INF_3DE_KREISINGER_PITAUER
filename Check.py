import argparse
import hashlib
import os
import datetime

# Funkce pro získání hash souboru
def HashSha1(Path):
    sha1_hash = hashlib.sha1()
    with open(Path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha1_hash.update(byte_block)
    return sha1_hash.hexdigest()

# Funkce pro nastavení argumentů init, add, remove, status
def SetupArguments():
    parser = argparse.ArgumentParser()
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    subparsers.add_parser("init", help="Creates a new file containing the list of tracked files.")
    
    add_parser = subparsers.add_parser("add", help="Adds specified files to tracking.")
    add_parser.add_argument("files", nargs="+", help="Files to add to tracking.")
    
    remove_parser = subparsers.add_parser("remove", help="Removes specified files from tracking.")
    remove_parser.add_argument("files", nargs="+", help="Files to remove from tracking.")
    
    subparsers.add_parser("status", help="Displays the status of all tracked files.")
    
    return parser

# Funkce pro kontrolu existence souboru
def FileExist(fileName):
    if not os.path.exists(fileName):
        print(f"Tracking file '{fileName}' does not exist. Run 'init' to create it first.")
        return False
    return True

# Funkce pro načtení sledovaných souborů
def LoadTrackedFiles(fileName):
    tracked_files = {}
    if os.path.exists(fileName):
        with open(fileName, "r") as file:
            for line in file:
                tracked_file, hash_value = line.strip().split(",", 1)
                tracked_files[tracked_file] = hash_value
    return tracked_files

# Funkce pro přidání souborů ze sledování
def AddFilesToTracking(fileName, tracked_files, args):
    with open(fileName, "a") as file:
        for file_path in args.files:
            if os.path.exists(file_path):
                rel_path = os.path.relpath(file_path, os.getcwd())
                file_hash = HashSha1(file_path)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if rel_path in tracked_files:
                    print(f"File '{rel_path}' is already tracked.")
                else:
                    file.write(f"{rel_path},{file_hash},{timestamp}\n")
                    print(f"File '{rel_path}' added to tracking.")
            else:
                print(f"File '{file_path}' does not exist. Skipping.")

# Funkce pro odstranění souborů ze sledování
def RemoveFilesFromTracking(fileName, tracked_files, args):
    files_to_remove = args.files
    removed_any = False

    for file_path in files_to_remove:
        rel_path = os.path.relpath(file_path, os.getcwd())
        if rel_path in tracked_files:
            del tracked_files[rel_path]
            print(f"File '{rel_path}' removed from tracking.")
            removed_any = True
        else:
            print(f"File '{rel_path}' is not currently tracked.")

    if removed_any:
        with open(fileName, "w") as file:
            for tracked_file, hash_value in tracked_files.items():
                file.write(f"{tracked_file},{hash_value}\n")
    else:
        print("No files were removed.")

# Funkce pro kontrolu statusu
def CheckStatus(fileName):
    if not os.path.exists(fileName):
        print(f"Tracking file '{fileName}' does not exist. Run 'init' to create it first.")
        return

    tracked_files = {}
    with open(fileName, "r") as file:
        for line in file:
            tracked_file, hash_value, timestamp = line.strip().split(",", 2)
            tracked_files[tracked_file] = {"hash": hash_value, "timestamp": timestamp}

    summary = {'OK': 0, 'CHANGE': 0, 'ERROR': 0}

    for file_path, info in tracked_files.items():
        if os.path.exists(file_path):
            current_hash = HashSha1(file_path)

            if current_hash == info["hash"]:
                print(f"[OK] {info['hash']} {file_path}")
                summary['OK'] += 1
            else:
                print(f"[CHANGE] {info['hash']} {file_path} (Last modified: and NEW HASH: {current_hash}")
                summary['CHANGE'] += 1
        else:
            print(f"[ERROR] File not found: {file_path}")
            summary['ERROR'] += 1

    print(f"Summary: {summary['OK']} OK, {summary['CHANGE']} CHANGE, {summary['ERROR']} ERROR")

# Funkce pro zpracování argumentů
def HandleArguments(args, filename):
    if args.command == "init":
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Existing file '{filename}' has been removed.")
        with open(filename, "w") as file:
            pass
        print(f"New file '{filename}' has been successfully created.")
    elif args.command == "add":
        if not FileExist(filename):
            return
        tracked_files = LoadTrackedFiles(filename)
        AddFilesToTracking(filename, tracked_files, args)
    elif args.command == "remove":
        if not FileExist(filename):
            return
        tracked_files = LoadTrackedFiles(filename)
        RemoveFilesFromTracking(filename, tracked_files, args)
    elif args.command == "status":
        if not FileExist(filename):
            return
        CheckStatus(filename)
    else:
        print("Use the -h option for help.")

# Funkce pro spuštění programu
def Main():
    if __name__ == "__main__":
        parser = SetupArguments()
        args = parser.parse_args()
        HandleArguments(args, ".check")

Main()