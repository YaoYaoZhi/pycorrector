# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
import os

import numpy as np
import tensorflow as tf

from pycorrector.rnn_lm.data_reader import UNK_TOKEN, END_TOKEN, START_TOKEN, load_word_dict
from pycorrector.rnn_lm.rnn_lm_model import rnn_model
from pycorrector.utils.logger import logger

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class LM:
    def __init__(self, model_path, vocab_path, learning_rate=0.01, batch_size=1):
        self.word_to_idx = load_word_dict(vocab_path)
        self.idx_to_word = {v: k for k, v in self.word_to_idx.items()}
        self.learning_rate = learning_rate
        self.batch_size = batch_size

        tf.reset_default_graph()
        self.input_data = tf.placeholder(tf.int32, [batch_size, None])
        self.output_targets = tf.placeholder(tf.int32, [batch_size, None])
        # init model
        self.model = rnn_model(model='lstm',
                               input_data=self.input_data,
                               output_data=self.output_targets,
                               vocab_size=len(self.word_to_idx),
                               rnn_size=128,
                               num_layers=2,
                               batch_size=batch_size,
                               learning_rate=learning_rate)
        saver = tf.train.Saver(tf.global_variables())
        init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
        self.sess = tf.Session()
        # init op
        self.sess.run(init_op)
        checkpoint = tf.train.latest_checkpoint(model_path)
        saver.restore(self.sess, checkpoint)
        logger.info("loading model from the checkpoint {0}".format(checkpoint))

    def perplexities(self, sentences):
        result = []
        for sentence in sentences:
            result.append(self.perplexity(sentence))
        return result

    def score(self, sentence, *args, **kwargs):
        sentence = ''.join([i for i in sentence if i])
        return self.perplexity(sentence)

    def perplexity(self, sentence):
        sentence = ''.join([i for i in sentence if i])
        ppl = 0
        # data idx
        x = [self.word_to_idx[c] if c in self.word_to_idx else self.word_to_idx[UNK_TOKEN] for c in sentence]
        x = [self.word_to_idx[START_TOKEN]] + x + [self.word_to_idx[END_TOKEN]]
        # reshape
        y = np.array(x[1:]).reshape((-1, self.batch_size))
        x = np.array(x[:-1]).reshape((-1, self.batch_size))
        # get each word perplexity
        word_count = x.shape[0]
        for i in range(word_count):
            perplexity = self.sess.run(self.model['perplexity'],
                                       feed_dict={self.input_data: x[i:i + 1, :],
                                                  self.output_targets: y[i:i + 1, :]})
            # logger.debug('{0} -> {1}, perplexity: {2}'.format(self.idx_to_word[x[i:i + 1, :].tolist()[0][0]],
            #                                                   self.idx_to_word[y[i:i + 1, :].tolist()[0][0]],
            #                                                   perplexity))
            if i == 0 or i == word_count:
                continue
            ppl += perplexity
        ppl /= (word_count - 2)
        return ppl
