import nltk
nltk.download('punkt')
from functools import reduce
import math
import re
from textblob import TextBlob as tb
from models import *
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
connect("BigData_art", host="localhost", port=27017)

db = client.BigData_art

with open("/home/dali/Downloads/stopwoorden.txt", "r") as f:
    i = 0
    tmpList = []
    for line in f:
        i +=1
        tmp = (' '+line.rstrip()+ ' ', ' ')
        tmpList.append(tmp)

stop_words = (tmpList)

bloblist = []
counter = 0

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

url = "/home/dali/BDTFIDF/articles.csv"
file = open(url, "r", encoding="utf8")

count = 0
for lines in range(1000):
    line = file.readline()
    counts = line.count(';')
    if counts <= 4:
        id, titel, date, author, text = line.split(";")
        print(line)
        data = re.sub(r"[^a-zA-Z0-9]+", ' ', line)
        #remove special characters
        data = reduce(lambda a, kv: a.replace(*kv), stop_words, data)
        data = re.sub(r'[0-9]+', '', data)
        bloblist.append(tb(data.lower()))

    ak = Artikel()
    ak.ID = id
    ak.Title = titel
    ak.Date = date
    ak.Source = 'Test'
    ak.Text = text
    ak.save


    #Controle of er al een artikel is in de DB met deze id of titel
    #Hierzo het artikel in de DB gooien nog

for i, blob in enumerate(bloblist):
    tmp = []
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:5]:
        TF_IDF_str = word + ':' + str(score)
        tmp.append(TF_IDF_str)

    TI = TF_IDF()
    TI.ID = id
    title = titel
    TI.TF_IDF1 = tmp[0]
    TI.TF_IDF2 = tmp[1]
    TI.TF_IDF3 = tmp[2]
    TI.TF_IDF4 = tmp[3]
    TI.TF_IDF5 = tmp[4]
    TI.save()

# for i, string in line:

#



