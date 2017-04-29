#!/usr/bin/python

import numpy as np
import random as rand
import operator

filepath = ''

userid_lda_topic_scores_filename = filepath + 'user_id_lda_topic_scores_current.out'

userid_pagerank_topic_scores_filename = filepath + 'PageRank_Results_Current/' + 'Result%d.out'
userid_pagerank_topic_scores_filename_range = range(0,10)

userid_pagerank_topic_scores_filename_output_prefix = "MostInfluentialNodes_"
userid_pagerank_topic_scores_filename_output_index = filepath + userid_pagerank_topic_scores_filename_output_prefix + "random_index.out"
userid_pagerank_topic_scores_filename_output_data = filepath + userid_pagerank_topic_scores_filename_output_prefix + "data.out"

#Load files
userid_lda_topic_scores_matrix = np.loadtxt(userid_lda_topic_scores_filename ,dtype=int)

userid_pagerank_topic_scores_matrix = {}
for i in  userid_pagerank_topic_scores_filename_range:
	userid_pagerank_topic_scores_matrix[i] = np.loadtxt(userid_pagerank_topic_scores_filename % (i) , dtype=float)

#Pick a random user topic score
random_index = rand.randrange(0,len(userid_lda_topic_scores_matrix))
random_index = 1010 

#Pick rows from given index and calculate sum
userid_lda_topic_score = userid_lda_topic_scores_matrix[random_index]
userid_lda_topic_score_sum = sum(userid_lda_topic_score)

#write random index data to file
fo = open(userid_pagerank_topic_scores_filename_output_index,"w+")	
output_text = str(random_index) + ":" + str(userid_lda_topic_score.tolist())
print "Random Index Data : "+output_text
line = fo.write(output_text)
fo.close()

#create final matrix with zeroes
userid_pagerank_topic_scores_matrix_merge = np.zeros((len(userid_pagerank_topic_scores_matrix[0]),10))

#Go thorugh each result matrix and multiple corresponding alpha
for i in userid_pagerank_topic_scores_filename_range:
	cur_alpha = userid_lda_topic_score[i]*1.0/userid_lda_topic_score_sum
	required_matirx = userid_pagerank_topic_scores_matrix[i]
	current_matirx = [(1.0 * cur_alpha * j) for j in required_matirx] 
	userid_pagerank_topic_scores_matrix_merge[:,i] = current_matirx

userid_pagerank_topic_scores_singluar_matrix = {}

#Calculate sum of each row and assign to user id
current_index = 0
for current_list in userid_pagerank_topic_scores_matrix_merge:
	userid_pagerank_topic_scores_singluar_matrix[current_index] = sum(current_list)
	current_index = current_index + 1
	
#sort by dict value
userid_pagerank_topic_scores_singluar_matrix_sorted = sorted(userid_pagerank_topic_scores_singluar_matrix.items(), key=operator.itemgetter(1),reverse=True)

#write most influtential nodes data to file

output_text_list = []
for current_list_data in userid_pagerank_topic_scores_singluar_matrix_sorted:
	output_text = "%d:%f" % (current_list_data[0],current_list_data[1])
	output_text_list.append(output_text)
	
	
fo = open(userid_pagerank_topic_scores_filename_output_data,"w+")
output_text = "\n".join(output_text_list)
print "\n\nInfluential Nodes Data : \n\n"+output_text
line = fo.write(output_text)
fo.close()

	


