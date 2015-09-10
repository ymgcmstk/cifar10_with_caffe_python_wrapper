#!/usr/bin/env python
# -*- coding:utf-8 -*-

import google.protobuf as pb2
import numpy as np
import os
import sys

sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath(os.path.join('..', 'tools')))

from settings import *
from myfunctions import *

sys.path.append(os.path.join(CAFFE_ROOT, 'python'))

import caffe
from caffe.proto import caffe_pb2

class CaffeTrainer:
    model_dir  = MODEL_DIR
    model_name = False # model name or False
    prefix     = ''
    batchsize  = 32
    n_epoch    = 50
    gpu_id     = None

    def __init__(self, fetcher, solver_prototxt, gpu_id=None):
        assert isinstance(solver_prototxt, str)
        if gpu_id is not None:
            self.gpu_id = gpu_id # id or None
        if self.gpu_id is not None:
            caffe.set_mode_gpu()
            caffe.set_device(self.gpu_id)
            print 'GPU_' + str(self.gpu_id) + ' will be used.'
        self.fetcher = fetcher
        self.init_solver(solver_prototxt)

    def init_solver(self, solver_prototxt):
        self.solver = caffe.SGDSolver(solver_prototxt)
        self.solver_param = caffe_pb2.SolverParameter()
        with open(solver_prototxt, 'rt') as f:
            pb2.text_format.Merge(f.read(), self.solver_param)

    def set_blob(self, blob, layer_name, blob_ind=0, blob_type=None):
        if blob_type is None:
            self.solver.net.params[layer_name][blob_ind].data[...] = blob.astype(np.float32)
        else:
            self.solver.net.params[layer_name][blob_ind].data[...] = blob.astype(blob_type)

    def train_one_epoch(self, verbose=False):
        # training
        sum_accuracy = 0
        sum_loss     = 0
        assert self.fetcher.end_of_epoch_train
        while True:
            if verbose and self.fetcher.train_count > 0:
                printr('[train] epoch :',
                       self.fetcher.epoch_count,
                       ',',
                       self.fetcher.train_count,
                       '/',
                       self.fetcher.N_train,
                       ', acc :',
                       sum_accuracy / self.fetcher.train_count,
                       ', loss :',
                       sum_loss / self.fetcher.train_count
                       )
            x_batch, y_batch = self.fetcher.fetch_train_data(self.batchsize)
            blob = {'data':x_batch, 'labels':y_batch}
            self.solver.net.layers[0].set_next_minibatch(blob)
            self.solver.step(1)
            sum_loss     += self.solver.net.blobs['loss'].data * self.batchsize
            sum_accuracy += self.solver.net.blobs['accuracy'].data * self.batchsize

            if self.fetcher.end_of_epoch_train:
                break

        if verbose:
            print 'train mean loss={}, accuracy={}'.format(
                sum_loss / self.fetcher.N_train, sum_accuracy / self.fetcher.N_train)
        return sum_loss / self.fetcher.N_train, sum_accuracy / self.fetcher.N_train

    def val_one_epoch(self, verbose=False):
        # evaluation
        sum_accuracy = 0
        sum_loss     = 0
        assert self.fetcher.end_of_epoch_val
        while True:
            if verbose and self.fetcher.val_count > 0:
                printr('[val] epoch :',
                       self.fetcher.epoch_count,
                       ',',
                       self.fetcher.val_count,
                       '/',
                       self.fetcher.N_val,
                       ', acc :',
                       sum_accuracy / self.fetcher.val_count,
                       ', loss :',
                       sum_loss / self.fetcher.val_count
                       )
            x_batch, y_batch = self.fetcher.fetch_val_data(self.batchsize)
            blob = {'data':x_batch, 'labels':y_batch}
            self.solver.net.layers[0].set_next_minibatch(blob)
            self.solver.net.forward()
            sum_loss     += self.solver.net.blobs['loss'].data * self.batchsize
            sum_accuracy += self.solver.net.blobs['accuracy'].data * self.batchsize

            if self.fetcher.end_of_epoch_val:
                break

        if verbose:
            print 'val mean loss={}, accuracy={}'.format(
                sum_loss / self.fetcher.N_val, sum_accuracy / self.fetcher.N_val)
        return sum_loss / self.fetcher.N_val, sum_accuracy / self.fetcher.N_val

    def save_model(self, model_name):
        if not os.path.exists(self.model_dir):
            os.mkdir(self.model_dir)
        if self.prefix is None:
            save_path = os.path.join(self.model_dir, model_name)
        elif len(str(self.prefix)) == 0:
            save_path = os.path.join(self.model_dir, model_name)
        else:
            save_path = os.path.join(self.model_dir, self.prefix + '_' + model_name)
        self.solver.net.save(save_path)
        print 'Current model has been saved as ' + save_path + '.'

    def load_model(self, model_name):
        model_path = os.path.join(self.model_dir, model_name)
        self.solver.net.copy_from(model_path)

    def train_and_val(self, verbose=False, early_stopping_count=0):
        max_acc     = 0
        break_count = 0
        while True:
            if self.fetcher.epoch_count > self.n_epoch:
                break
            print 'epoch', self.fetcher.epoch_count
            train_loss, train_acc = self.train_one_epoch(verbose)
            val_loss, val_acc     = self.val_one_epoch(verbose)
            if max_acc > val_acc:
                break_count += 1
                if break_count == early_stopping_count:
                    break
            else:
                max_acc = val_acc
