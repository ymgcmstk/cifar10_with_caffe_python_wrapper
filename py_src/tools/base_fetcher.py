#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np

class BaseFetcher:
    train_count = 0
    val_count   = 0
    iter_count  = 0
    used_count  = 0
    epoch_count = 0

    def __init__(self):
        self.load_data()
        self.perm = np.arange(self.N_train)

    def fetch_train_data(self, batch_size, permutate=True, augment=False, discard=False):
        self.iter_count += 1
        self.used_count += batch_size
        if self.N_train == 0:
            return
        if self.train_count == 0 and permutate:
            self.perm = np.random.permutation(self.N_train)
        start_ind = self.train_count
        if self.train_count >= self.N_train - batch_size:
            end_ind          = self.N_train
            self.train_count = 0
            self.epoch_count += 1
        elif discard and self.train_count > self.N_train - 2 * batch_size:
            end_ind          = self.train_count + batch_size
            self.train_count = 0
            self.epoch_count += 1
        else:
            end_ind          = self.train_count + batch_size
            self.train_count += batch_size
        return self.return_train_data(start_ind, end_ind)

    def fetch_val_data(self, batch_size, augment=False, discard=False):
        if self.N_val == 0:
            return
        start_ind = self.val_count
        if self.val_count >= self.N_val - batch_size:
            end_ind        = self.N_val
            self.val_count = 0
        elif discard and self.val_count > self.N_val - 2 * batch_size:
            # Not recommended
            end_ind          = self.val_count + batch_size
            self.val_count = 0
        else:
            end_ind        = self.val_count + batch_size
            self.val_count += batch_size
        return self.return_val_data(start_ind, end_ind)

    @property
    def end_of_epoch_train(self):
        if self.train_count == 0:
            return True
        else:
            return False

    @property
    def end_of_epoch_val(self):
        if self.val_count == 0:
            return True
        else:
            return False
