#!/usr/bin/python
from sqlalchemy import Column, Integer, Float, Date, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

sqlalchemy_base = declarative_base()

class TableDefinitions:
	def __init__(self,database_engine):
		self.database_engine = database_engine
		self.create_tables()
		
	def create_tables(self):
		sqlalchemy_base.metadata.create_all(self.database_engine)
		
	
	class Checkins(sqlalchemy_base):
		__tablename__ = 'Checkins'
		__table_args__ = {'sqlite_autoincrement': True}
		business_id = Column(String, primary_key=True, nullable=False) 
		types = Column(String)
	 	times = Column(String)

	class Tips(sqlalchemy_base):
		__tablename__ = 'Tips'
		__table_args__ = {'sqlite_autoincrement': True}
		id = Column(Integer, primary_key=True, autoincrement=True)
		user_id = Column(String) 
		business_id = Column(String) 
		text = Column(String)
	 	likes = Column(Integer)
		date = Column(Date)
		types = Column(String)
	
def base_type_return(filename,data):
	switcher = {
		'yelp_academic_dataset_checkin.csv' : Checkins(**{
						'times' : str(data[0]),
						'types' : str(data[1]),
						'business_id' : str(data[2]),

					}),
		'yelp_academic_dataset_tip.csv' : 
			Tips(**{'user_id' : str(data[0]),
						'text' : str(data[1]),
						'business_id' : str(data[2]),
						'likes' : int(data[3]),
						'date' : datetime.strptime(str(data[4]), '%Y-%m-%y').date(),
						'types' : str(data[5]),
					}),
	}
	return switcher.get(filename, "nothing")