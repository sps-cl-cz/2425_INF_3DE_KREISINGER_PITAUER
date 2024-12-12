import argparse
import hashlib
import glob
import os
import datetime

#function to hash a file
def HashSha1(Path):
    sha1_hash = hashlib.sha1()
    with open(Path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha1_hash.update(byte_block)
    return sha1_hash.hexdigest()

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

def FileExist(fileName):
    if not os.path.exists(fileName):
        print(f"Tracking file '{fileName}' does not exist. Run 'init' to create it first.")
        return False
    
def LoadTrackedFiles(fileName):
    tracked_files = {}
    if os.path.exists(fileName):
        with open(fileName, "r") as file:
            for line in file:
                tracked_file, hash_value = line.strip().split(",", 1)
                tracked_files[tracked_file] = hash_value
    return tracked_files

def AddFilesToTracking(fileName, file_path,tracked_files):
    with open(fileName, "a") as file:
            for file_path in args.files:
                if os.path.exists(file_path):
                    file_hash = HashSha1(file_path)
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if file_path in tracked_files:
                        print(f"File '{file_path}' is already tracked.")
                    else:
                        file.write(f"{file_path},{file_hash},{timestamp}\n")
                        print(f"File '{file_path}' added to tracking.")
                else:
                    print(f"File '{file_path}' does not exist. Skipping.")

def RemoveFilesFromTracking(fileName, file_path, tracked_files):
        files_to_remove = args.files
        removed_any = False

        for file_path in files_to_remove:
            if file_path in tracked_files:
                del tracked_files[file_path]
                print(f"File '{file_path}' removed from tracking.")
                removed_any = True
            else:
                print(f"File '{file_path}' is not currently tracked.")

        # Přepsání sledovacího souboru, pokud byl některý soubor odstraněn
        if removed_any:
            with open(fileName, "w") as file:
                for tracked_file, hash_value in tracked_files.items():
                    file.write(f"{tracked_file},{hash_value}\n")
        else:
            print("No files were removed.")

    #kontrola statusu vytvořených hashů
def CheckStatus(fileName):
    if not os.path.exists(fileName):
        print(f"Tracking file '{fileName}' does not exist. Run 'init' to create it first.")
        return

    tracked_files = LoadTrackedFiles(fileName)
    summary = {'OK': 0, 'CHANGE': 0, 'ERROR': 0}

    for file_path, info in tracked_files.items():
        if os.path.exists(file_path):
            current_hash = HashSha1(file_path)
            if current_hash == info:
                print(f"[OK] {info} {file_path}")
                summary['OK'] += 1
            else:
                print(f"[CHANGE] {info} {file_path} and NEW HASH: {current_hash}")
                summary['CHANGE'] += 1
        else:
            print(f"[ERROR] File not found: {file_path}")
            summary['ERROR'] += 1

    print(f"Summary: {summary['OK']} OK, {summary['CHANGE']} CHANGE, {summary['ERROR']} ERROR")


def HandleArguments(args):
    fileName = ".check"
    if args.command == "init":
        if os.path.exists(fileName):
            os.remove(fileName)
            print(f"Existing file '{fileName}' has been removed.")
        with open(fileName, "w") as file:
            pass
        print(f"New file '{fileName}' has been successfully created.")
    elif args.command == "add":
        if FileExist(fileName) == False:
            return
        tracked_files = LoadTrackedFiles(fileName)
        AddFilesToTracking(fileName, args.files, tracked_files)
        
    elif args.command == "remove":
        if FileExist(fileName) == False:
            return
        tracked_files = LoadTrackedFiles(fileName)
        RemoveFilesFromTracking(fileName, args.files, tracked_files)
    elif args.command == "status":
        if FileExist(fileName) == False:
            return
        CheckStatus(fileName)
    else:
        print("Use the -h option for help.")

if __name__ == "__main__":
    parser = SetupArguments()
    args = parser.parse_args()
    HandleArguments(args)
