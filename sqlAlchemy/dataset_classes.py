#!/usr/bin/python
# coding=utf-8

from sqlalchemy import Column, Integer, Float, Date, String, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import re

sqlalchemy_base = declarative_base()


class Checkins(sqlalchemy_base):
    __tablename__ = 'Checkins'
    __table_args__ = {'sqlite_autoincrement': True}
    business_id = Column(String, primary_key=True, nullable=False)
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
#        'date': datetime.strptime(str(data[4]), '%Y-%m-%y').date(),
                'date': datetime.now(),
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
    


        
