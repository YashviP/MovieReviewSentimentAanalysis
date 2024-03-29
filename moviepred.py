# IMDB Movie Review Sentiment Analysis 


import re
import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer



# STEP-1 - GETTING THE DATASET (download dataset and extract downloaded files from http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz)

# STEP-2 - PREPROCESSING

def clean_text(text):
	"""
	Applies some pre-processing on the given text.
	Steps :
	- Removing HTML tags
	- Removing punctuation
	- Lowering text

	"""
	# remove HTML tags
	text = re.sub(r'<.*?>', '', text)
    
	# remove the characters [\], ['] and ["]
	text = re.sub(r"\\", "", text)    
	text = re.sub(r"\'", "", text)    
	text = re.sub(r"\"", "", text)    

	# convert text to lowercase
	text = text.strip().lower()
    
	# replace punctuation characters with spaces
	filters='!"\'#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'
	translate_dict = dict((c, " ") for c in filters)
	translate_map = str.maketrans(translate_dict)
	text = text.translate(translate_map)

	return text



def load_train_test_imdb_data(data_dir):
	"""
	Loads the IMDB train/test datasets from a folder path.
	Input:
	data_dir: path to the "aclImdb" folder.
    	
	Returns:
	train/test datasets as pandas dataframes.
	"""

	data = {}
	for split in ["train", "test"]:
		data[split] = []
		for sentiment in ["neg", "pos"]:
			score = 1 if sentiment == "pos" else 0
			path = os.path.join(data_dir, split, sentiment)
			file_names = os.listdir(path)
			for f_name in file_names:
				with open(os.path.join(path, f_name), "r") as f:
					review = f.read()
					data[split].append([review, score])
	np.random.shuffle(data["train"])        
	data["train"] = pd.DataFrame(data["train"],columns=['text', 'sentiment'])

	np.random.shuffle(data["test"])
	data["test"] = pd.DataFrame(data["test"],columns=['text', 'sentiment'])
	
	return data["train"],data["test"]


train_data, test_data = load_train_test_imdb_data(data_dir="aclImdb/")

# STEP-3 - VECTORIZATION  
# METHOD 1- Bag of words model

# this vectorizer will skip stop words

vectorizer = CountVectorizer(
    stop_words="english",
    preprocessor=clean_text
)

# Transform each text into a vector of word counts
vectorizer = CountVectorizer(stop_words="english",
                             preprocessor=clean_text)

training_features = vectorizer.fit_transform(train_data["text"])    
test_features = vectorizer.transform(test_data["text"])

# Training
model = LinearSVC()
model.fit(training_features, train_data["sentiment"])
y_pred = model.predict(test_features)

# Evaluation
acc = accuracy_score(test_data["sentiment"], y_pred)

print("Accuracy on the IMDB dataset(using BOW): {:.2f}".format(acc*100))


#METHOD-2 - USING tf-idf 



# Transform each text into a vector of word counts
vectorizer = TfidfVectorizer(stop_words="english",
                             preprocessor=clean_text,
                             ngram_range=(1, 2))

training_features = vectorizer.fit_transform(train_data["text"])    
test_features = vectorizer.transform(test_data["text"])

# Training
model = LinearSVC()
model.fit(training_features, train_data["sentiment"])
y_pred = model.predict(test_features)

# Evaluation
acc = accuracy_score(test_data["sentiment"], y_pred)

print("Accuracy on the IMDB dataset(using tf-idf): {:.2f}".format(acc*100))









