from os import listdir
import gensim
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
import sqlite3 as lite
import re

LabeledSentence = gensim.models.doc2vec.LabeledSentence

#per user review data
con = lite.connect('smlProject_v2_usr(str-4,fans-50,review_count-50)_business(review_count-5).db')
def extractUserID(con):
    with con:
        cur = con.cursor()
        cur.execute('Create table if not exists user_id_details as select distinct user_id from Reviews_Businesses_Users')
        #print val
        con.commit()
extractUserID(con)
i = 1
with con:
    cur = con.cursor()
    cur.execute('SELECT user_id from user_id_details')
    rows = cur.fetchall()
    for row in rows:
        i += 1
        reviewtext = ""
        user_id = row[0]
        print "User ID:"+user_id
        id = str("WKIW7tWyMq7_XN0V2ouo0A")
        cur.execute('SELECT review_text from Reviews_Businesses_Users where user_id = :id',{"id":user_id})
        reviewrows = cur.fetchall()
        for review in reviewrows:
            reviewtext+=re.sub('[^A-Za-z0-9\']+', ' ', review[0])
        reviewtext = reviewtext.split()
        sent = LabeledSentence(words=reviewtext,tags=[user_id])
        break

it = [sent]
print it
model = gensim.models.Doc2Vec(size=300, window=1, min_count=1, workers=11,alpha=0.025, min_alpha=0.025) # use fixed learning rate
model.build_vocab(it)
for epoch in range(10):
    model.train(it)
    model.alpha -= 0.002 # decrease the learning rate
    model.min_alpha = model.alpha # fix the learning rate, no deca
    model.train(it)
model.save("doc2vec.model")
print "Doc vectors of dimension 50:"
print model.docvecs[u'GABWrw5Et9jubriKwMUDbw'] #name of the userreviewdoc; returns vector for each document

