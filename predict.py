#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: yangkang
@license: Apache Licence 
@contact: ghooo55@gmail.com
@site: http://abc.com/
@software: PyCharm
@file: test.py.py
@time: 2017/7/26 下午3:29
"""
import numpy as np
import os
import pickle
from model import Model
from util import DataLoader
import tensorflow as tf
import time



class CheckConfig(object):
  """Tiny config, for testing."""
  init_scale = 0.1
  learning_rate = 1.0
  max_grad_norm = 1
  num_layers = 1
  num_steps = 20
  hidden_size = 128
  # max_epoch = 1
  # max_max_epoch = 1
  keep_prob = 1.0
  lr_decay = 0.5
  batch_size = 30



config=CheckConfig
data_loader = DataLoader(False, config.batch_size, config.num_steps)
vocab_size = data_loader.vocab_size
label_size = data_loader.label_size
model = Model(is_training=False, vocab_size=vocab_size, label_size=label_size, num_layers=2,config=config)
def sample(text):




    x = data_loader.transform(text)

    with tf.Session() as sess:
        saver =tf.train.Saver()
        saver.restore(sess,'/Users/yangkang/PycharmProjects/TextClassification/save/model.ckpt')
        # ckpt = tf.train.get_checkpoint_state(args.save_dir)
        # if ckpt and ckpt.model_checkpoint_path:
        #     saver.restore(sess, ckpt.model_checkpoint_path)
        print(list(predict_label(sess, model, data_loader.labels, [x])))



def accuracy():
    # with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
    #     saved_args = pickle.load(f)
    # with open(os.path.join(args.utils_dir, 'chars_vocab.pkl'), 'rb') as f:
    #     chars, vocab = pickle.load(f)
    # with open(os.path.join(args.utils_dir, 'labels.pkl'), 'rb') as f:
    #     labels = pickle.load(f)

    # model = Model(is_training=False,vocab_size=vocab_size,label_size=label_size,config=config)

    with tf.Session() as sess:
        saver = tf.train.Saver(tf.all_variables())

        saver.restore(sess, '/Users/yangkang/PycharmProjects/TextClassification/save/model.ckpt')

        data = data_loader.tensor.copy()
        n_chunks = int(len(data) / config.batch_size)
        if len(data) % config.batch_size:
            n_chunks += 1
        data_list = np.array_split(data, n_chunks, axis=0)

        correct_total = 0.0
        num_total = 0.0
        for m in range(n_chunks):
            start = time.time()
            x = data_list[m][:, :-1]
            y = data_list[m][:, -1]
            results = predict_class(sess=sess,model=model,data=x)
            correct_num = np.sum(results==y)
            end = time.time()
            print('batch {}/{} cost time {:.3f}, sub_accuracy = {:.6f}'.format(m+1, n_chunks, end-start, correct_num*1.0/len(x)))

            correct_total += correct_num
            num_total += len(x)

        accuracy_total = correct_total / num_total
        print('total_num = {}, total_accuracy = {:.6f}'.format(int(num_total), accuracy_total))





def predict_class(sess, model,data):
    x = np.array(data)
    feed = {model.input_data: x}
    probs, state = sess.run([model.probs, model.final_state], feed_dict=feed)

    results = np.argmax(probs, 1)
    return results






def predict_label(sess, model, labels, text):
    x = np.array(text)
    feed = {model.input_data: x}
    probs, state = sess.run([model.probs, model.final_state], feed_dict=feed)

    results = []
    # for index, i in enumerate(probs[0]):
    #     if i > 0.02:
    #         results.append(index)
    #
    results = np.argmax(probs, 1)
    id2labels = dict(zip(labels.values(), labels.keys()))
    labels = map(id2labels.get, results)
    return labels

if __name__ == "__main__":
    # sample("我冲了话费还没有到")
    accuracy()