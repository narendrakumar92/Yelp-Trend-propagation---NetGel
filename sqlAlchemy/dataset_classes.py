#!/usr/bin/python
# coding=utf-8

from sqlalchemy import Column, Integer, Float, Date, String, Text, Boolean,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import re
from utility_functions import *

sqlalchemy_base = declarative_base()

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
    user_id = Column(String)
    business_id = Column(String)
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
    


        
