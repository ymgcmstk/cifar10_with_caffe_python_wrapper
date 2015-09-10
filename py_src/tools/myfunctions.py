#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import shutil
import types
import json
import cPickle
import pickle
import time

class TimeReporter:
    def __init__(self, max_count):
        self.time       = time.time
        self.start_time = time.time()
        self.max_count  = max_count
        self.cur_count  = 0
    def report(self, cur_count=None, max_count=None, overwrite=True, prefix=None, postfix=None):
        if cur_count is not None:
            self.cur_count = cur_count
        else:
            self.cur_count += 1
        if max_count is None:
            max_count = self.max_count
        cur_time = self.time()
        elapsed  = cur_time - self.start_time
        if self.cur_count <= 0:
            ave_time = float('inf')
        else:
            ave_time = elapsed / self.cur_count
        ETA = (max_count - self.cur_count) * ave_time
        print_str = 'count : %d, elapsed time : %f, ETA : %f' % (self.cur_count, elapsed, ETA)
        if prefix is not None:
            print_str = str(prefix) + ' ' + print_str
        if postfix is not None:
            print_str += ' ' + str(postfix)
        if overwrite:
            printr(print_str)
        else:
            print print_str

def textread(path):
    if not os.path.exists(path):
        print path, 'does not exist.'
        return False
    f = open(path)
    lines = f.readlines()
    f.close()
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')
    return lines

def textdump(path, lines):
    if os.path.exists(path):
        if 'n' == choosebyinput(['Y', 'n'], path + ' exists. Would you replace? [Y/n]'):
            return False
    f = open(path, 'w')
    for i in lines:
        f.write(i + '\n')
    f.close()

def pickleload(path):
    if not os.path.exists(path):
        print path, 'does not exist.'
        return False
    f = open(path)
    this_ans = pickle.load(f)
    f.close()
    return this_ans

def pickledump(path, this_dic):
    f = open(path, 'w')
    this_ans = pickle.dump(this_dic, f)
    f.close()

def cPickleload(path):
    if not os.path.exists(path):
        print path, 'does not exist.'
        return False
    f = open(path, 'rb')
    this_ans = cPickle.load(f)
    f.close()
    return this_ans

def cPickledump(path, this_dic):
    f = open(path, 'wb')
    this_ans = cPickle.dump(this_dic, f, -1)
    f.close()

def jsonload(path):
    if not os.path.exists(path):
        print path, 'does not exist.'
        return False
    f = open(path)
    this_ans = json.load(f)
    f.close()
    return this_ans

def jsondump(path, this_dic):
    f = open(path, 'w')
    this_ans = json.dump(this_dic, f)
    f.close()

def choosebyinput(cand, message=False):
    if not type(cand) == list and not type(cand) == int:
        print 'The type of cand_list has to be \'list\' or \'int\' .'
        return
    if type(cand) == int:
        cand_list = range(cand)
    if type(cand) == list:
        cand_list = cand
    int_cand_list = []
    for i in cand_list:
        if type(i) == int:
            int_cand_list.append(str(i))
    if message == False:
        message = 'choose by input : ['
        for i in int_cand_list:
            message += i + ' / '
        for i in cand_list:
            if not str(i) in int_cand_list:
                message += i + ' / '
        message = message[:-3] + ']'
    while True:
        your_ans = raw_input(message)
        if your_ans in int_cand_list:
            return int(your_ans)
            break
        if your_ans in cand_list:
            return your_ans
            break

def mv_files(name1, name2):
    files = os.listdir('.')
    for this_file in files:
        if name1 in this_file:
            flg = True
            if os.path.exists(this_file.replace(name1, name2)):
                your_ans = choosebyinput(['Y', 'n'], message=this_file.replace(name1, name2) + ' exists. Would you replace? [Y/n]')
                if your_ans == 'n':
                    flg = False
                    break
                elif your_ans == 'Y':
                    flg = True
                    break
            if flg:
                shutil.move(this_file, this_file.replace(name1, name2))
                print this_file, 'is moved to', this_file.replace(name1, name2)

def find_from_to(str1, start_str, end_str):
    start_num = str1.find(start_str) + len(start_str)
    end_num = str1.find(end_str, start_num)
    return str1[start_num:end_num]

def get_photo(url, fname):
    try:
        urllib.urlretrieve(url, fname)
        urllib.urlcleanup()
        return True
    except IOError:
        return False
    except urllib2.HTTPError:
        return False
    except urllib2.URLError:
        return False
    except httplib.BadStatusLine:
        return False

def get_photos(photos):
    for i in photos:
        threads=[]
        for photo in photos:
            if not 'http' in photo[0]:
                print 'Maybe urls and file names are the opposite. You should switch the indices.'
            t = threading.Thread(target = get_photo,args = (photo[0], photo[1]))
            threads.append(t)
            t.start()

def printr(*targ_str):
    str_to_print = ''
    for temp_str in targ_str:
        str_to_print += str(temp_str) + ' '
    str_to_print = str_to_print[:-1]
    sys.stdout.write(str_to_print + '\r')
    sys.stdout.flush()

def mkdir_if_missing(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

def makedirs_if_missing(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def makebsdirs_if_missing(f_path):
    if not os.path.exists(os.path.basename(f_path)):
        os.makedirs(os.path.basename(f_path))
