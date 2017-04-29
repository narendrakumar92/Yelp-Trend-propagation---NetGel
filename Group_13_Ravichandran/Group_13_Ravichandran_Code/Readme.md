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

* Steps - create_database:
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


## Perform Topic Clustering for Kmeans and TwitterRank

	
* Data Inputs:
	* smlProject_v2_usr(str-4,fans-50,review_count-50)_business(review_count-5).db - Database used for topic modelling
	* userid_adjacency_original.out - UserId Adjacney list calculated using the friend ids
	* user_id_lda_topic_scores.out - UserId topic scores calculated from calculate LDA step

* Outputs:
	* userid_adjacency_original.out - UserId Adjacency list calculated using the friend ids
	* user_id_lda_topic_scores.out - UserId topic scores calculated from calculate LDA step

* Steps - calculate_lda:
	* Provide the correct relative path for the listed required input files
	-  Calculate adjacency List
		1. execute matrix_FriendsList function from graph.py to get the required adjacency matrix in regards to the database file used.
	-  Calculate Similarity Computation
		1. Compute weight of the edges with respect to the adjacency matrix
		2. execute similarityComputation function from graph.py 
	- Perform K-Means Clustering for Users
		1. Execute k-means clustering based on similarity computation of edges from previous step
		2. to achieve this please call Kmeans_clusterSeparate from graph.py
	- Create LDA Corpus
		1.	Select all the reviews from the database to create the corpus
		2. execute corpusFormulation function from LDA_formulation.py
		3. execute LDAUnique function from LDA_formulation.py to remove the stop words from the corpus
		4. To apply LDA to the generated and pruned corpus please execute corpusLDA function from LDA_Formulation.py
	- Perform LDA for each User
		1. To apply LDA on every user please call the function usewrReviewLDA from LDA_Formulation.py 
	- Create the Adjacency Matrix for topics
		1. To create the 10 Matrices with respect to the topics please call readUserTopics function from LDA_Formualtion.py

## Perform Page Rank for Kmeans and TwitterRank

* Assumptions: 
	* Python version 3 is installed.

* Data Inputs Assumptions:
	* FileNameAdj is the prefix of the Adjacency Matrix files
	* FileNameDocWord is the name of the file containing the Document term Matrix

* Data Inputs: 
	1. Adjacency Matrix
	2. Document Term Matrix

* Outputs:
	* resultpagerank score followed by the node index. The results are sorted in descending order.

* Steps - calculate_rank:
	* Provide the correct input relative path for the listed required input files in an input folder 
	- Execute Twitter Rank
		1. Ensure the adjacency matrices and the document term matrix are in the input folder.
		2. Execute the script pagerank_tr.py
	- Execute K-Means Pagerank
		1. Ensure the adjacency matrices is in the input folder.
		2. Execute the script pagerank_KMeans.py
	- Calculate the No Of Connections
		1. Ensure the adjacency matrices of relationships an unweighted graph showing all friend relationships is in the input folder. 
		2. Execute the script noOfConnections.py
	- Determine Active vs Influential users
		1. Ensure document term matrix and the user list files from the previous step are in the input folder.
		2. Execute the script activeUsers.py

## Perform Topic Clustrering Using Doc2Vec

* Assumptions: 
	* genism is installed.
	* re is installed.
	* stop_words is installed.

* Data Inputs:
	* smlProject_v2_usr(str-4,fans-50,review_count-50)_business(review_count-5).db - Database used for topic modelling

* Output:
	* doc2vec.model - saved state of our doc2vec model 
	* Doc2Vec_kmeans.txt - contains all the userids and their cluster assignments.

* Steps - calculate_doc2vec:
	* Set the relative path for the Database to be used.
	* execute doc2vec_final.py


## Visualising K-means vs Twitter rank hit ratios

* Assumptions: 
	* Neo4j is installed
	* Given file is in CSV format

* Data Inputs: 
	* Graphfriends.csv - The output file of the comparisons between the K-means and Twitter rank algorithms which has the hit ratio percentages.


* Outputs:
	* The output can be seen in the browser by visiting localhost:7474. The influential user and his friends network will be displayed upon cypher query. The information dissemination is shown in a different colour throughout the graph.

* Steps - graph_visualization_using_neo4j:
	1. In command prompt, change directory to the folder "graph_visualization_using_neo4j" to get the script "graph_network_plot.py".
	2. Make sure the neo4j local server is running.
	3. Ensure the path to the input file is given from command line at the time of running the program.
	4. Run the program from the terminal, using the command; python graph_plot_neo4j.py <file_path> . [The graph data used can be viewed at this link] (https://drive.google.com/open?id=0B0ETTAFdGvp9ZTZNdDZ1cERNYWM)
	5. Open the browser and type in; localhost:7474.
	6. To view the resultant graph, in the cypher command line in the browser, run; MATCH (n) RETURN n;

## Testing PageRank Correctness

 * Assumptions
 	* Python 2.7 Installed 	

 * Data Inputs: 
	* userid_adjacency_original.out - UserId Adjacency list calculated using the friend ids
	* user_id_mapping_list.out - The index and UserID mapping
	* user_id_lda_topic_scores.out - UserId topic scores calculated from calculate LDA step
	* smlProject_v2_usr(str-4,fans-50,review_count-50)_business(review_count-5).db - The pruned database generated in create database step

* Outputs
	1.  userid_topic_adjaceny_list - For Each topic
	2.  pagrank_topic_result - For Each topic
	3.  influential_node_result - the userid index selected and the matrix computation

* Steps - test_pageRank:
	1. Provide the correct input relative path for the listed required input files
	2. Provide the correct output relative path.
	3. Run test_script_tr.py 
		

