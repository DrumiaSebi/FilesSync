import os
import shutil
import time
from Log import Log
import utils


class Sync:
    def __init__(self, source_path, replica_path, log_file, interval):
        self.source_path = source_path
        self.replica_path = replica_path
        self.log = Log(log_file)
        self.interval = interval
        self.running = True

    # will be set to False when we enter 'exit', by the ConsoleCommands Thread, so the execution of syncing will stop
    def set_running(self, bool_value):
        self.running = bool_value

    def create_dirs(self, dirs_in_source, rep_path):
        for dir_name in dirs_in_source:
            if not os.path.exists(os.path.join(rep_path, dir_name)):
                os.mkdir(rep_path + "/" + dir_name)
                op = self.log.get_time() + "-> Created folder " + dir_name
                print(op)
                self.log.ad_operation(op)

    def delete_dirs(self, dirs_in_source, rep_path):
        dirs_in_replica = [f.name for f in os.scandir(rep_path) if f.is_dir()]
        for dir_name in dirs_in_replica:
            if dir_name not in dirs_in_source:
                shutil.rmtree(os.path.join(rep_path, dir_name))
                op = self.log.get_time() + "-> Deleted folder " + dir_name
                print(op)
                self.log.ad_operation(op)

    def delete_files(self, files_to_del, rep_path):
        for file in files_to_del:
            try:
                os.remove(os.path.join(rep_path, file))
                op = self.log.get_time() + "-> Removed file " + file
                print(op)
                self.log.ad_operation(op)
            except FileNotFoundError:
                print("Trying to delete a file which name you've changed")

    def sync_files(self, files_in_source, rep_path, source_dir_path):
        # storing files that exists both in replica and source, and we visited
        visited = []

        # dictionaries for storing hash values, so we don't calculate them for every comparison
        hash_from_source = dict()
        hash_from_replica = dict()
        for file in files_in_source:
            hash_from_source[file] = utils.hashfile(os.path.join(source_dir_path, file))
        files_in_replica = [f.name for f in os.scandir(rep_path) if f.is_file()]
        for file in files_in_replica:
            hash_from_replica[file] = utils.hashfile(os.path.join(rep_path, file))

        for file_s in files_in_source:
            found_current_file = False
            for file_r in files_in_replica:
                try:
                    if file_r not in visited:
                        if hash_from_source[file_s] == hash_from_replica[file_r]:
                            # if they have the same hash but different names, we only rename the file in replica
                            if file_r != file_s:
                                if os.path.isfile(os.path.join(rep_path, file_s)):
                                    # there may be already a file with that name, so we assign a random name to it
                                    new_name = utils.get_random_name()
                                    hash_from_replica[new_name] = hash_from_replica[file_s]
                                    files_in_replica.append(new_name)
                                    os.rename(os.path.join(rep_path, file_s),
                                              os.path.join(rep_path, new_name))
                                os.rename(os.path.join(rep_path, file_r), os.path.join(rep_path, file_s))
                            visited.append(file_s)
                            found_current_file = True
                            break
                except FileNotFoundError:
                    print("Trying to access a file which name you've changed")

            if not found_current_file:
                # didn't find a file, so we copy it
                shutil.copy(os.path.join(source_dir_path, file_s), rep_path)
                op = self.log.get_time() + "-> Created file " + file_s
                print(op)
                self.log.ad_operation(op)
                visited.append(file_s)

        self.delete_files([f for f in files_in_replica if f not in visited], rep_path)

    def sync(self):
        while self.running:
            for root, dirs, files in os.walk(os.path.join(".", self.source_path)):
                replica_dir_path = root.replace(self.source_path, self.replica_path)
                self.create_dirs(dirs, replica_dir_path)
                self.delete_dirs(dirs, replica_dir_path)
                self.sync_files(files, replica_dir_path, root)
                self.log.write_info()
            time.sleep(self.interval)
