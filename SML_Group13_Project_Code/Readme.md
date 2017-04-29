# CSE 575 Statistical Machine Learning:

# Group 13

## Yelp Trend Propagation: Finding like-minded Influential user to spread Information 

## Dataset Processing and Database Set Up

* Assumptions:
	* SQLlite3 is Installed
	* Python 2.7 is Installed
	* SQLAlchemy is Installed
	* JSON dataset downloaded from Yelp

* Data Inputs:
	* user.csv
	* business.csv
	* review.csv
	* tip.csv
	* checkin.csv

* Outputs:
	* Outputs of JSON into CSV format
	* Output of all csv files into respected tables in an SQLlite database file
	* Output of a pre-processed table Reviews_Business_Users in an SQLlite database file

* Steps:
	- Convert CSV into JSON format
		1. Clone the repo https://github.com/Yelp/dataset-examples
		2. Provide the correct input relative path for the JSON files in json_to_csv_converter.py
		3. Provide the correct output relative path for the CSV files in json_to_csv_converter.py

	- Create Database from  CSV Files
		1. In the create_database Folder provide the correct relative path for the CSV files mentioned in the data inputs
		2. Run create_database.py to get the database in SQLlite format.
	
	- Create Formatted Database
		1. In the create_database Folder provide the correct relative path for the database created from the previous step. 
		2. Run create_format_database.py to get the database in SQLlite format.
		3. [Databases created by us can by viewed at this link] (https://drive.google.com/open?id=0B5u6zDw91bPWckIyTTd6U3F4ZVk)

## Perform Topic Clustrering Using Doc2Vec

* Assumptions: 
	* genism is installed.
	* re is installed.
	* stop_words is installed.

* Data Inputs:
	* smlProject_v2_usr(str-4,fans-50,review_count-50)_business(review_count-5).db - Database used for topic modelling

* Output
	* doc2vec.model - saved state of our doc2vec model 
	* Doc2Vec_kmeans.txt - contains all the userids and their cluster assignments.

* Steps
	* Set the relative path for the Database to be used.
	* exectute doc2vec_final.py


## Visualising K-means vs Twitter rank hit ratios

* Assumptions: 
	* Neo4j is installed
	* Given file is in CSV format

* Data Inputs: 
	* Graphfriends.csv - The output file of the comparisons between the K-means and Twitter rank algorithms which has the hit ratio percentages.


* Outputs:
	* The output can be ssen in the browser by visiting localhost:7474. The influential user and his friends network will be displayed upon cypher query. The information dissemination is shown in a different color throughout the graph.

* Steps:
	1. In command prompt, change directory to the folder "visual" of the script "graph_plot_neo4j.py".
	2. Make sure the neo4j local server is running.
	3. Ensure the path to the input file is given from command line at the time of running the program.
	4. Run the program from the terminal, using the command; python graph_plot_neo4j.py <file_path> . [The graph data used can be viewed at this link] (https://drive.google.com/open?id=0B0ETTAFdGvp9ZTZNdDZ1cERNYWM)
	5. Open the browser and type in; localhost:7474.
	6. To view the resultant graph, in the cypher command line in the browser, run; MATCH (n) RETURN n;

## Testing PageRank Correctness

 * Assumptions
 	* Python 2.7 Installed 	

 * Data Inputs: 
	* userid_adjacency_original.out - UserId Adjacney list calculated using the friend ids
	* user_id_mapping_list.out - The index and UserID mapping
	* user_id_lda_topic_scores.out - UserId topic scores calculated from calculate LDA step
	* smlProject_v2_usr(str-4,fans-50,review_count-50)_business(review_count-5).db - The pruned database generated in create database step

* Outputs
	1.  userid_topic_adjaceny_list - For Each topic
	2.  pagrank_topic_result - For Each topic
	3.  influential_node_result - the userid index selected and the matirx computation

* Steps:
	1. Provide the correct input relative path for the listed required input files
	2. Provide the correct output relative path.
	3. Run test_script_tr.py 
		

