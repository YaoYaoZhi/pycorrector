# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 
from __future__ import print_function

import sys

from setuptools import setup, find_packages

from pycorrector import __version__

if sys.version_info < (3,):
    sys.exit('Sorry, Python3 is required for pycorrector.')

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    reqs = f.read()

setup(
    name='pycorrector',
    version=__version__,
    description='Chinese Text Error corrector',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='XuMing',
    author_email='xuming624@qq.com',
    url='https://github.com/shibing624/pycorrector',
    license="Apache 2.0",
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='NLP,correction,Chinese error corrector,corrector',
    install_requires=reqs.strip().split('\n'),
    packages=find_packages(exclude=['tests']),
    package_dir={'pycorrector': 'pycorrector'},
    package_data={
        'pycorrector': ['*.*', 'LICENSE', '../LICENSE', 'README.*', '../*.txt', 'data/*',
                        'data/kenlm/people_chars_lm.klm', 'utils/*',
                        'bert/*', 'deep_context/*', 'rnn_attention/*', 'rnn_crf/*', 'rnn_lm/*', 'seq2seq/*',
                        'seq2seq_attention/*', 'transformer/*'],
    },
    test_suite='tests',
)
