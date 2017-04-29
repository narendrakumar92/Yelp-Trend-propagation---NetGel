#!/usr/bin/python
import os
import random as rand
import pprint
import json


def calc_run_hash():
    # print "Calculate Run Hash Details - Started"

    run_hash = {}

    userid_size = 1052
    database_file_name = 'smlProject_v2_usr(str-4,fans-50,review_count-50)_business(review_count-5).db'
    adjacency_input_file_name_prefix = 'userid_adjacency_'
    adjacency_output_file_name_prefix = 'userid_topic_adjacency'
    pagerank_output_file_name_prefix = 'pagerank_topic_result'
    influential_output_file_name_prefix = 'influential_node_result'
    userid_topic_scores_file_name = 'user_id_lda_topic_scores.out'
    userid_mapping_list_file_name = 'user_id_mapping_list.out'


    userid_index = rand.randrange(0,userid_size)
    userid_index = 1010
    random_number = rand.randrange(0,userid_size)

    run_number = '_' + str(userid_index) + '_' + str(random_number) + '_'
    run_number = "_1010_1_"
    run_file_name = "run_details" + run_number + '.out'


    input_dir = 'input_files/'
    output_dir = 'output'+run_number+'files/'

    next_input_dir = 'next_input' + run_number + 'files/'
    next_output_dir = 'next_output' + run_number + 'files/'

    final_dir = "finalOutput_files/"

    directories = []
    directories.append(input_dir),directories.append(output_dir)
    directories.append(next_input_dir),directories.append(next_output_dir)
    directories.append(final_dir)

    for cur_dir in directories:
        if not os.path.exists(cur_dir):
            os.makedirs(cur_dir)

    run_hash["run_file_name"] = run_file_name
    run_hash["userid_size"] = userid_size
    run_hash["userid_index"] = userid_index
    run_hash["random_number"] = random_number
    run_hash["run_number"] = run_number
    run_hash["database_file_name"] = input_dir + database_file_name
    run_hash["userid_topic_scores_file_name"] = input_dir + userid_topic_scores_file_name
    run_hash["userid_mapping_list_file_name"] = input_dir + userid_mapping_list_file_name
    run_hash["final_dir"] = final_dir
    run_hash["run_details"] = {}
    run_details = {}
    run_details["input_dir"] = input_dir
    run_details["output_dir"] = output_dir
    run_details["adjacency_file_name"] = input_dir + adjacency_input_file_name_prefix + "original.out"
    run_details["adjacency_output_prefix"] = output_dir + adjacency_output_file_name_prefix + run_number + 'run1_T'
    run_details["pagerank_output_prefix"] = output_dir + pagerank_output_file_name_prefix + run_number + 'run1_T'
    run_details["influential_output_prefix"] = output_dir + influential_output_file_name_prefix + run_number + 'run1_'
    run_hash["run_details"]["1"] = run_details
    run_details = {}
    run_details["input_dir"] = next_input_dir
    run_details["output_dir"] = next_output_dir
    run_details["adjacency_file_name"] = next_input_dir + adjacency_input_file_name_prefix + run_number + ".out"
    run_details["adjacency_output_prefix"] = next_output_dir + adjacency_output_file_name_prefix + run_number + 'run2_T'
    run_details["pagerank_output_prefix"] = next_output_dir + pagerank_output_file_name_prefix + run_number + 'run2_T'
    run_details["influential_output_prefix"] = next_output_dir + influential_output_file_name_prefix + run_number + 'run2_'
    run_hash["run_details"]["2"] = run_details

    # pprint.pprint(run_hash,width = 1)

    with open(run_file_name, 'w') as outfile:
        json.dump(run_hash, outfile)


    # print "Calculate Run Hash Details - Ended"

    return run_hash


def read_run_details_file(run_details_file_name):
    with open(run_details_file_name) as data_file:
        data = json.load(data_file)
    return data