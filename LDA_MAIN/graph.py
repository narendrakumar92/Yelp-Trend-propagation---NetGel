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

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt 
import numpy as np


class  graph:

	def __init__(self,database):
		self.db = database

	def connection(self):
		con = lite.connect(self.db)
		return con

	def matrix_FriendsList(self,con,filename,filenameadj):
		with con:
			user_list = []
			cur = con.cursor()
			cur.execute('SELECT distinct user_id,user_friends from Reviews_Businesses_Users')
			userdata = cur.fetchall()

			
			print len(user_list)

			print len(userdata)
			rows=len(userdata)
			cols=len(userdata)
			Adj_matrix =[[0 for x in range(cols)]for y in range(rows)]
			
			#fo = open(filename,"a")
			userindex=0
			fo = open(filename,"a")
			for data in userdata:
				userId = data[0]
				user_list.append(userId)	
			

			for data in userdata:
				userId = data[0]
				friendsList = data[1]
				list = friendsList.split()
				#print list[0]+"\n\n\n"
				line = fo.write(userId+":")
				for i in range(0,len(list)):
					s = list[i].replace(",","")
					s = s.replace("'","")
					s = s.replace("[","")
					str = s.replace("]","")
					if str in user_list:
						#print str
						colindex = user_list.index(str)
						print colindex
						Adj_matrix[userindex][colindex]=1
					line = fo.write(str+",")
				userindex+=1
				line = fo.write("\n")
			fo.close()
			print Adj_matrix
			npar = np.array(Adj_matrix)
			np.savetxt('Adjacency.out',npar,fmt='%d')
			userlist_npar = np.array(user_list)
			np.savetxt('user_list.out',userlist_npar,fmt='%s')
	


	def similarityComputation(self,con):
		
		nparr = np.loadtxt('Adjacency.out',dtype=int)
		adj_matrix = nparr.tolist()
		#print adj_matrix
		npar = np.loadtxt('User_id_adj.out',dtype=int)
		user_matrix = npar.tolist()
		#print user_matrix
		user_list_npar = np.loadtxt('user_list.out',dtype=str)
		user_id = user_list_npar.tolist()
		#print user_id
		user_id_val=[]
		review_count=[]
		with con:
			cur = con.cursor()
			cur.execute('SELECT user_id,user_review_count from Reviews_Businesses_Users group by user_id')
			rows = cur.fetchall()
			for row in rows:
				#print row[0]
				#print row[1]
				user_id_val.append(row[0])
				review_count.append(row[1])
			#print review_count
			rows = len(user_id_val)
			cols = len(user_id_val)
			Adj_matrix_weighted =[[0 for x in range(cols)]for y in range(rows)]
			topiciterator=0
			for topiciterator in range (0,10):
				for i in range(0,len(adj_matrix)):
					reviewcnt=0#normalization
					r = adj_matrix[i]
					#print len(r)
					for j in range(0,len(r)):
						#print adj_matrix[i][j]
						if(adj_matrix[i][j]==1):
							#print j
							reviewcnt+=review_count[j]
							
							friendsreviewcount=reviewcnt
							userreviewcount = review_count[j] #change made, its sj not si
							#outliers , if friends posted no reviews
							if friendsreviewcount == 0:
								friendsreviewcount  =userreviewcount
					
							sim = self.simweight(i,j,user_matrix,topiciterator)
							PIJ = (userreviewcount/float(friendsreviewcount))*sim
							#print str(userreviewcount)+ ":" +str(friendsreviewcount) +":"+str(PIJ)
							#if userreviewcount>friendsreviewcount:
								#print str(userreviewcount)+ ":" +str(friendsreviewcount)
							if PIJ>1:
								print "ERR"
							Adj_matrix_weighted[i][j] = PIJ
				#print Adj_matrix_weighted
				filename_T = "Adjacency_T"+str(topiciterator)
				npar_T = np.array(Adj_matrix_weighted)
				np.savetxt(filename_T,npar_T,fmt='%f')
				

	def simweight(self,i,j,user_matrix,topiciterator):
		user_mat1 = user_matrix[i]
		user_mat2 = user_matrix[j]
		sum=0
		for i in range (0,len(user_mat1)):
			sum+=user_mat1[i]
		normalizedDTIT = user_mat1[topiciterator]/sum

		sum=0
		for i in range (0,len(user_mat2)):
			sum+=user_mat2[i]
		normalizedDTJT = user_mat2[topiciterator]/sum

		simcal = 1 - abs(normalizedDTIT-normalizedDTJT)
		if simcal>1:
			print "greater"
		return simcal

			









			


graph = graph("smlProject_v2_usr(str-4,fans-50,review_count-50)_business(review_count-5).db")
conn = graph.connection()
#graph.matrix_FriendsList(conn,"Graphfriends.txt","Adj_matrix.txt")
#print conn
graph.similarityComputation(conn)