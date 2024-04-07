import nltk
nltk.download("stopwords")
nltk.download("wordnet")
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
import json
import pandas as pd
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
import dill as pickle
import kfold_template


review_stars = []
review_text = []


with open("dataset.csv", encoding="utf-8") as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        review_stars.append(row["stars"])
        review_text.append(row["reviewtext"])

dataset = pd.DataFrame(data={"text": review_text, "stars": review_stars})

#dataset = dataset.iloc[0:]

dataset = dataset[(dataset['stars'] == '1') | (dataset['stars'] == '2') | (dataset['stars'] == '3')]

print(dataset)

data = dataset["text"]
target = dataset["stars"]

lemmatizer = WordNetLemmatizer()

def pre_processing(text):
  text_processed = text.translate(str.maketrans("","", string.punctuation))
  text_processed = text_processed.split()
  result = []
  for word in text_processed:
    word_processed = word.lower()
    if word_processed not in stopwords.words("english"):
      word_processed = lemmatizer.lemmatize(word_processed)
      result.append(word_processed)
  return result
  
count_vectorize_transformer = CountVectorizer(analyzer=pre_processing).fit(data)

data = count_vectorize_transformer.transform(data)

machine = RandomForestClassifier(criterion="gini", max_depth=10,n_estimators=11)
#validation with kfold_template
return_values=kfold_template.run_kfold(machine, data, target, 4, True)
print(return_values)

machine = RandomForestClassifier(criterion="gini", max_depth=10,n_estimators=11)
machine.fit(data,target)


with open("text_analysis_machine_random_forest.pickle", "wb") as f:
  pickle.dump(machine, f)
  pickle.dump(count_vectorize_transformer, f)
  pickle.dump(lemmatizer, f)
  pickle.dump(stopwords, f)
  pickle.dump(string, f)
  pickle.dump(pre_processing, f)
  