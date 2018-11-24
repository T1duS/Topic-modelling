import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import string
from nltk.corpus import stopwords
from collections import Counter
import os
import sys
from math import log10, sqrt

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

def preprocess(restart=False):
	global corpus_freq
	global total
	if (not os.path.exists('freq_data.txt')) or restart:
		corpus_file = open('corpus.txt', 'rt')
		with open("freq_data.txt", "w") as data_file:
			corpus_freq = clean_text(corpus_file.read())
			data_file.write(str(corpus_freq))
		corpus_file.close()
	else:
		with open("freq_data.txt", "r") as data_file:
			corpus_freq = eval(data_file.read())
	total = sum(corpus_freq.values())		

def cos_similarity(d1, d2):
	dotprod = mod_d1 = mod_d2 = 0
	for i in d1:
		if i in d2:
			dotprod += d1[i]*d2[i]
	for i in d1:
		mod_d1 += d1[i]*d1[i]
	for i in d2:
		mod_d2 += d2[i]*d2[i]
	mod_d1 = sqrt(mod_d1)
	mod_d2 = sqrt(mod_d2)	
	return dotprod/(mod_d1*mod_d2)

if __name__ == '__main__':
	

	if len(sys.argv) > 2 and sys.argv[2] == "-R":
		preprocess(True)
	else:
		preprocess()	

	if len(sys.argv) < 2:
		print("Missing file name")
		exit()

	inpy = open(sys.argv[1], "r")
	file_text = inpy.read()
	doc_freq = clean_text(file_text)
	sentences = sent_tokenize(file_text)
	inpy.close()

	tfidf = {}

	for i in doc_freq:
		tfidf[i] = doc_freq[i]*log10(total/(corpus_freq.get(i,0)+1))

	tfidfsent = []

	for sent in sentences:
		cleansent = clean_text(sent)
		vec = {}
		for i in cleansent:
			vec[i] = tfidf[i] 
		tfidfsent.append(vec)

	tfidfsent = [i for i in tfidfsent if i]
	
	n = len(tfidfsent)
	score = [0]*(n+1)		
	for i in range(n):
		for j in range(i+1,n):
			similar = cos_similarity(tfidfsent[i],tfidfsent[j])
			score[i] += similar
			score[j] += similar

	mx = score[0]
	sent = sentences[0]
	for i in range(1,n):
		if score[i] > mx:
			mx = score[i]
			sent = sentences[i]

	print(sent)					
