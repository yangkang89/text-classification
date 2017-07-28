#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: yangkang
@license: Apache Licence 
@contact: ghooo55@gmail.com
@site: http://abc.com/
@software: PyCharm
@file: train.py
@time: 2017/7/26 上午9:49
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import time
import argparse
import pickle

import numpy as np
import pandas as pd
import tensorflow as tf
from cnn_model import CNNModel
from util import DataLoader
from lstm_model import LSTMModel

class SmallConfig(object):
  """Small config."""
  learning_rate = 0.001
  max_grad_norm = 5
  decay_rate = 0.9
  num_epochs=10
  save_every=100




data_loader = DataLoader(is_training=True)
vocab_size = data_loader.vocab_size
label_size = data_loader.label_size
seq_length=data_loader.seq_length

config=SmallConfig()
lstm_checkpoint_path = 'save/lstm/model.ckpt'
rnn_checkpoint_path = 'save/cnn/model.ckpt'

import os
for i in ['save/cnn','save/lstm']:
    if not os.path.exists(i):
        os.mkdir(i)
def lstm_train():


    #data_loader数据获取模块
    #数据大小
    #label个数(类数)
    #vocab:字到编号的字典
    #labels:类标签到编号的字典




    model = LSTMModel(is_training=True,vocab_size=vocab_size,label_size=label_size, seq_length=seq_length)

    with tf.Session() as sess:
        merged=tf.summary.merge_all()
        writer=tf.summary.FileWriter('logs',sess.graph)
        init = tf.global_variables_initializer()
        sess.run(init)
        saver = tf.train.Saver(tf.global_variables())


        for e in range(config.num_epochs):
            # if e > 0: tf.get_variable_scope().reuse_variables()
            # sess.run(tf.assign(model.lr, config.learning_rate * (config.decay_rate ** e)))
            data_loader.reset_batch_pointer()

            for b in range(data_loader.num_batches):
                start = time.time()
                x, y = data_loader.next_batch()
                feed = {model.lr:config.learning_rate * (config.decay_rate ** e),model.input_data: x, model.targets: y}
                train_loss, state, _, accuracy = sess.run([model.cost, model.final_state, model.optimizer, model.accuracy], feed_dict=feed)
                end = time.time()

                if (e*data_loader.num_batches+b+1) % config.save_every == 0 \
                    or (e==config.num_epochs-1 and b==data_loader.num_batches-1):
                    print('{}/{} (epoch {}), train_loss = {:.3f}, accuracy = {:.3f}, time/batch = {:.3f}' \
                          .format(e * data_loader.num_batches + b + 1,
                                  config.num_epochs * data_loader.num_batches,
                                  e + 1,
                                  train_loss,
                                  accuracy,
                                  end - start))

                    saver.save(sess, lstm_checkpoint_path, global_step=e*data_loader.num_batches+b+1)
                    # print('model saved to {}'.format(checkpoint_path))

                if b==0:
                    res=sess.run(merged,feed_dict=feed)
                    writer.add_summary(res,e)


def cnn_train():

    # model = Model(is_training=True,vocab_size=vocab_size,label_size=label_size,num_layers=2,config=config)
    model=CNNModel(is_training=True, vocab_size=vocab_size, label_size=label_size,seq_length=seq_length)

    with tf.Session() as sess:
        merged=tf.summary.merge_all()
        writer=tf.summary.FileWriter('logs',sess.graph)
        init = tf.global_variables_initializer()
        sess.run(init)
        saver = tf.train.Saver(tf.global_variables())


        for e in range(config.num_epochs):
            # if e > 0: tf.get_variable_scope().reuse_variables()
            # sess.run(tf.assign(model.lr, config.learning_rate * (config.decay_rate ** e)))
            data_loader.reset_batch_pointer()

            for b in range(data_loader.num_batches):
                start = time.time()
                x, y = data_loader.next_batch()
                feed = {model.input_data: x, model.target: y}
                train_loss, _, accuracy = sess.run([model.loss, model.optimizer, model.accuracy], feed_dict=feed)
                end = time.time()

                if (e*data_loader.num_batches+b+1) % config.save_every == 0 \
                    or (e==config.num_epochs-1 and b==data_loader.num_batches-1):
                    print('{}/{} (epoch {}), train_loss = {:.3f}, accuracy = {:.3f}, time/batch = {:.3f}' \
                          .format(e * data_loader.num_batches + b + 1,
                                  config.num_epochs * data_loader.num_batches,
                                  e + 1,
                                  train_loss,
                                  accuracy,
                                  end - start))

                    saver.save(sess, rnn_checkpoint_path, global_step=e*data_loader.num_batches+b+1)

                # if b==0:
                #     res=sess.run(merged,feed_dict=feed)
                #     writer.add_summary(res,e)
if __name__ == "__main__":
    cnn_train()
    lstm_train()
