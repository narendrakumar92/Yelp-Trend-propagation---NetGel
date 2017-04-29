#!/usr/bin/python
# coding=utf-8

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import re

sqlalchemy_base = declarative_base()


class Reviews_Businesses_Users(sqlalchemy_base):
    __tablename__ = 'Reviews_Businesses_Users'
    __table_args__ = {'sqlite_autoincrement': True}
    review_id = Column(String, primary_key=True)
    user_id = Column(String)
    business_id = Column(String)
    review_text = Column(String)
    business_name = Column(String)
    business_categories = Column(String)
    business_state = Column(String)
    business_city = Column(String)
    business_attributes = Column(String)
    business_review_count = Column(Integer)
    business_stars = Column(Float)
    user_name = Column(String)
    user_review_count = Column(Integer)
    user_average_stars = Column(Float)
    user_fans = Column(Integer)
    review_stars = Column(Integer)
    review_date = Column(Date)
    review_useful = Column(Integer)
    review_cool = Column(Integer)
    review_funny = Column(Integer)
    user_useful = Column(Integer)
    user_yelping_since = Column(Date)
    user_cool = Column(Integer)
    user_funny = Column(Integer)
    business_address = Column(String)
    business_postal_code = Column(String)
    review_types = Column(String)
    user_friends_count = Column(Integer)
    user_friends = Column(String)



def reviews_businesses_users_object(data):
    return Reviews_Businesses_Users(**{
        'review_id': str(data[0]),
        'review_text': str(data[1]),
        'review_stars' : int(data[2]),
        'review_date' : datetime.strptime(str(data[3]), '%Y-%m-%y').date(),
        'review_useful' : int(data[4]),
        'review_cool' : int(data[5]),
        'review_funny': int(data[6]),
        'review_types': str(data[7]),

        'business_id': str(data[8]),
        'business_address': str(data[9]),
        'business_attributes': str(data[10]),
        'business_categories': str(data[11]),
        'business_city': str(data[12]),
        'business_review_count': int(data[13]),
        'business_name': str(data[14]),
        'business_state': str(data[15]),
        'business_stars': float(data[16]),
        'business_postal_code': str(data[17]),

        'user_id': str(data[18]),
        'user_yelping_since': datetime.strptime(str(data[19]), '%Y-%m-%y').date(),
        'user_useful': int(data[20]),
        'user_review_count': int(data[21]),
        'user_fans': int(data[22]),
        'user_funny': int(data[23]),
        'user_friends': str(data[24]),
        'user_friends_count': 0,
        'user_cool': int(data[25]),
        'user_name': str(data[26]),
        })


class Tips_Businesses_Users(sqlalchemy_base):
    __tablename__ = 'Tips_Businesses_Users'
    __table_args__ = {'sqlite_autoincrement': True}
    tip_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    business_id = Column(String)
    tip_text = Column(Text)
    tip_likes = Column(Integer)
    tip_date = Column(Date)
    business_name = Column(String)
    business_categories = Column(String)
    business_state = Column(String)
    business_city = Column(String)
    business_attributes = Column(String)
    business_review_count = Column(Integer)
    business_stars = Column(Float)
    user_name = Column(String)
    user_review_count = Column(Integer)
    user_average_stars = Column(Float)
    user_fans = Column(Integer)
    user_useful = Column(Integer)
    user_yelping_since = Column(Date)
    user_cool = Column(Integer)
    user_funny = Column(Integer)
    business_address = Column(String)
    business_postal_code = Column(String)
    tip_types = Column(String)
    user_friends_count = Column(Integer)
    user_friends = Column(String)


def tips_businesses_users_object(data):
    return Tips_Businesses_Users(**{
        'tip_text': str(data[0]),
        'tip_likes': int(data[1]),
        'tip_date': datetime.strptime(str(data[2]), '%Y-%m-%y').date(),
        'tip_types': str(data[3]),

        'business_id': str(data[4]),
        'business_address': str(data[5]),
        'business_attributes': str(data[6]),
        'business_categories': str(data[7]),
        'business_city': str(data[8]),
        'business_review_count': int(data[9]),
        'business_name': str(data[10]),
        'business_state': str(data[11]),
        'business_stars': float(data[12]),
        'business_postal_code': str(data[13]),

        'user_id': str(data[14]),
        'user_yelping_since': datetime.strptime(str(data[15]), '%Y-%m-%y').date(),
        'user_useful': int(data[16]),
        'user_review_count': int(data[17]),
        'user_fans': int(data[18]),
        'user_funny': int(data[19]),
        'user_friends': str(data[20]),
        'user_friends_count': 0,
        'user_cool': int(data[21]),
        'user_name': str(data[22]),

        })


class FormattedTableDefinitions:
    def __init__(self, database_engine):
        self.database_engine = database_engine
        self.create_tables()

    def create_tables(self):
        sqlalchemy_base.metadata.create_all(self.database_engine)


def formatted_base_type_return(classname, data):
    if classname == 'reviews_businesses_users': return reviews_businesses_users_object(data)
    elif classname == 'tips_businesses_users': return tips_businesses_users_object(data)