from datetime import datetime


class Log:
    def __init__(self, file):
        self.file = file
        self.operations = []

    def ad_operation(self, operation):
        self.operations.append(operation + "\n")

    # after all the file operations are done, we just append them to the log file and repeat the process
    def write_info(self):
        try:
            with open(self.file, 'a') as f:
                for op in self.operations:
                    f.write(op)
        except EnvironmentError:
            print("Something went wrong when trying to log file operations")
        finally:
            self.operations.clear()

    @staticmethod
    def get_time():
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S ")
