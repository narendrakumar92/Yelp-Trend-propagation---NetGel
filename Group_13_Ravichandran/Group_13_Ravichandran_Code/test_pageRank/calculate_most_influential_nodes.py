#!/usr/bin/python

import numpy as np
import random as rand
import operator

import sys
from calculate_run_details import read_run_details_file


run_details_hash = {}
userid_pagerank_topic_scores_filename_range = range(0, 10)
userid_lda_topic_scores_filename , userid_pagerank_topic_scores_filename = "" , ""
userid_pagerank_topic_scores_filename_output_index , userid_pagerank_topic_scores_filename_output_data = "" , ""


def calculate_score_matrix(userid_index,run_number,run_file_name):
    print "Calculate Influential Nodes - Started"

    run_details_hash = read_run_details_file(run_file_name)

    run_number = str(run_number)

    userid_lda_topic_scores_filename = run_details_hash['userid_topic_scores_file_name']
    userid_pagerank_topic_scores_filename = run_details_hash['run_details'][run_number]['pagerank_output_prefix'] + '%d.out'

    userid_pagerank_topic_scores_filename_output_index = run_details_hash["run_details"][run_number]["influential_output_prefix"] + "userid_index.out"
    userid_pagerank_topic_scores_filename_output_data = run_details_hash["run_details"][run_number]["influential_output_prefix"] + "pagerank_matrix.out"
    result_hash = {}
    # Load files
    # print userid_lda_topic_scores_filename
    userid_lda_topic_scores_matrix = np.loadtxt(userid_lda_topic_scores_filename, dtype=int)

    userid_pagerank_topic_scores_matrix = {}
    for i in userid_pagerank_topic_scores_filename_range:
        userid_pagerank_topic_scores_matrix[i] = np.loadtxt(userid_pagerank_topic_scores_filename % (i), dtype=float)

    # Pick a random user topic score
    if userid_index == -1:
        userid_index = 1010
    random_index = userid_index
    result_hash["userid_index"] = random_index

    # Pick rows from given index and calculate sum
    userid_lda_topic_score = userid_lda_topic_scores_matrix[random_index]
    userid_lda_topic_score_sum = sum(userid_lda_topic_score)

    # write random index data to file
    fo = open(userid_pagerank_topic_scores_filename_output_index, "w+")
    output_text = str(random_index) + ":" + str(userid_lda_topic_score.tolist())
    # print "Random Index Data : " + output_text
    line = fo.write(output_text)
    fo.close()

    # create final matrix with zeroes
    userid_pagerank_topic_scores_matrix_merge = np.zeros((len(userid_pagerank_topic_scores_matrix[0]), 10))

    # Go thorugh each result matrix and multiple corresponding alpha
    for i in userid_pagerank_topic_scores_filename_range:
        cur_alpha = userid_lda_topic_score[i] * 1.0 / userid_lda_topic_score_sum
        required_matirx = userid_pagerank_topic_scores_matrix[i]
        current_matirx = [(1.0 * cur_alpha * j) for j in required_matirx]
        userid_pagerank_topic_scores_matrix_merge[:, i] = current_matirx

    userid_pagerank_topic_scores_singluar_matrix = {}

    # Calculate sum of each row and assign to user id
    current_index = 0
    for current_list in userid_pagerank_topic_scores_matrix_merge:
        userid_pagerank_topic_scores_singluar_matrix[current_index] = sum(current_list)
        current_index = current_index + 1

    # sort by dict value
    userid_pagerank_topic_scores_singluar_matrix_sorted = sorted(userid_pagerank_topic_scores_singluar_matrix.items(),
                                                                 key=operator.itemgetter(1), reverse=True)

    # write most influtential nodes data to file
    result_hash["influentail_pagerank_result"] = userid_pagerank_topic_scores_singluar_matrix_sorted
    output_text_list = []
    for current_list_data in userid_pagerank_topic_scores_singluar_matrix_sorted:
        output_text = "%d:%f" % (current_list_data[0], current_list_data[1])
        output_text_list.append(output_text)

    fo = open(userid_pagerank_topic_scores_filename_output_data, "w+")
    output_text = "\n".join(output_text_list)
    # print "\n\nInfluential Nodes Data : \n\n" + output_text
    line = fo.write(output_text)
    fo.close()

    print "Calculate Influential Nodes - Ended"
    return result_hash

def main_calculate_score_matrix(userid_index):
    return calculate_score_matrix(userid_index,1,'run_details_1010_1_.out')


