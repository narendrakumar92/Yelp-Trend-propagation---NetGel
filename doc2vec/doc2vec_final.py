from os import listdir
import gensim
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
import sqlite3 as lite
import re
import stop_words_yelp
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words

stop_word_list = stop_words_yelp.stop_word_list
# p_stemmer = PorterStemmer()
LabeledSentence = gensim.models.doc2vec.LabeledSentence
it = []

#per user review data
con = lite.connect('smlProject_v2_usr(str-4,fans-50,review_count-50)_business(review_count-5).db')

def extractUserID(con):
    with con:
        cur = con.cursor()
        cur.execute('Create table if not exists user_id_details as select distinct user_id from Reviews_Businesses_Users')
        #print val
        con.commit()
        cur.execute('SELECT user_id from user_id_details')
        rows = cur.fetchall()
        for row in rows:
            user_id.append(row[0])
        return user_id

def user_doc():
    i = 0
    users = []
    with con:
        cur = con.cursor()
        cur.execute('SELECT user_id from user_id_details')
        rows = cur.fetchall()
        for row in rows:
            i += 1
            reviewtext = ""
            users.append(row[0])
            user_id = row[0]
            print "No."+str(i)+" User ID:"+user_id
            cur.execute('SELECT review_text from Reviews_Businesses_Users where user_id = :id',{"id":user_id})
            reviewrows = cur.fetchall()
            for review in reviewrows:
                reviewtext+=re.sub('[^A-Za-z0-9\']+', ' ', review[0])
            reviewtext = reviewtext.split()
            en_stop = get_stop_words('en')
            stopped_tokens = [j.lower() for j in reviewtext if not j in en_stop]
            # stemmed_token = [p_stemmer.stem(i) for i in stopped_tokens]
            # vocab_list = [word.lower().strip() for word in stopped_tokens if (word.lower().strip() + ' ' not in stop_word_list)]
            # print stopped_tokens
            sent = LabeledSentence(words=stopped_tokens,tags=[user_id])
            it.append(sent)
        # if(i == 2):
        # break
        return it

def model():
    model = gensim.models.Doc2Vec(min_count=5, window=5, size=100, sample=1e-4, negative=5, workers=8) # use fixed learning rate
    model.build_vocab(user_doc())
    for epoch in range(10):
        print epoch
        model.train(it)
        model.alpha -= 0.002 # decrease the learning rate
        model.min_alpha = model.alpha # fix the learning rate, no deca
        model.train(it)
    model.save("doc2vec-full.model")
    # print "Doc vectors of dimension 50:"
    # print model.docvecs[users[40]].__len__() #name of the userreviewdoc; returns vector for each document
    # print model.docvecs.most_similar(users[2])
    # print model.most_similar('tacos')

def user_vectors(user_id):
    model = gensim.models.Doc2Vec.load("doc2vec.model")
    vec = []
    for user in user_id:
        vec.append(model.docvecs[user])
    return vec
    #print model.docvecs[user_id[40]] #name of the userreviewdoc; returns vector for each document
    #print model.docvecs.most_similar(u'HduHfYjJUFjQUrrQ1Ets-A')
    #print model.docvecs.similarity(u'HduHfYjJUFjQUrrQ1Ets-A', u'VatcQtdb5tlz4D-N6y8e7A')

def Kmeans_Transform(cluster,file,user_id,vec):
        s = ""
        clusdict = dict()
        for i in range(5):
            clusdict[i] = []
        kmeans = KMeans(n_clusters=cluster,random_state=0).fit(vec)
        labels = kmeans.labels_
        centroid = kmeans.cluster_centers_
        fo = open(file,"w")
        for i in range(len(vec)):
            s = user_id[i] + " " + str(labels[i]) + "\n"
            clusdict[labels[i]].append(user_id)
            # print str
            fo.write(s)
        fo.close()
        for keys in clusdict:
            print len(clusdict[keys])

if __name__ == '__main__':
    user_id = extractUserID(con)
    model()
    vec = user_vectors(user_id)
    Kmeans_Transform(5,"Doc2Vec_Kmeans.txt",user_id,vec)z
