#!/usr/bin/python
import os
import random as rand
import pprint
import json
import numpy as np

from calculate_run_details import calc_run_hash

from calculate_most_influential_nodes import calculate_score_matrix

lowset_nodes_perc = 0.99
strongest_nodes_perc = 0.005

def print_list(current_list):
    print "~" * 20
    print ', '.join(map(str, current_list))
    print "~" * 20 + "\n"


def run_node_dissemination(run_hash, run_number, userid_index = - 1):
    run_file_name = run_hash["run_file_name"]
    if userid_index == -1:
        userid_index = run_hash["userid_index"]
    else:
        userid_index = userid_index

    print ("Node Dissemination Run %s - Started" % (run_number) )

    run_args = run_file_name ,run_number

    run_calculate_adj_lists_tr = "python calculate_adj_lists_tr.py %s %s" % (run_args)
    os.system(run_calculate_adj_lists_tr)

    run_calculate_pagerank_tr_loop = "python calculate_pagerank_tr_loop.py %s %s" % (run_args)
    os.system(run_calculate_pagerank_tr_loop)

    score_matrix = calculate_score_matrix(userid_index, run_number, run_file_name)

    print ("Node Dissemination Run %s - Ended" % (run_number))

    return score_matrix

def find_lowest_random_node(score_matrix):
    user_list = score_matrix[:,0]
    random_index = rand.randrange(int(lowset_nodes_perc*len(score_matrix)),len(score_matrix))
    random_index = 1051
    return user_list[random_index]
    # return 5


def find_strongest_nodes(score_matrix):
    user_list = score_matrix[:, 0]
    random_index = rand.randrange(0, int(strongest_nodes_perc * len(score_matrix)))
    random_index = 15
    return user_list[:random_index]


def create_adj_list_with_strong_nodes(strongest_nodes_list,adjacency_matrix, userid_size, userid_index):
    print "req adj list ="
    # strongest_nodes_list = [12]
    required_adj_list = adjacency_matrix[userid_index]
    np_adjacency_matrix = np.array(adjacency_matrix)
    print_list(required_adj_list)
    required_adj_list = np.array(required_adj_list)
    outgoing_nodes = []
    incoming_nodes = []
    print "strongest_nodes_list = "+ str(strongest_nodes_list)
    for cur_node in strongest_nodes_list:
        cur_node = int(cur_node)
        print "started cur node = " + str(cur_node)
        cur_list = adjacency_matrix[cur_node]
        print "cur adj list = "
        print_list(cur_list)
        # or the list to get followers of influentinal users
        row_list = np.array(cur_list)
        required_adj_list = row_list | required_adj_list

        index = 0
        for cur_value in cur_list:
            if cur_value != 0 :
                outgoing_nodes.append(index)
            index = index + 1

        col_list = np_adjacency_matrix[:,cur_node]
        print "cur col adj list = "
        print_list(list(col_list))

        index = 0
        for cur_value in col_list:
            if cur_value != 0 :
                incoming_nodes.append(index)
            index = index + 1

        print "finished cur node = " + str(cur_node) + " \n\n\n"


    required_adj_list = list(required_adj_list)
    outgoing_nodes = list(set(outgoing_nodes))
    print "outgoing_nodes = " + str(outgoing_nodes)
    for outgoing_node in outgoing_nodes:
        adjacency_matrix[userid_index][outgoing_node]= 1

    incoming_nodes = list(set(incoming_nodes))
    print "incoming_nodes = " + str(incoming_nodes)
    for incoming_node in incoming_nodes:
        adjacency_matrix[incoming_node][userid_index] = 1

    # adjacency_matrix[userid_index] = required_adj_list

    print "req adj list 2= \n"
    print(required_adj_list)
    print " finished"

    return adjacency_matrix

def main_node_dissemination():
    print "Test Script TR - Started"

    # first run
    run_hash = calc_run_hash()
    score_hash = run_node_dissemination(run_hash, "1")
    # score_hash = calculate_score_matrix(1010, "1", 'run_details_1010_1_.out')


    userid_size = run_hash['userid_size']
    score_matrix = score_hash['influentail_pagerank_result']
    userid_index = score_hash['userid_index']
    score_matrix = np.array(score_matrix)


    # read current adjacaency list
    adjacency_file = run_hash["run_details"]["1"]["adjacency_file_name"]
    adjacency_matrix = np.loadtxt(adjacency_file, dtype=int)
    # print "size of adjaceny matrix = " + len(adjacency_matrix)

    # modify current adjacency matrix
    next_userid_index = find_lowest_random_node(score_matrix)
    # next_userid_index = 959
    matrix_userid_index = next_userid_index
    print next_userid_index , matrix_userid_index
    strongest_nodes_list = find_strongest_nodes(score_matrix)
    new_adjacency_matrix = create_adj_list_with_strong_nodes(strongest_nodes_list,adjacency_matrix, userid_size, matrix_userid_index)

    # put new ad next input dir
    next_adjacency_file_name = run_hash["run_details"]["2"]["adjacency_file_name"]
    np.savetxt(next_adjacency_file_name, new_adjacency_matrix, fmt='%d')

    next_score_hash = run_node_dissemination(run_hash, "2", next_userid_index)

    print "*"*50
    # pprint.pprint(next_score_hash)


    #delete output dir
    #delete next output dir
    #delete next input dir

    print "Test Script TR - Ended"


main_node_dissemination()