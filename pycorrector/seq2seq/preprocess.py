# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief:
import sys

sys.path.append('../..')

from codecs import open
from xml.dom import minidom

from sklearn.model_selection import train_test_split

from pycorrector.seq2seq import config
from pycorrector.tokenizer import segment

split_symbol = ['，', '。', '？', '！']


def split_2_short_text(sentence):
    for i in split_symbol:
        sentence = sentence.replace(i, i + '\t')
    return sentence.split('\t')


def parse_xml_file(path):
    print('Parse data from %s' % path)
    data_list = []
    dom_tree = minidom.parse(path)
    docs = dom_tree.documentElement.getElementsByTagName('DOC')
    for doc in docs:
        # Input the text
        text = doc.getElementsByTagName('TEXT')[0]. \
            childNodes[0].data.strip()
        # Input the correct text
        correction = doc.getElementsByTagName('CORRECTION')[0]. \
            childNodes[0].data.strip()

        texts = split_2_short_text(text)
        corrections = split_2_short_text(correction)
        if len(texts) != len(corrections):
            print('error:' + text + '\t' + correction)
            continue
        for i in range(len(texts)):
            if len(texts[i]) > 40:
                print('error:' + texts[i] + '\t' + corrections[i])
                continue
            source = segment(texts[i], cut_type='char')
            target = segment(corrections[i], cut_type='char')
            pair = [source, target]
            if pair not in data_list:
                data_list.append(pair)
    return data_list


def _save_data(data_list, data_path):
    with open(data_path, 'w', encoding='utf-8') as f:
        count = 0
        for src, dst in data_list:
            f.write('src: ' + ' '.join(src) + '\n')
            f.write('dst: ' + ' '.join(dst) + '\n')
            count += 1
        print("save line size:%d to %s" % (count, data_path))


def transform_corpus_data(data_list, train_data_path, test_data_path):
    train_lst, test_lst = train_test_split(data_list, test_size=0.1)
    _save_data(train_lst, train_data_path)
    _save_data(test_lst, test_data_path)


if __name__ == '__main__':
    # train data
    data_list = []
    for path in config.raw_train_paths:
        data_list.extend(parse_xml_file(path))
    transform_corpus_data(data_list, config.train_path, config.test_path)
