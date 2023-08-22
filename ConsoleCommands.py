import threading


class ConsoleCommands(threading.Thread):
    def __init__(self, folder_path, sync_interval, log_file_path, sync_object):
        super(ConsoleCommands, self).__init__()
        self.folder_path = folder_path
        self.sync_interval = sync_interval
        self.log_file_path = log_file_path
        self.sync_object = sync_object

    def print_folder_path(self):
        print(self.folder_path)

    def print_sync_interval(self):
        print(self.sync_interval)
        # print('\n')

    def print_log_file_path(self):
        print(self.log_file_path)

    def run(self):
        while True:
            command = str(input("Type: interval, logfpath, filepath for info or exit to exit the program \n"))

            if command == "interval":
                self.print_sync_interval()
            elif command == "logfpath":
                self.print_log_file_path()
            elif command == "filepath":
                self.print_folder_path()
            elif command == "exit":
                self.sync_object.set_running(False)
                break
            else:
                print("Unknown command!")



