#!/usr/bin/python
# coding=utf-8

from time import time

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

from dataset_classes import *
from dataset_classes_formatted import *
from global_variables import *

# import statements for yelp datasets
import_db_engine = create_engine('sqlite:///' + sqlLite_database_name_test)
import_metadata = MetaData(import_db_engine)
table_definitions = TableDefinitions(import_db_engine)
session = sessionmaker()
session.configure(bind=import_db_engine)
import_db_session = session()
# table definitions for yelp datasets table
users = Table('Users', import_metadata, autoload=True)
businesses = Table('Businesses', import_metadata, autoload=True)
checkins = Table('Checkins', import_metadata, autoload=True)
tips = Table('Tips', import_metadata, autoload=True)
reviews = Table('Reviews', import_metadata, autoload=True)

# statements for export database
export_db_engine = create_engine('sqlite:///' + sqlLite_database_name_formatted)
export_metadata = MetaData(export_db_engine)
table_definitions = FormattedTableDefinitions(export_db_engine)
session = sessionmaker()
session.configure(bind=export_db_engine)

categories = ['Food', 'Restaurants']
categories_conditon = Businesses.categories.contains('Food') | Businesses.categories.contains('Restaurants')

def run_query_and_add_data(class_name,join_class_name,class_attributes):
    print "@" * 20 + " - Started Processing - " + class_name

    print "#" * 10
    current_start_time = time()
    current_time = current_start_time

    print "Started Query Processing for " + class_name

    businesses_condition = (Businesses.review_count > 5500) & (categories_conditon)
    users_condition = (Users.average_stars > 4) & (Users.review_count > 50) & (Users.fans > 50)

    select_query = import_db_session.query(eval(class_name), Businesses, Users).filter(businesses_condition).filter(
        users_condition).join(Businesses).join(Users)
    query_result = select_query.all()

    print "Ended Query Processing for " + class_name + " | Time elapsed: " + str(time() - current_time) + " s."

    print "#" * 10
    current_time = time()

    print "Started Data loading for " + class_name

    export_db_session = session()
    business_attributes = ['business_id', 'address', 'attributes', 'categories', 'city', 'review_count', 'name',
                           'state', 'stars', 'postal_code']
    user_attributes = ['user_id', 'yelping_since', 'useful', 'review_count', 'fans', 'funny', 'friends', 'cool', 'name']
    for row in query_result:
        current_class = row[0]
        current_business = row[1]
        current_user = row[2]
        data_list = []
        for attribute in class_attributes:
            data_list.append(getattr(current_class, attribute))
        for attribute in business_attributes:
            data_list.append(getattr(current_business, attribute))
        for attribute in user_attributes:
            data_list.append(getattr(current_user, attribute))
        record = formatted_base_type_return(join_class_name, data_list)
        export_db_session.add(record)
    print "Ended Data loading for " + class_name + " | Time elapsed: " + str(time() - current_time) + " s."

    print "#" * 10
    current_time = time()

    print "Started Commiting Records To Database for " + class_name
    export_db_session.commit()
    print "Ended Commiting Records To Database for " + class_name + " | Time elapsed: " + str(
        time() - current_time) + " s."

    print "#" * 10
    print "@" * 20 + " - Ended Processing - " + class_name + " | Time elapsed: " + str(
        time() - current_start_time) + " s."

if __name__ == "__main__":

    start_time = time()
    class_names = {
        'Reviews': {
            "join_class_name" : 'reviews_businesses_users',
            "attributes" : ['review_id', 'review_text', 'stars', 'date', 'useful', 'cool', 'funny', 'types']
        },
        'Tips' : {
            "join_class_name": 'tips_businesses_users',
            "attributes": ['text','likes','date','types']
                   }
        }

    for class_name in class_names:
        current_dict = class_names[class_name]
        run_query_and_add_data(class_name, current_dict["join_class_name"],current_dict["attributes"])

    print "Total Time elapsed: " + str(time() - start_time) + " s."