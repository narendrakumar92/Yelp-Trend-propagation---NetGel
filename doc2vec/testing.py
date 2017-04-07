import gensim
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
import sqlite3 as lite
import re
user_id = []
rows = []
con = lite.connect('smlProject_v2_usr(str-4,fans-50,review_count-50)_business(review_count-5).db')
def extractUserID(con):
    with con:
        cur = con.cursor()
        cur.execute('Create table if not exists user_id_details as select distinct user_id from Reviews_Businesses_Users')
        #print val
        con.commit()
        cur.execute('SELECT user_id from user_id_details')
        rows = cur.fetchall()
        cur.execute('SELECT user_id from user_id_details')
        rows = cur.fetchall()
        for row in rows:
            user_id.append(row[0])
        return user_id
user_id = extractUserID(con)
print user_id[300]
model = gensim.models.Doc2Vec(size=300, window=10, min_count=5, workers=11,alpha=0.025, min_alpha=0.025) # use fixed learning rate
model = gensim.models.Doc2Vec.load("doc2vec.model")
print model.docvecs[user_id[300]]
print model.docvecs.most_similar(user_id[300])
