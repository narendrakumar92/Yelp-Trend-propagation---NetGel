#per user review data
import sqlite3 as lite
import re
import gensim
LabeledSentence = gensim.models.doc2vec.LabeledSentence

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
        print user_id
        id = str("WKIW7tWyMq7_XN0V2ouo0A")
        cur.execute('SELECT review_text from Reviews_Businesses_Users where user_id = :id',{"id":user_id})
        reviewrows = cur.fetchall()
        for review in reviewrows:
            reviewtext+=re.sub('[^A-Za-z0-9\']+', ' ', review[0])
        reviewtext = reviewtext.lower().split()
        sent = LabeledSentence(words=reviewtext,tags=[user_id])
        break
