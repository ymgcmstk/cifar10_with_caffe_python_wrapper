#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cPickle as pickle
import numpy as np
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..', 'tools')))
from base_fetcher import BaseFetcher

class Cifar10Fetcher(BaseFetcher):
    ds_path     = '/path/to/your/dataset/cifar'
    x_train     = None
    y_train     = []
    x_val       = None
    y_val       = []
    N_train     = 0
    N_val       = 0

    def __init__(self, minus_mean=True, norm=True):
        BaseFetcher.__init__(self)
        if minus_mean:
            self.minus_mean = minus_mean
            self.__minus_mean_from_data()
        if norm:
            self.norm = norm
            self.__norm_from_data()

    def load_data(self):
        for i in xrange(1,6):
            data_dictionary = pickle.load(open(os.path.join(self.ds_path, 'data_batch_%d') % i, 'rb'))
            if self.x_train is None:
                self.x_train = data_dictionary['data']
                self.y_train = data_dictionary['labels']
            else:
                self.x_train = np.vstack((self.x_train, data_dictionary['data']))
                self.y_train = self.y_train + data_dictionary['labels']
        self.x_train = self.x_train.reshape((len(self.x_train), 3, 32, 32)).astype(np.float32)
        self.y_train = np.array(self.y_train).astype(np.int32)

        val_data_dictionary = pickle.load(open(os.path.join(self.ds_path, 'test_batch'), 'rb'))
        self.x_val   = val_data_dictionary['data'].reshape(len(val_data_dictionary['data']), 3, 32, 32).astype(np.float32)
        self.y_val   = np.array(val_data_dictionary['labels']).astype(np.int32)
        self.N_train = len(self.x_train)
        self.N_val   = len(self.x_val)

    def return_train_data(self, start_ind, end_ind):
        return self.x_train[self.perm[start_ind:end_ind]], self.y_train[self.perm[start_ind:end_ind]]

    def return_val_data(self, start_ind, end_ind):
        return self.x_val[start_ind:end_ind], self.y_val[start_ind:end_ind]

    def __minus_mean_from_data(self):
        self.mean_data = self.x_train.mean(axis=0)
        self.x_train   -= self.mean_data
        self.x_val     -= self.mean_data
        assert np.abs(self.x_train.mean()) < 1e-5

    def __norm_from_data(self):
        self.std     = self.x_train.std()
        self.x_train /= self.std
        self.x_val   /= self.std
        assert np.abs(self.x_train.std() - 1.0) < 1e-5
