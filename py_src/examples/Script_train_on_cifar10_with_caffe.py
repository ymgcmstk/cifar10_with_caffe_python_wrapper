#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath(os.path.join('..', 'tools')))

from settings import *
from caffe_trainer import CaffeTrainer
from cifar10_fetcher import Cifar10Fetcher
from myfunctions import *

if __name__ == '__main__':
    SAVETEST = True

    fetcher         = Cifar10Fetcher(norm=False)
    solver_prototxt = os.path.join(PROTOTXT_DIR, 'cifar10/solver_cifar10_quick.prototxt')

    CT           = CaffeTrainer(fetcher, solver_prototxt, 1)
    CT.batchsize = 100

    if SAVETEST:
        CT.train_and_val(early_stopping_count=1)
        CT.save_model('temp.caffemodel')
    else:
        CT.load_model('temp.caffemodel')
        CT.val_one_epoch(verbose=True)
