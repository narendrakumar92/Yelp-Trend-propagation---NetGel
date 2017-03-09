#!/usr/bin/python
# coding=utf-8

from global_variables import *
from dataset_classes import *

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

def run(sql_statement):
	rows = sql_statement.execute()
	return rows


db_engine = create_engine('sqlite:///' + sqlLite_database_name_test)

metadata = MetaData(db_engine)

#table_definitions = TableDefinitions(db_engine)

users = Table('Users', metadata, autoload=True)
businesses = Table('Businesses', metadata, autoload=True)
checkins = Table('Checkins', metadata, autoload=True)
tips = Table('Tips', metadata, autoload=True)
reviews = Table('Reviews', metadata, autoload=True)

categories = ['Food', 'Restaurants']
categories_conditon =  businesses.c.categories.contains('Food') | businesses.c.categories.contains('Restaurants')

#select_query = businesses.select( (businesses.c.review_count > 2500) & ( categories_conditon ) )
#rows = run(select_query)
#for row in rows:
#	print " - ".join([row.business_id,row.name,row.state])
	
select_query = join(tips, businesses).select((businesses.c.review_count > 2500) & ( categories_conditon ))

rows = run(select_query)
for row in rows:
	print " - ".join([row.name,row.state,row.text])
	
	
select_query = join(reviews, businesses).select((businesses.c.review_count > 2500) & ( categories_conditon ))

rows = run(select_query)
for row in rows:
	print " - ".join([row.name,row.state,row.review_text])

