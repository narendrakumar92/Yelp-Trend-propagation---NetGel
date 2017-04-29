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
		* Provide the correct output relative path for the CSV files in json_to_csv_converter.py

	- Create Database from  CSV Files
		1. In the createDatabase Folder provide the correct relative path for the CSV files mentioned in the data inputs
		2. Run create_database.py to get the database in SQLlite format.
	
	- Create Formatted Database
		1. In the createDatabase Folder provide the correct relative path for the database created from the previous step. 
		2. Run create_format_database.py to get the database in SQLlite format.
		3. [Databses created by us can by viewed at this link] (https://drive.google.com/open?id=0B5u6zDw91bPWckIyTTd6U3F4ZVk)

## Visualizing K-means vs Twitter rank hit ratios

* Assumptions: 
	* Neo4j is installed
	* Given file is in CSV format

* Data Inputs: 
	* Graphfriends.csv - The output file of the comparions between the K-means and Twitter rank algorithms which hsa the hit ratio percentages.


* Outputs:
Outputs n similar frames into the output directory. Also outputs 
    1. the number of unique SIFT vectors considered
    2. the overall number of SIFT vectors considered
    3. the number of bytes of data from the index accessed to process the query

* Steps:
	1. Download the MATLAB software for your operating system.
	2. Install the MATLAB software with all functionalities.
	3.  Open the MATLAB code file “Task_6.m”.
	4. Compile the program and run the program.
	5. Input the fields in the dialog prompt and click OK.
		

