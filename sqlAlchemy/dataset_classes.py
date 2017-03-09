#!/usr/bin/python
# coding=utf-8

from sqlalchemy import Column, Integer, Float, Date, String, Text, Boolean,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import re
from utility_functions import *

sqlalchemy_base = declarative_base()

class Users(sqlalchemy_base):
    __tablename__ = 'Users'
    __table_args__ = {'sqlite_autoincrement': True}
    user_id = Column(String, primary_key=True, nullable=False)
    name  = Column(String)
    yelping_since = Column(Date)
    useful = Column(Integer)
    compliment_photos = Column(Integer)
    compliment_list = Column(Integer)
    compliment_funny = Column(Integer)
    compliment_plain = Column(Integer)
    review_count = Column(Integer)
    elite = Column(String)
    fans = Column(Integer)
    types = Column(String)
    compliment_note = Column(Integer)
    funny = Column(Integer)
    compliment_writer = Column(Integer)
    compliment_cute = Column(Integer)
    average_stars = Column(Float)
    compliment_more = Column(Integer)
    friends = Column(String)
    compliment_hot = Column(Integer)
    cool = Column(Integer)
    compliment_profile = Column(Integer)
    compliment_cool = Column(Integer)


def users_object(data):
    return  Users(**{
    'yelping_since' : datetime.strptime(str(data[0]), '%Y-%m-%y').date(),
    'useful' : int(data[1]),
    'compliment_photos' : int(data[2]),
    'compliment_list' : int(data[3]),
    'compliment_funny' : int(data[4]),
    'compliment_plain' : int(data[5]),
    'review_count' : int(data[6]),
    'elite' : str(data[7]),
    'fans' : int(data[8]),
    'types' : str(data[9]),
    'compliment_note' : int(data[10]),
    'funny' : int(data[11]),
    'compliment_writer' : int(data[12]),
    'compliment_cute' : int(data[13]),
    'average_stars' : float(data[14]),
    'user_id' : str(data[15]),
    'compliment_more' : int(data[16]),
    'friends' : str(data[17]),
    'compliment_hot' : int(data[18]),
    'cool' : int(data[19]),
    'name' : re.sub(r'[^\x00-\x7F]+',' ', data[20]),
    'compliment_profile' : int(data[21]),
    'compliment_cool' : int(data[22]),
    })
    

class Businesses(sqlalchemy_base):
    __tablename__ = 'Businesses'
    __table_args__ = {'sqlite_autoincrement': True}
    business_id = Column(String, primary_key=True, nullable=False)
    hours = Column(String)
    is_open = Column(Boolean)
    address = Column(String)
    attributes = Column(String)
    categories = Column(String)
    city = Column(String)
    review_count = Column(Integer)
    name = Column(String)
    longitude = Column(Float)
    state = Column(String)
    stars = Column(Float)
    latitude = Column(Float)
    postal_code = Column(String)
    types = Column(String)
    
def businesses_object(data):
    return  Businesses(**{
        'business_id': str(data[1]),
        'hours': str(data[2]),
        'is_open' : str2bool(data[3]),
        'address' : re.sub(r'[^\x00-\x7F]+',' ', data[4]),
        'attributes' : str(data[5]),
        'categories' : str(data[6]),
        'city' : re.sub(r'[^\x00-\x7F]+',' ', data[7]),
        'review_count' : int(data[8]),
        'name' : re.sub(r'[^\x00-\x7F]+',' ', data[9]),
        'longitude' : float(data[10]),
        'state' : str(data[11]),
        'stars' : float(data[12]),
        'latitude' : float(data[13]),
        'postal_code' : str(data[14]),
        'types' : str(data[15]),
        })


class Checkins(sqlalchemy_base):
    __tablename__ = 'Checkins'
    __table_args__ = {'sqlite_autoincrement': True}
    id  = Column(Integer, primary_key=True, autoincrement=True)
    business_id = Column(String, ForeignKey(Businesses.business_id), nullable=False)
    types = Column(String)
    times = Column(String)
    
def checkins_object(data):
    return  Checkins(**{
        'times': str(data[0]),
        'types': str(data[1]),
        'business_id': str(data[2]),
        })


class Tips(sqlalchemy_base):
    __tablename__ = 'Tips'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String , ForeignKey(Users.user_id))
    business_id = Column(String, ForeignKey(Businesses.business_id))
    text = Column(Text)
    likes = Column(Integer)
    date = Column(Date)
    types = Column(String)

def tips_object(data):
    return Tips(**{
        'user_id': str(data[0]),
        'text': re.sub(r'[^\x00-\x7F]+',' ', data[1]),
        'business_id': str(data[2]),
        'likes': int(data[3]),
        'date': datetime.strptime(str(data[4]), '%Y-%m-%y').date(),
        'types': str(data[5]),
        })

class TableDefinitions:
    def __init__(self, database_engine):
        self.database_engine = database_engine
        self.create_tables()

    def create_tables(self):
        sqlalchemy_base.metadata.create_all(self.database_engine)


def base_type_return(filename, data):
    if filename == 'yelp_academic_dataset_checkin.csv' : return checkins_object(data)
    elif filename == 'yelp_academic_dataset_tip.csv': return tips_object(data)
    elif filename == 'yelp_academic_dataset_business.csv': return businesses_object(data)
    elif filename == 'yelp_academic_dataset_user.csv': return users_object(data)
    


        
