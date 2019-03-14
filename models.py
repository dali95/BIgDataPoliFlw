from mongoengine import *

class Artikel(Document):
    ID = StringField()
    Title = StringField()
    Date = DateTimeField()
    Source = StringField()
    Text = StringField()

class TF_IDF(Document):
    ID = StringField()
    Title = StringField()
    TF_IDF1 = StringField()
    TF_IDF2 = StringField()
    TF_IDF3 = StringField()
    TF_IDF4 = StringField()
    TF_IDF5 = StringField()
