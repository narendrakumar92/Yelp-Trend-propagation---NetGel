from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import gensim
from gensim import corpora, models
import sqlite3 as lite
import sys
import re

con = lite.connect('smlProject_v2_usr(str-4,fans-50,review_count-50)_business(review_count-5).db')
with con:
	cur = con.cursor()
	reviewtext = ""
	cur.execute('Select Count(*) from Reviews_Businesses_Users ')
	val = cur.fetchone()
	cur.execute('Create table if not exists user_id_details as select distinct user_id from Reviews_Businesses_Users')
	#print val
	con.commit()
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
		#reviewtext = reviewtext.strip()
		#print reviewtext
		sampletext = reviewtext

		p_stemmer = PorterStemmer()

		rawdata = sampletext.lower()
		tokens = tokenizer.tokenize(rawdata)
		en_stop = get_stop_words('en')
		stopped_tokens = [i for i in tokens if not i in en_stop]
		#print stopped_tokens

		#To remove all the tensed words into normal form
		stemmed_token = [p_stemmer.stem(i) for i in stopped_tokens]
		#print stemmed_token

		texts = []
		texts.append(stemmed_token)
		#print texts

		dictionary = corpora.Dictionary(texts)
		corpus = [dictionary.doc2bow(text) for text in texts]

		#print dictionary.token2id
		#print corpus[0]

		#Applying LDA model

		ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=1, id2word = dictionary,passes = 1)

		#passes - no of iteration
		out = ldamodel.show_topics(num_topics=1,num_words=10,log=False,formatted=False)
		#print out
		#print len(out)
		words_comma_seperated = ""
		for i in range(0,len(out)):

			eachtuple = out[i]
			#print val[1]
			tuplewords = eachtuple[1]
			for words_ in tuplewords:
				#print words_[0]
				words_comma_seperated=words_comma_seperated+words_[0]+","
			print words_comma_seperated



		fo = open("newoutput.txt","a")	
		line = fo.write(user_id+";"+words_comma_seperated+"\n")
		fo.close()


