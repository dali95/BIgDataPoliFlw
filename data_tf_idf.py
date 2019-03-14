__author__ = 'Dennis Strik'

from functools import reduce
import os
import glob
import re
import math
import ijson
import re
from textblob import TextBlob as tb

counter = 0

with open("articles.csv", "w") as my_empty_csv:
  # now you have an empty file already
  pass

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

stop_words =()

with open("/home/dali/Downloads/stopwoorden.txt", "r") as f:
    i = 0
    tmpList = []
    for line in f:
        i +=1
        tmp = (' '+line.rstrip()+ ' ', ' ')
        tmpList.append(tmp)

stop_words = (tmpList)

bloblist = []


f = open("/home/dali/Downloads/complete-dump.json")
objs = ijson.items(f, '')
for item in ijson.items(f, "item"):

    try:
        art_text = item['_source']['description']
        re.sub('\s+',' ',art_text)

        art_text = (re.sub(r'[^\x00-\x7F]+', ' ', art_text))

        clean_text = re.sub("(<img.*?>)", "", art_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<div class.*?>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<div id.*?>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<a href.*?>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#160;)", " ", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#8364;)", "€", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#233;)", "é", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#8217;)", "’", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#243;)", "ó", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#239;)", "ï", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#235;)", "ë", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#8216;)", "‘", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#8220;)", "“", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#8221;)", "”", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#226;)", "â", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<h6>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(</h6>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(</a>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<div>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(</div>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<p>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<em>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<li>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(</li>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<pi>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(</pi>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&nbsp;)", " ", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<strong>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(</strong>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<br />)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&euml;)", "Ë", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&hellip;)", "…", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&rsquo;)", "’", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&ldquo)", "“", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&rdquo;)", "”", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&iuml;)", "Ï", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(ul>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&eacute;)", "é", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&aacute;)", "Á", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&hellip;)", "…", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&quot;)", "''", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&oacute;)", "Ó", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&uuml:)", "	Ü", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#039:)", "'", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&euml;)", "Ë", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&uacute;)", "Ú", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&ouml;)", "Ö", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&acute;)", "´", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#13;)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(</p>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<br/)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<br>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(</span>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<b>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(</b>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<ol>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(</ol>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("</em>", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<h3>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(</h3>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<h2>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(</h2>)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    #  clean_data = re.sub("()", "", clean_data, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(</)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(<)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#8211;)", "–", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&amp;)", "&", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#8230;)", "…", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#232;)", "è", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#199;)", "Ç", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&amp;)", "&", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#263;)", "ć", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#224)", "à", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#246;)", "ö", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#8230)", "…", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#8223)", "‟", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&lt;)", "<", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(/&gt)", ">", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#8212;)", "—", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#236;)", "ì", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#242;)", "ò", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(!--*-->)", "", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&#039;)", "'", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&reg;)", "®", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&ndash;)", "–", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&euro;)", "€", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&lsquo;)", "‘", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = re.sub("(&uuml;)", "Ü", clean_text, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        clean_text = clean_text.lower()
    except KeyError:
        Bool = False
        pass



    try:
        art_id = item['_id']
    except KeyError:
        pass

    try:
        art_source = item['_source']['source']
    except KeyError:
        art_source = 'Niet bekend'
        pass

    try:
        art_date = item['_source']['date']
    except KeyError:
        art_date = 'Geen datum'
        pass

    try:
        art_title = item['_source']['title']
    except KeyError:
        art_title = 'Geen titel'
        pass


    print(counter)
    counter +=1

    # print(art_id)
    # print(art_title)
    # print(art_date)
    # print(art_source)
    # print(clean_text)
    #
    #
    # print('----------------------------')

    clean_text = clean_text.replace('\r', '').replace('\n', '')
    clean_text = clean_text.replace(';', ' ').replace('\t', '')



    #print(clean_text)
    art_id = (re.sub(r'[^\x00-\x7F]+', ' ', art_id))
    art_title = (re.sub(r'[^\x00-\x7F]+', ' ', art_title))
    art_date = (re.sub(r'[^\x00-\x7F]+', ' ', art_date))
    art_source = (re.sub(r'[^\x00-\x7F]+', ' ', art_source))

    if len(clean_text) > 150:
        with open('articles.csv','a', encoding="utf-8") as fd:
            fd.write(art_id + ';' + art_title + ';' + art_date + ';' + art_source + ';' + clean_text + '\n')

    # data = re.sub(r"[^a-zA-Z0-9]+", ' ', clean_text)
    # #remove special characters
    #
    # data = reduce(lambda a, kv: a.replace(*kv), stop_words, data)
    # data = re.sub(r'[0-9]+', '', data)


    # text = tb(data)
    #
    # bloblist.append(text)




        # document = tb(test.read())
        # counter2 = 0
        # while counter2 <3:
        #     print(document)
        #
        # while counter < 3:
        #     bloblist.append(document)
        #     counter +=1

#print(len(blobList))


# for i, blob in enumerate(bloblist):
#     print("Top words in document {}:".format(i + 1))
#     scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
#     sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#     for word, score in sorted_words[:10]:
#         print("\t{}, TF-IDF: {}".format(word, round(score, 5)))
