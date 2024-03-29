import gensim
from gensim.models import Word2Vec, Phrases
import jieba
import json
import os
import logging
import csv

# load word dict
with open('./word_dict.json', 'r', encoding='utf-8') as f:
    word_dict = json.load(f)

dirname =  './mdatxts'

# csv headline
data = [['name', 'year', '发展', '稳定', '退潮'], ]

for fname in os.listdir(dirname):
    for line in open(os.path.join(dirname, fname), encoding='utf-8'):
        # get basic information of the file
        sentence = jieba.lcut(line.strip())
        company_name = fname.split('_')[0]
        year = fname.split('_')[1]
        one_data = [company_name, year]
        word_count = 0
        
        # count the number of these keywords' appearence 
        for word in list(word_dict.keys()):
            for keyword in word_dict[word]:
                word_count += sentence.count(keyword)
            one_data.append(word_count)
            word_count = 0
        data.append(one_data)


with open('./data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(data)



