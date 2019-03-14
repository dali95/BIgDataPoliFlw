from difflib import SequenceMatcher
import nltk
nltk.download('punkt')
from models import *
from pymongo import MongoClient

def similar(a, b):
    s =  SequenceMatcher(None, a, b)
    return s.ratio()

artikel = {}
new_term = ''
tf_highest = ''


client = MongoClient('localhost', 27017)
connect("BigData_art", host="localhost", port=27017)
db = client.BigData_art
tf_idf_collection = db.t_f__i_d_f


term = 'zuiderzee'



def Search(term):
    terms = []
    for doc in tf_idf_collection.find():
        i = 1
        while i < 6:
                tf_loc = 'TF_IDF' + str(i)
                tf_idf_term = doc[tf_loc].split(':')[0]
                sim = similar(tf_idf_term,term)
                i = i+1
                if sim > 0.65:
                    terms.append(doc)
    return terms

results = Search(term)
print(results)