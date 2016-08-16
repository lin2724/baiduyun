import urllib2
import urllib
import requests
import hashlib
import os
import sys
import time

access_token = '21.1cb7ed1a2fe0fb2905cc3d3f3213861f.2592000.1473212979.2886689246-1572671'


def __get_dir_list(rfolder):

    login_data = {
        'method': 'list',
        'access_token': access_token,
        'path': rfolder,
        'by': 'name',
        'order': 'asc',
        #'limit': 'frame',
    }
    login_url = 'https://pcs.baidu.com/rest/2.0/pcs/file'
    r = requests.get(login_url, params=login_data)
    print(r.text)


def get_true_rpath(filepath, rfolder):
    rfolder = rfolder.lstrip('/')
    rpath = os.path.join('/apps/bypy/', os.path.join(rfolder, os.path.basename(filepath)))
    if os.name == 'nt':
        rpath = rpath.replace('\\', '/')
    return rpath


def upload_file(filepath=None, rfolder='/', filetups=None, ondelete=False):
    login_url = 'https://c.pcs.baidu.com/rest/2.0/pcs/file'
    #rfolder = rfolder.lstrip('/')
    #rpath = os.path.join('/apps/bypy/', os.path.join(rfolder, os.path.basename(filepath)))
    #rpath = '/apps/bypy/hkpic'
    #print(os.name)
    #if os.name == 'nt':
    #    rpath = rpath.replace('\\', '/')
    #print (rpath)
    #if not os.path.exists(filepath) or not os.path.isfile(filepath):
    #    print('file not exist or is not a file!!')
    #    return 1
    try:
        if filetups:
            login_data = {
                'method': 'upload',
                'access_token': access_token,
                'path': '',
                'ondup': 'overwrite',
            }
            fail_count = 0
            for filetup in filetups:
                filepath = filetup['file']
                actual_rfolder = get_true_rpath(filepath, filetup['folder'])
                login_data['path'] = actual_rfolder
                print('upload:%s' % filepath)
                print('TO')
                print(actual_rfolder)
                file_content = {'file': open(filepath, 'rb')}
                r = requests.post(login_url, params=login_data, files=file_content)
                if r.status_code != 200:
                    print(r.text)
                    fail_count += 1
                    print('upload fail: %s' % filepath)
                    time.sleep(3)
                else:
                    if ondelete:
                        os.remove(filepath)
            return fail_count
        else:
            actual_rfolder = get_true_rpath(filepath, rfolder)
            login_data = {
                'method': 'upload',
                'access_token': access_token,
                'path': actual_rfolder,
                'ondup': 'overwrite',
            }
            files = {'file':open(filepath, 'rb')}
            print('upload file: %s' % filepath)
            print('to')
            print(actual_rfolder)
            r = requests.post(login_url, params=login_data, files=files)
            print(r.text)
            return 0

    except KeyboardInterrupt:  #
        print('keyboard interrupt')
        exit(0)
    except requests.exceptions.SSLError:
        print('SSL error:maybe your system time set wrong,check it!')
        print(time.asctime())
        return 2
    except:
        print('upload fail :%s ' % filepath)
        print(sys.exc_info()[0])
        return 1



if __name__ == '__main__':
    fd = open('CSV.py')
    md5req = hashlib.md5()
    md5req.update(fd.read())
    fd.close()
    print(md5req.hexdigest())
    if len(sys.argv) > 1:
        print(sys.argv[1])
        upload_file(sys.argv[1], 'hkpic')
    else:
        upload_file('CSV.py', 'hkpic')

