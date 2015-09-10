import caffe
import numpy as np
import json

class CaffeDataLayer(caffe.Layer):
    _name_to_top_map_and_type = {'data': [0, np.float32],
                                 'labels': [1, np.int32]}

    def set_next_minibatch(self, blob):
        self._next_blob = blob

    def setup(self, bottom, top):
        dic_shape = json.loads(self.param_str)
        for shape_key, this_shape in dic_shape.items():
            top[self._name_to_top_map_and_type[shape_key][0]].reshape(*this_shape)

    def forward(self, bottom, top):
        for blob_name, blob in self._next_blob.iteritems():
            top_ind, top_type = self._name_to_top_map_and_type[blob_name]
            top[top_ind].reshape(*(blob.shape))
            top[top_ind].data[...] = blob.astype(top_type, copy=False)

    def backward(self, top, propagate_down, bottom):
        pass

    def reshape(self, bottom, top):
        pass
