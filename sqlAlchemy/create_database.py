#!/usr/bin/python

from global_variables import *
from dataset_classes import *
from utility_functions import get_csv_data

import traceback
from time import time
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



if __name__ == "__main__":
	start_time = time()
	
	engine = create_engine('sqlite:///'+sqlLite_database_name)
	print "Database Engine Created"
	
	table_definitions = TableDefinitions(engine)
	
	session = sessionmaker()
	session.configure(bind=engine)
	dbSession = session()

	try:
		for remove_file in added_files:
			if remove_file in file_names : file_names.remove(remove_file)
		print "Processing CSV Files - Started - Files Considered Are - "+str(file_names)
		for file_name in file_names:
			current_time = time()
			print "@"*20+" - Started Processing - "+file_name
			current_file_path = file_path + file_name
			print "#"*10
			print "Data loading for "+file_name+" - Started"
			data = get_csv_data(current_file_path)
			print "Data loading for "+file_name+" - Ended"
			print "#"*10
			print "Adding Records To Database "+file_name + " - Started"
			for current_data in data:
				record = base_type_return(file_name,current_data)
				dbSession.add(record)
				dbSession.commit()
			print "Adding Records To Database "+file_name + " - Ended"
			print "Commiting Records To Database "+file_name + " - Started"
			dbSession.commit()
			print "Commiting Records To Database "+file_name + " - Ended"
			print "@"*20+" - Ended Processing - "+file_name+" - Time elapsed: " + str(time() - current_time) + " s."
		print "Processing CSV Files - Ended"
	except Exception as e:
		print "!Exception!"*10
		traceback.print_exc()
		dbSession.rollback()
	finally:
		dbSession.close()
	print "Total Time elapsed: " + str(time() - start_time) + " s."