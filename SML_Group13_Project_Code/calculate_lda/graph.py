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
from random import randint

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt 
import numpy as np
import string

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

			
			#print len(user_list)

			remove_index = [3,2,8,34,9,1,4,10,12,14,60,5,11,63,21,7,13,61,15,123]
			
			#print len(userdata)
			
			#fo = open(filename,"a")
			userindex=0
			fo = open(filename,"a")
			for data in userdata:
				userId = data[0]
				if userdata.index(data) not in remove_index: 
					user_list.append(userId)	

			rows=len(user_list)
			cols=len(user_list)
			Adj_matrix =[[0 for x in range(cols)]for y in range(rows)]
			

			print len(user_list)
			

			for data in userdata:
				if userdata.index(data) not in remove_index:
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
							#print colindex
							Adj_matrix[userindex][colindex]=1
						line = fo.write(str+",")
					userindex+=1
					line = fo.write("\n")
			fo.close()
			print Adj_matrix
			npar = np.array(Adj_matrix)
			np.savetxt('Adjacency_new.out',npar,fmt='%d')
			userlist_npar = np.array(user_list)
			np.savetxt('user_list.out',userlist_npar,fmt='%s')
	


	def similarityComputation(self,con):
		
		nparr = np.loadtxt('Adjacency_new.out',dtype=int)
		adj_matrix = nparr.tolist()
		#print adj_matrix
		npar = np.loadtxt('User_id_adj_ravi.out',dtype=int)
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
			remove_index = [3,2,8,34,9,1,4,10,12,14,60,5,11,63,21,7,13,61,15,123]
			
			for row in rows:
				#print row[0]
				#print row[1]
				if rows.index(row) not in remove_index:
					user_id_val.append(row[0])
					review_count.append(row[1])
				#print review_count
			rows = len(user_id_val)
			cols = len(user_id_val)
			topiciterator=0
			for topiciterator in range (0,10):
				Adj_matrix_weighted =[[0 for x in range(cols)]for y in range(rows)]
				#user iteration
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
							#PIJ = int(PIJ*1000)
							Adj_matrix_weighted[i][j] = PIJ
							x=i
							y=j
				print PIJ
				print i 
				print j
							
				#print Adj_matrix_weighted
				filename_T = "Adjacency_T"+str(topiciterator)
				npar_T = np.array(Adj_matrix_weighted)
				np.savetxt(filename_T,npar_T,fmt='%f')
				print "\n"
				

	def simweight(self,i,j,user_matrix,topiciterator):
		#print topiciterator
		user_mat1 = user_matrix[i]
		user_mat2 = user_matrix[j]
		sum=0
		for i in range (0,len(user_mat1)):
			sum+=user_mat1[i]
		normalizedDTIT = user_mat1[topiciterator]/(sum*1.0)
		#print user_mat1[topiciterator]
		sum=0
		for i in range (0,len(user_mat2)):
			sum+=user_mat2[i]
		normalizedDTJT = user_mat2[topiciterator]/(sum*1.0)

		#print normalizedDTJT 
		#print normalizedDTIT
		#print "\n"
		simcal = 1 - (abs(normalizedDTIT-normalizedDTJT))
		if simcal>1:
			print "greater"
		if simcal<0:
			print "lesser"
		return simcal

	def Kmeans_clusterSeparate(self,filename,cluster_size):
		data = []
		for line in open(filename):
			data.append(tuple(line.strip().split(':')))

		for i in range (0,cluster_size):
			cluster_data =[]
			index_val = []
			count_index=0
			for rowdata in data:
				if (rowdata[2]==str(i)):
					cluster_data.append(rowdata)
					index_val.append(count_index)
				count_index+=1
			#print cluster_data
			#print cluster_data
			file = "Cluster_data"+str(i)
			fo = open(file,"a")
			count_iter = 0
			for dataout in cluster_data:
				#print dataout[0] ,":" ,dataout[1] , ":" , dataout[2] ,"\n"
				line = fo.write(str(index_val[count_iter])+":"+str(dataout[0])+":"+str(dataout[1])+":"+str(dataout[2])+"\n")
				count_iter+=1
			fo.close()

	def Testdata(self,filename,centroidfile,num_cluster):
		user_vector = []
		for line in open(filename):
			strval = line.strip().translate(None, string.punctuation)
			user_vector.append(strval)

		#print len(user_vector)
		randval = randint(0,len(user_vector))
		#print randval
		test_data = user_vector[randval]
		print test_data

		test_data_vector =[]
		int_val = test_data.split()
		for val in int_val:
			test_data_vector.append(int(val))

		print test_data_vector
		centroid_list=[]
		for line in open(centroidfile):
			strval = line.strip().translate(None, string.punctuation)
			centroid_list.append(strval)

		#print centroid_list

		centroid_vector_2d = []
		for row_data in centroid_list:
			centroid_vector = []
			row_data = row_data.strip()
			row_data = row_data.split()
			#print row_data
			for val in row_data:
				#print val
				centroid_vector.append(int(val))
			centroid_vector_2d.append(centroid_vector)
		print centroid_vector_2d

		dist = []
		a = np.array(test_data_vector)
		for i in range (0,num_cluster):
			b = np.array(centroid_vector_2d[i])
			dis = np.linalg.norm(a-b)
			dist.append(dis)

		print dist
		cluster_min_dist = dist.index(min(dist))
		print cluster_min_dist

		fo = open("test_data.out","a")
		fo.write(str(randval)+":"+str(test_data_vector)+":"+str(cluster_min_dist)+"\n")
		fo.close()

	def TestData_AdjMatrix(self,con,test_data_file):
		data = []
		for line in open(test_data_file):
			data.append(tuple(line.strip().split(':')))

		cluster_num =  data[0][2]
		filename = "Cluster_data"+str(cluster_num)
		print filename
		for line in open(filename):
			data.append(tuple(line.strip().split(':')))
		user_list = []
		user_vector = []

		for rowdata in data:
			user_list.append(rowdata[0])
		
		rows =  len(user_list)
		cols = len(user_list)

		Adj_matrix =[[0 for x in range(cols)]for y in range(rows)]
		
		with con:
			cur = con.cursor()
			cur.execute('SELECT distinct user_id,user_friends from Reviews_Businesses_Users')
			userdata = cur.fetchall()
	

			for data in userdata:
				userId = data[0]
				if userId in user_list:
					userindex = user_list.index(userId)
					friendsList = data[1]
					list = friendsList.split()
					#print list[0]+"\n\n\n"
					#line = fo.write(userId+":")
					for i in range(0,len(list)):
						s = list[i].replace(",","")
						s = s.replace("'","")
						s = s.replace("[","")
						strval = s.replace("]","")
						if strval in user_list:
							#print str
							colindex = user_list.index(strval)
							#print colindex
							Adj_matrix[userindex][colindex]=1
						
			print Adj_matrix
			npar = np.array(Adj_matrix)
			np.savetxt('Kmeans_Adjacency.out',npar,fmt='%d')
			


		







			









			


graph = graph("smlProject_v2_usr(str-4,fans-50,review_count-50)_business(review_count-5).db")
conn = graph.connection()
#graph.matrix_FriendsList(conn,"Graphfriends.txt","Adj_matrix.txt")
#print conn
#graph.similarityComputation(conn)
#graph.Kmeans_clusterSeparate('Kmeans_FINAL.txt',5)
#graph.Testdata('User_id_adj_ravi.out','centroid.out',5)
graph.TestData_AdjMatrix(conn,"test_data.out")