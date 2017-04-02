#!/usr/bin/python
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import gensim
from gensim import corpora, models
import sqlite3 as lite
import sys
import re
import numpy as numpy
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt 
import numpy as np


class  LDA_Formulation:

	def __init__(self,database):
		self.db = database

	def connection(self):
		con = lite.connect(self.db)
		return con

	def corpusFormulation(self,con,filename):
		with con:
			reviewtext=""
			cur = con.cursor()
			cur.execute('SELECT review_text from Reviews_Businesses_Users')
			reviewrows = cur.fetchall()
			for review in reviewrows:
				reviewtext+=review[0]
			fo = open(filename,"a")	
			line = fo.write(reviewtext)
			fo.close()

	def corpusLDAUtil(self,sampletext,ntopics,nwords,file):
		p_stemmer = PorterStemmer()
		rawdata = sampletext.lower()
		tokens = tokenizer.tokenize(rawdata)
		en_stop = get_stop_words('en')
		stopped_tokens = [i for i in tokens if not i in en_stop]
		stemmed_token = [p_stemmer.stem(i) for i in stopped_tokens]
		texts = []
		texts.append(stemmed_token)
		dictionary = corpora.Dictionary(texts)
		corpus = [dictionary.doc2bow(text) for text in texts]

		ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=ntopics, id2word = dictionary,passes = 1)
		out = ldamodel.show_topics(num_topics=ntopics,num_words=nwords,log=False,formatted=False)
		print len(out)
		for i in range(0,len(out)):
			words_comma_seperated = ""
			eachtuple = out[i]
			#print val[1]
			tuplewords = eachtuple[1]
			for words_ in tuplewords:
				#print words_[0]
				words_comma_seperated=words_comma_seperated+words_[0]+","
			#print words_comma_seperated
			fo = open(file,"a")	
			line = fo.write(words_comma_seperated+"\n")
			fo.close()

	def corpusLDAUsers(self,user_id,sampletext,ntopics,nwords,file):
		p_stemmer = PorterStemmer()
		rawdata = sampletext.lower()
		tokens = tokenizer.tokenize(rawdata)
		en_stop = get_stop_words('en')
		stopped_tokens = [i for i in tokens if not i in en_stop]
		stemmed_token = [p_stemmer.stem(i) for i in stopped_tokens]
		texts = []
		texts.append(stemmed_token)
		dictionary = corpora.Dictionary(texts)
		corpus = [dictionary.doc2bow(text) for text in texts]

		ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=ntopics, id2word = dictionary,passes = 1)
		out = ldamodel.show_topics(num_topics=ntopics,num_words=nwords,log=False,formatted=False)
		#print out
		print len(out)
		words_comma_seperated = ""
		for i in range(0,len(out)):
			
			eachtuple = out[i]
			#print val[1]
			tuplewords = eachtuple[1]
			print len(tuplewords)
			for words_ in tuplewords:
				#print words_[0]
				words_comma_seperated=words_comma_seperated+words_[0]+","
		#print words_comma_seperated
		fo = open(file,"a")	
		line = fo.write(user_id+":"+words_comma_seperated+"\n")
		fo.close()

	def corpusLDA(self,filename,file):
		with open(filename) as f:
			content = f.read()
    		#print content
    		sampletext = content
    		self.corpusLDAUtil(sampletext,10,20,file)
    		

	def extractUserID(self,con):
		with con:
			cur = con.cursor()
			cur.execute('Create table if not exists user_id_details as select distinct user_id from Reviews_Businesses_Users')
			#print val
			con.commit()

	
	def userReviewLDA(self,con,file):
		with con:
			cur = con.cursor()
			cur.execute('SELECT user_id from user_id_details')
			rows = cur.fetchall()
			for row in rows:
				reviewtext = ""
				user_id = row[0]
				print user_id
				#id = str("WKIW7tWyMq7_XN0V2ouo0A")
				cur.execute('SELECT review_text from Reviews_Businesses_Users where user_id = :id',{"id":user_id})
				reviewrows = cur.fetchall()
				for review in reviewrows:
					reviewtext+=review[0]
				self.corpusLDAUsers(user_id,reviewtext,1,20,file)

				
	#user as rows and topics as columns			
	def readUserTopics(self,file,trainingfile,topics):
		data = []
		User_list=[]

		for line in open(file):
			#print line
			data.append(tuple(line.strip().split(':')))
		#iterating users
		print data
		rows = len(data)
		cols = topics#topics
		#print len(data)
		lda_user=[]
		Adj_matrix =[[0 for x in range(cols)]for y in range(rows)]
		userindex=0
		for usertext in data:
			User_list.append(usertext[0])
			print usertext[1]
			lda_user = str(usertext[1])
			#print lda_user+"\n"
			lda_user =lda_user.split(',')
			
			for i in range(0,len(lda_user)):
				everyword = lda_user[i]
				#print everyword
				topicindex=0
				for linetopic in open(trainingfile):
					#print everyword
					#print linetopic
					if everyword in linetopic:
						print everyword
						print "\n"
						print linetopic
						print topicindex
						Adj_matrix[userindex][topicindex]+=1
					topicindex+=1
			userindex+=1
		#Adj_matrix /= topics
		print userindex
		print topicindex
		print Adj_matrix
		return User_list,Adj_matrix

#			print "\n\n\n"


		#print data


	def scatter_plot(self,Adj_matrix):
		plt.plot(Adj_matrix)
		plt.show()


	def Kmeans_Transform(self,cluster,file,User_list,Adj_matrix):
		kmeans = KMeans(n_clusters=cluster,random_state=0).fit(Adj_matrix)
		labels = kmeans.labels_
		centroid = kmeans.cluster_centers_
		print labels
		print centroid
		fo = open(file,"a")
		for i in range(len(Adj_matrix)):
			print User_list[i] ,":" ,Adj_matrix[i] , ":" , labels[i] ,"\n"
			line = fo.write(str(User_list[i])+":"+str(Adj_matrix[i])+":"+str(labels[i])+"\n")
		fo.close()
			



model = LDA_Formulation("smlProject_v2_usr(str-4,fans-50,review_count-50)_business(review_count-5).db")
conn = model.connection()
print conn

#model.corpusFormulation(conn,"CorpusData.txt")
#model.corpusLDA("CorpusData.txt","OUTPUT_FILE.txt")
#model.extractUserID(conn)
#model.userReviewLDA(conn,"User_Topic.txt")
User_list,Adjacency_matrix = model.readUserTopics("User_Topic.txt","OUTPUT_FILE.txt",10)
print len(User_list)
print len(Adjacency_matrix)
#model.scatter_plot(Adjacency_matrix)
model.Kmeans_Transform(5,"Kmeans.txt",User_list,Adjacency_matrix)
