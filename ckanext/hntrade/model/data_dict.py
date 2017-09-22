from datetime import datetime
from sqlalchemy import Column, MetaData
from sqlalchemy import types
from sqlalchemy.ext.declarative import declarative_base

from ckan.lib.base import *


log = __import__('logging').getLogger(__name__)

Base = declarative_base()

metadata = MetaData()


class DataDict(Base):
    __tablename__ = 'data_dict'

    id = Column(types.Text, primary_key=True)
    res_id = Column(types.Text, index=True)
    pkg_id = Column(types.Text, index=True)
    records = Column(types.Text)
    created = Column(types.DateTime, default=datetime.now)
    modified = Column(types.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def get(cls, res_id):
        query = model.Session.query(cls).autoflush(False)
        query = query.filter(cls.res_id == res_id)
        return query.first()

    @classmethod
    def delete(cls, res_id):
        query = model.Session.query(cls).autoflush(False)
        query.filter(cls.res_id == res_id).delete()
        model.Session.commit()
        return


def init_tables(e):
    Base.metadata.create_all(e)
