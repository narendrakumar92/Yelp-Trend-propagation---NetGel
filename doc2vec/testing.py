import gensim
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
import sqlite3 as lite
from sklearn.cluster import KMeans

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

model = gensim.models.Doc2Vec(size=300, window=10, min_count=5, workers=11,alpha=0.025, min_alpha=0.025) # use fixed learning rate
model = gensim.models.Doc2Vec.load("doc2vec.model")

vec = []
for user in user_id:
    vec.append(model.docvecs[user])

print model.most_similar('pork')


def Kmeans_Transform(cluster,file,User_list,vec):
        kmeans = KMeans(n_clusters=cluster,random_state=0).fit(vec)
        labels = kmeans.labels_
        centroid = kmeans.cluster_centers_
        print labels
        print centroid
        fo = open(file,"w")
        for i in range(len(vec)):
            # print i, User_list[i] ,":" ,vec[i] , ":" , labels[i] ,"\n"
            line = fo.write(str(labels[i])+"\n")
        fo.close()

Kmeans_Transform(5,"Doc2Vec_Kmeans.txt",user_id,vec)
