from gensim.models import Word2Vec
import json

# load word2vec model
model = Word2Vec.load("word2vec.model")

# the keywords we want
words = ['发展', '退潮', '稳定']

word_dict = {}
# find similar keywords
for word in words:
    word_dict[word]= []
    similar_words = model.wv.most_similar(word, topn=50)
    for similar_word, _ in similar_words:
        word_dict[word].append(similar_word)

with open('word_dict.json', 'w', encoding='utf-8') as f:
    json.dump(word_dict, f, ensure_ascii=False, indent=4)
