import ConfigParser
import time
import os
import sys
import byyun
import multiprocessing

def sync_folder(filetups=None, files=None, lfolder=None,rfolder=None, ondelete=False):
    fail_count = 0
    if files:
        for file in files:
            print(file, rfolder)
            ret = byyun.upload_file(file, rfolder)
            if ret:
                fail_count += 1
            else:
                if ondelete:
                    os.remove(file)
    if filetups:
        for tup in filetups:
            file = tup['file']
            rfolder = tup['folder']
            print('file:%s  rfolder:%s' % (file, rfolder))
            ret = byyun.upload_file(filepath=file, rfolder=rfolder)
            if ret:
                fail_count += 1
            else:
                if ondelete:
                    os.remove(file)
    return fail_count


def parse_config():
    configfile = 'sync.config'
    config = ConfigParser.ConfigParser()
    tmp = config.read(configfile)
    if not tmp:
        print('config file not exit,we create by default')
        with open(configfile, 'w+') as fd:
            lfolder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'localbaidu')
            fd.write('[setting]\n')
            fd.write('lfolder=%s\n' % lfolder)
            fd.write('rfolder=/\n')
            fd.write('max_threads=10\n')
        return lfolder, '/', 10
    else:
        lfolder = config.get('setting', 'lfolder')
        rfolder = config.get('setting', 'rfolder')
        max_threads = config.get('setting', 'max_threads')
        return lfolder, rfolder, max_threads


def get_file_list(lfolder, max=None):
    if not os.path.exists(lfolder):
        print('wrong folder %s' % lfolder)
        return 1
    pre_stat = os.stat(lfolder)
    file_list = []
    for dir, subdirs, files in os.walk(lfolder):
        for file in files:
            if max and len(file_list) >= max:
                time.sleep(1)
                stat = os.stat(lfolder)
                if stat.st_mtime != pre_stat.st_mtime:
                    print('folder content is changing')
                    return []
                return file_list
            file_list.append(os.path.join(dir, file))
    time.sleep(1)
    stat = os.stat(lfolder)
    if stat.st_mtime != pre_stat.st_mtime:
        print('folder content is changing')
        return []

    return file_list


def move_upload_to(files, lfolder):
    cur_time = time.time()
    sync_tmp_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_tmp')
    print('sync_tmp folder %s '% sync_tmp_folder)
    if not os.path.exists(sync_tmp_folder):
        os.mkdir(sync_tmp_folder)
        print('sync tmp folder not exit we create it at %s' % sync_tmp_folder)
    for file in files:
        if os.path.dirname(file) == lfolder:
            store_folder = sync_tmp_folder
        else:
            subfolder = os.path.join(sync_tmp_folder,os.path.basename(os.path.dirname(file)) )
            if not os.path.exists(subfolder):
                os.mkdir(subfolder)
            store_folder = subfolder
        try:
            if cur_time - os.stat(file).st_mtime > 10:
                os.rename(file, os.path.join(store_folder, os.path.basename(file)))
                print('move %s to %s' % (file, os.path.join(store_folder, os.path.basename(file))))
            else:
                print('skip one file...%s' % file)

        except OSError:
            print('skip one file...%s' % file)
            print(sys.exc_info()[0])


def assign_homework(filetups=None, ondelete=True):
    _, _, max_thread = parse_config()
    max_thread = int(max_thread)
    file_num = len(filetups)
    if file_num > max_thread:
        reminder = file_num // max_thread
    reminder = len(filetups) // max_thread
    start = 0
    end = reminder
    if reminder:
        while end < len(filetups):
            #byyun.upload_file(filetups=filetups, ondelete=True)
            pro = multiprocessing.Process(target=byyun.upload_file, args =(None, None, filetups[start:end], True))
            print(start, end)
            pro.start()
            start += reminder
            end += reminder
    lefted = len(filetups) % max_thread
    if lefted:
        byyun.upload_file(None, None, filetups[-lefted:], True)
    pass



if __name__ == '__main__':
    sync_tmp_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_tmp')
    if not os.path.exists(sync_tmp_folder):
        print('tmp folder not exist, create it %s' % sync_tmp_folder)
        os.mkdir(sync_tmp_folder)
    lfolder, rfolder, _ = parse_config()
    print(lfolder, rfolder)
    while True:
        fail_count = 0
        file_list = get_file_list(lfolder, max=50)
        if file_list:
            move_upload_to(file_list, lfolder)
            print('we have new file %d' % len(file_list))
        else:
            file_list = get_file_list(sync_tmp_folder, max=50)
            if not file_list:
                print('no new file')
                time.sleep(3)
                continue
            else:
                print('%d files in tmp folder' % len(file_list))
        try:
            file_list = get_file_list(sync_tmp_folder, max=50)
            filetups = []
            for file in file_list:
                if os.path.dirname(file) == sync_tmp_folder:
                    rfolder = '/'
                else:
                    rfolder = os.path.join('/', os.path.basename(os.path.dirname(file)))
                filetups.append({'file': file, 'folder': rfolder})
                files = list()
                files.append(file)
            if filetups:
                assign_homework(filetups=filetups, ondelete=True)
                time.sleep(5)
                #ret = byyun.upload_file(filetups=filetups, ondelete=True)
                #if ret:
                #    print('fail count %d' % ret)
                #    time.sleep(5)
        except KeyboardInterrupt:
            print('keyboard interrupt')
            exit(1)
        except SystemExit:
            print(sys.exc_info()[0])
            print('other except')
            time.sleep(6)
            pass
