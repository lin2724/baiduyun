import os
import time
import sys


def check_folder(folder_path):
    pre_time = 0
    pre_files = []
    while True:
        stat = os.stat(folder_path)
        if stat.st_mtime != pre_time:
            pre_time = stat.st_mtime
            pre_files = os.listdir(folder_path)
            print(stat.st_mtime)
        else:
            if len(pre_files) != len(os.listdir(folder_path)):
                print('%d files on coping...' % (len(os.listdir(folder_path)) - len(pre_files)) )
        time.sleep(0.3)


def check_file(file_path):
    pre_time = 0
    pre_files = []
    while True:
        if os.path.exists(file_path):
            break
        time.sleep(0.5)
    while True:
        stat = os.stat(file_path)
        if stat.st_mtime != pre_time:
            pre_time = stat.st_mtime
            print(stat.st_mtime)
            print('cur_time %s '% time.time())
        time.sleep(0.3)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        #check_folder(sys.argv[1])
        check_file(sys.argv[1])

