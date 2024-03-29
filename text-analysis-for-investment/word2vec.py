from gensim.models import Word2Vec, Phrases
import jieba
import os
import logging

# config log
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# load text data
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname), encoding='utf-8'):
                yield jieba.lcut(line.strip())

sentences = MySentences('./mdatxts') 
# bigram_transformer = Phrases(sentences)
 
# train the model
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=8)

# save the model
model.save("word2vec.model")

