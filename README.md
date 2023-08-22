# FilesSync
Syncing two files using python

The syncing is done periodically by the Sync class. We iterate through source path and it's content recursively and we sync the replica folder:
  -> for each folder we find, we create it if it doesn't exist in replica, then we delete the folders that are in replica but not in source.
  -> for each file in source, we try to find a file with a matching sha256(unique id for same content), and if we do find one then we try to match the names;
     if we don't find one, we simply create/copy that file. After this process is done we delete the files that are in replice but not in source.
  -> after each operation, we add it to an array that stores it along with the time it was performed. After the syncing is done, we write all the operations
     from the array into a log file.
  -> this process is done at a certain interval, it's value can be found in main script.
  -> during the execution of the program, we can write certain commands to obtain info, or to exit the program.
  Classes:
  -> Sync is dealing with the syncing of the files(delete, create, copy, renaming, etc.)
  -> Log is dealing with the operations log file
  -> utils module has function for getting the sha256 of a file and a random name for renaming the files
  -> ConsoleCommands is a thread that runs concurrently with the main thread and waits for user input, then displays info based on what the use asked. When the user
     types 'exit' the thread sends a signal to the Sync object that it should stop syncing and the stops its execution.
  -> main pieces togheter all the other components. It's the script that should be run from terminal for the program to start syncing.

