![alt text](docs/logo.svg)

[![PyPI version](https://badge.fury.io/py/pycorrector.svg)](https://badge.fury.io/py/pycorrector)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![License Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/shibing624/pycorrector/LICENSE)
![Language](https://img.shields.io/badge/Language-Python-blue.svg)
![Python3](https://img.shields.io/badge/Python-3.X-red.svg)


# pycorrector

中文文本纠错工具。音似、形似错字（或变体字）纠正，可用于中文拼音、笔画输入法的错误纠正。python3开发。

**pycorrector**依据语言模型检测错别字位置，通过拼音音似特征、笔画五笔编辑距离特征及语言模型困惑度特征纠正错别字。

## 问题

中文文本纠错任务，常见错误类型包括：

- 谐音字词，如 配副眼睛-配副眼镜
- 混淆音字词，如 流浪织女-牛郎织女
- 字词顺序颠倒，如 伍迪艾伦-艾伦伍迪
- 字词补全，如 爱有天意-假如爱有天意
- 形似字错误，如 高梁-高粱
- 中文拼音全拼，如 xingfu-幸福
- 中文拼音缩写，如 sz-深圳
- 语法错误，如 想象难以-难以想象

当然，针对不同业务场景，这些问题并不一定全部存在，比如输入法中需要处理前四种，搜索引擎需要处理所有类型，语音识别后文本纠错只需要处理前两种，
其中'形似字错误'主要针对五笔或者笔画手写输入等。


## 解决方案
### 规则的解决思路
1. 中文纠错分为两步走，第一步是错误检测，第二步是错误纠正；
2. 错误检测部分先通过结巴中文分词器切词，由于句子中含有错别字，所以切词结果往往会有切分错误的情况，这样从字粒度和词粒度两方面检测错误，
整合这两种粒度的疑似错误结果，形成疑似错误位置候选集；
3. 错误纠正部分，是遍历所有的疑似错误位置，并使用音似、形似词典替换错误位置的词，然后通过语言模型计算句子困惑度，对所有候选集结果比较并排序，得到最优纠正词。

### 深度模型的解决思路
1. 端到端的深度模型可以避免人工提取特征，减少人工工作量，RNN序列模型对文本任务拟合能力强，rnn_attention在英文文本纠错比赛中取得第一名成绩，证明应用效果不错；
2. CRF会计算全局最优输出节点的条件概率，对句子中特定错误类型的检测，会根据整句话判定该错误，阿里参赛2016中文语法纠错任务并取得第一名，证明应用效果不错；
3. seq2seq模型是使用encoder-decoder结构解决序列转换问题，目前在序列转换任务中（如机器翻译、对话生成、文本摘要、图像描述）使用最广泛、效果最好的模型之一。


## 特征
### 模型
* kenlm：kenlm统计语言模型工具
* rnn_lm：TensorFlow、PaddlePaddle均有实现栈式双向LSTM的语言模型
* rnn_attention模型：参考Stanford University的nlc模型，该模型是参加2014英文文本纠错比赛并取得第一名的方法
* rnn_crf模型：参考阿里巴巴2016参赛中文语法纠错比赛并取得第一名的方法
* seq2seq模型：使用序列模型解决文本纠错任务，文本语法纠错任务中常用模型之一
* seq2seq_attention模型：在seq2seq模型加上attention机制，对于长文本效果更好，模型更容易收敛，但容易过拟合
* transformer模型：全attention的结构代替了lstm用于解决sequence to sequence问题，语义特征提取效果更好
* bert模型：中文fine-tuned模型，使用MASK特征纠正错字


### 错误检测
* 字粒度：语言模型困惑度（ppl）检测某字的似然概率值低于句子文本平均值，则判定该字是疑似错别字的概率大。
* 词粒度：切词后不在词典中的词是疑似错词的概率大。


### 错误纠正
* 通过错误检测定位所有疑似错误后，取所有疑似错字的音似、形似候选词，
* 使用候选词替换，基于语言模型得到类似翻译模型的候选排序结果，得到最优纠正词。


### 思考
1. 现在的处理手段，在词粒度的错误召回还不错，但错误纠正的准确率还有待提高，更多优质的纠错集及纠错词库会有提升，我更希望算法上有更大的突破。
2. 另外，现在的文本错误不再局限于字词粒度上的拼写错误，需要提高中文语法错误检测（CGED, Chinese Grammar Error Diagnosis）及纠正能力，列在TODO中，后续调研。

## demo

https://www.borntowin.cn/product/corrector


## 规则方案使用说明

### 安装依赖
```
pip3 install -r requirements.txt
```

### 安装
* 全自动安装：pip3 install pycorrector
* 半自动安装：
```
git clone https://github.com/shibing624/pycorrector.git
cd pycorrector
python3 setup.py install
```


### 纠错  
使用示例:
```
import pycorrector

corrected_sent, detail = pycorrector.correct('少先队员因该为老人让坐')
print(corrected_sent, detail)

```

输出:
```
少先队员应该为老人让座 [[('因该', '应该', 4, 6)], [('坐', '座', 10, 11)]]
```


## 深度方案使用说明

### 安装依赖
```
pip3 install -r requirements.txt

pip3 install git+https://www.github.com/keras-team/keras-contrib.git
```

### 介绍

本项目的初衷之一是比对、共享各种文本纠错方法，抛砖引玉的作用，如果对大家在文本纠错任务上有一点小小的启发就是我莫大的荣幸了。

主要使用了多种深度模型应用于文本纠错任务，分别是前面`模型`小节介绍的`rnn_attention`、`rnn_crf`、`seq2seq`、`seq2seq_attention`、`transformer`、`bert`，每种方法单独放在文件夹中，
都可以独立运行，相互之间无依赖。


### 使用方法
各模型均可独立预处理数据、训练、预测，下面以其中`seq2seq_attention`为例：

seq2seq_attention 模型使用示例:

#### 配置

通过修改`config.py`。


#### 数据预处理
```
cd seq2seq_attention
# 数据预处理
python3 preprocess.py

```
自动新建文件夹output，在output下生成train.txt和test.txt文件，文件内容示例：

```
src: 不 然 的 话 ， 两 方 面 的 问 题 都 不 能 决 绝 ， 而 对 双 方 导 致 不 良 影 响 。
dst: 不 然 的 话 ， 两 方 面 的 问 题 都 不 能 解 决 ， 而 对 双 方 产 生 不 良 影 响 。
src: 你 们 的 这 种 精 神 使 我 更 加 勇 气 ， 努 力 学 习 。
dst: 你 们 的 这 种 精 神 使 我 增 加 勇 气 ， 努 力 学 习 。
```

#### 训练
```
# 训练
python3 train.py
```

#### 预测
```
# 预测
python3 infer.py
```


预测输出效果样例:

![long correct result](https://github.com/shibing624/pycorrector/blob/master/pycorrector/data/git_image/long_text.png)



## 自定义语言模型

语言模型对于纠错步骤至关重要，目前我能收集到的语料数据有人民日报数据。大家可以用中文维基（繁体转简体，pycorrector.utils下有此功能）等更大的语料数据训练效果更好的语言模型，
对于纠错效果会有比较好的提升。

1. kenlm语言模型训练工具的使用，请见博客：http://blog.csdn.net/mingzai624/article/details/79560063
2. 附上训练语料<人民日报2014版熟语料>，包括：
    1）标准人工切词及词性数据people2014.tar.gz，
    2）未切词文本数据people2014_words.txt，
    3）kenlm训练字粒度语言模型文件及其二进制文件people2014corpus_chars.arps/klm，
    4）kenlm词粒度语言模型文件及其二进制文件people2014corpus_words.arps/klm。

网盘链接:https://pan.baidu.com/s/1971a5XLQsIpL0zL0zxuK2A  密码:uc11。尊重版权，传播请注明出处。


## 贡献及优化点

- [x] 使用RNN语言模型来提高纠错准确率
- [x] 优化形似字字典，提高形似字纠错准确率
- [x] 整理中文纠错训练数据，使用seq2seq做深度中文纠错模型
- [x] 添加中文语法错误检测及纠正能力
- [x] 规则方法添加用户自定义纠错集，并将其纠错优先度调为最高
- [x] seq2seq_attention 添加dropout，减少过拟合


## 参考

1. [基于文法模型的中文纠错系统](https://blog.csdn.net/mingzai624/article/details/82390382)
2. [Norvig’s spelling corrector](http://norvig.com/spell-correct.html)
3. [《Chinese Spelling Error Detection and Correction Based on Language Model, Pronunciation, and Shape》[Yu, 2013]](http://www.aclweb.org/anthology/W/W14/W14-6835.pdf)
4. [《Chinese Spelling Checker Based on Statistical Machine Translation》[Chiu, 2013]](http://www.aclweb.org/anthology/O/O13/O13-1005.pdf)
5. [《Chinese Word Spelling Correction Based on Rule Induction》[yeh, 2014]](http://aclweb.org/anthology/W14-6822)
6. [《Neural Language Correction with Character-Based Attention》[Ziang Xie, 2016]](https://arxiv.org/pdf/1603.09727.pdf)
7. [《Chinese Spelling Check System Based on Tri-gram Model》[Qiang Huang, 2014]](http://www.anthology.aclweb.org/W/W14/W14-6827.pdf)


----

# pycorrector
Chinese text error correction tool. 


**pycorrector** Use the language model to detect errors, pinyin feature and shape feature to correct chinese text 
error, it can be used for Chinese Pinyin and stroke input method.

## Features
### language model
* Kenlm
* RNNLM

## Usage

### install
* pip install pycorrector / pip3 install pycorrector 
* Or download https://github.com/shibing624/pycorrector, Unzip and run: python setup.py install

### correct  
input:
```
import pycorrector

corrected_sent, detail = pycorrector.correct('少先队员因该为老人让坐')
print(corrected_sent, detail)

```

output:
```
少先队员应该为老人让座 [[('因该', '应该', 4, 6)], [('坐', '座', 10, 11)]]
```


### Future work
1. P(c), the language model. We could create a better language model by collecting more data, and perhaps by using a 
little English morphology (such as adding "ility" or "able" to the end of a word).

2. P(w|c), the error model. So far, the error model has been trivial: the smaller the edit distance, the smaller the 
error.
Clearly we could use a better model of the cost of edits. get a corpus of spelling errors, and count how likely it is
to make each insertion, deletion, or alteration, given the surrounding characters. 

3. It turns out that in many cases it is difficult to make a decision based only on a single word. This is most 
obvious when there is a word that appears in the dictionary, but the test set says it should be corrected to another 
word anyway:
correction('where') => 'where' (123); expected 'were' (452)
We can't possibly know that correction('where') should be 'were' in at least one case, but should remain 'where' in 
other cases. But if the query had been correction('They where going') then it seems likely that "where" should be 
corrected to "were".

4. Finally, we could improve the implementation by making it much faster, without changing the results. We could 
re-implement in a compiled language rather than an interpreted one. We could cache the results of computations so 
that we don't have to repeat them multiple times. 
One word of advice: before attempting any speed optimizations, profile carefully to see where the time is actually 
going.


### Further Reading
* [Roger Mitton has a survey article on spell checking.](http://www.dcs.bbk.ac.uk/~roger/spellchecking.html)

# Reference
1. [Norvig’s spelling corrector](http://norvig.com/spell-correct.html)
2. [Norvig’s spelling corrector(java version)](http://raelcunha.com/spell-correct/)

