import os
from ConsoleCommands import ConsoleCommands
from Sync import Sync

source_path = 'Files/source'
replica_path = 'Files/replica'
log_file = 'OperationsLog.txt'
interval_time = 5

sync = Sync(source_path, replica_path, log_file, interval_time)
console_reader = ConsoleCommands(os.path.join(".", "Files"), interval_time, os.path.join(".", "OperationsLog.txt"), sync)
console_reader.start()
sync.sync()