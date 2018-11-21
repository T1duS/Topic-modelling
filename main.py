import nltk
from nltk.tokenize import word_tokenize
import string
from nltk.corpus import stopwords
from collections import Counter
import os
import sys
from math import log10

stop_words = stopwords.words('english')
stop_words.sort()

def bsearch(word):
	low = 0
	high = len(stop_words)-1
	while low <= high:
		mid = (low+high)//2
		if word == stop_words[mid]:
			return True
		elif word < stop_words[mid]:
			high = mid-1
		else:
			low = mid+1
	return False			

def clean_text(text):
	# part of the code taken from 
	# https://machinelearningmastery.com/clean-text-machine-learning-python/
	tokens = word_tokenize(text)
	table = str.maketrans('', '', string.punctuation)
	stripped = [w.translate(table) for w in tokens]
	words = [word.lower() for word in tokens if word.isalpha()]
	# Using binary search to see if word is not a stop word 
	# since the corpus is large and would take a lot of time otherwise
	words = [w for w in words if (not bsearch(w))] 
	return dict(Counter(words))

def preprocess():
	global corpus_freq
	global total
	if not os.path.exists('freq_data.txt'):
		corpus_file = open('corpus.txt', 'rt')
		with open("freq_data.txt", "w") as data_file:
			corpus_freq = clean_text(corpus_file.read())
			data_file.write(str(corpus_freq))
		corpus_file.close()
	else:
		with open("freq_data.txt", "r") as data_file:
			corpus_freq = eval(data_file.read())
	total = sum(corpus_freq.values())		

if __name__ == '__main__':
	
	preprocess()

	if len(sys.argv) < 2:
		print("Missing file name")
		exit()

	inpy = open(sys.argv[1], "r")
	doc_freq = clean_text(inpy.read())
	inpy.close()

	tfidf = []

	for i in doc_freq:
		tfidf.append([doc_freq[i]*log10(total/(corpus_freq[i]+1)),i])

	tfidf.sort(reverse = True)

	print("Possible topics are ---")
	for i in range(10):
		print(tfidf[i][1])
