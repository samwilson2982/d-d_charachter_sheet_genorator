import datetime
import os


class DirHelper(object):
    @staticmethod
    def create_datedir():
        date_dir = os.getcwd() + "\\" + datetime.datetime.now().strftime("%m-%d-%Y") + "\\"
        try:
            os.mkdir(date_dir)
        except Exception as e:
            print("directory already exists")
        print(date_dir)
        os.chdir(date_dir)
        return date_dir

    @staticmethod
    def local_path(relative_path):
        return os.path.join(os.path.dirname(__file__), relative_path)