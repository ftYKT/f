# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Rider(db.Model):
    __tablename__ = 'rider'

    rid = db.Column(db.BigInteger, primary_key=True, info=u'??rid')
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info=u'??')
    mobile = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue(), info=u'????')
    adarea = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue(), info=u'????')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info=u'????????')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info=u'????')
