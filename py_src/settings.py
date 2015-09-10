#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

CAFFE_ROOT   = 'path/to/your/caffe'
PYSRC_ROOT   = 'path/to/your/py_src'

MODEL_DIR    = os.path.join(PYSRC_ROOT, '..', 'models')
PROTOTXT_DIR = os.path.join(PYSRC_ROOT, '..', 'prototxts')
