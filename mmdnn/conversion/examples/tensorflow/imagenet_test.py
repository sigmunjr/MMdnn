#----------------------------------------------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
#----------------------------------------------------------------------------------------------

import argparse
import numpy as np
import sys
import os
import tensorflow as tf
from mmdnn.conversion.examples.imagenet_test import TestKit

class TestTF(TestKit):

    def __init__(self):
        super(TestTF, self).__init__()
        self.input, self.model = self.MainModel.KitModel(self.args.w)
        # self.input, self.model, self.testop = self.MainModel.KitModel(self.args.w)


    def preprocess(self, image_path):
        x = super(TestTF, self).preprocess(image_path)
        self.data = np.expand_dims(x, 0)


    def print_result(self):
        with tf.Session() as sess:
            writer = tf.summary.FileWriter('./graphs', sess.graph)
            writer.close()
            init = tf.global_variables_initializer()
            sess.run(init)
            predict = sess.run(self.model, feed_dict = {self.input : self.data})
        
        super(TestTF, self).print_result(predict)
        
    
    def print_intermediate_result(self, layer_name, if_transpose = False):
        # testop = tf.get_default_graph().get_operation_by_name(layer_name)
        testop = self.testop
        with tf.Session() as sess:
            init = tf.global_variables_initializer()
            sess.run(init)
            intermediate_output = sess.run(testop, feed_dict = {self.input : self.data})
        
        super(TestTF, self).print_intermediate_result(intermediate_output, if_transpose)

    
    def inference(self, image_path):
        self.preprocess(image_path)
        
        # self.print_intermediate_result('conv1_7x7_s2_1', True)
        
        self.print_result()
        
        self.test_truth()


    def dump(self, path = None):
        if path is None: path = self.args.dump        
        with tf.Session() as sess:
            init = tf.global_variables_initializer()
            sess.run(init)
            saver = tf.train.Saver()
            save_path = saver.save(sess, self.args.dump)
            print ('Tensorflow file is saved as [{}], generated by [{}.py] and [{}].'.format(
                save_path, self.args.n, self.args.w))


if __name__=='__main__':       
    tester = TestTF()
    if tester.args.dump:
        tester.dump()
    else:
        tester.inference(tester.args.image)
