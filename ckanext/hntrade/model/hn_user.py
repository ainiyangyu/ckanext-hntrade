import uuid

from sqlalchemy import Column, MetaData
from sqlalchemy import types
from sqlalchemy.ext.declarative import declarative_base

import ckan.model as model
from ckan.lib.base import *

log = __import__('logging').getLogger(__name__)

Base = declarative_base()

metadata = MetaData()


def make_uuid():
    return unicode(uuid.uuid4())


class HnUser(Base):
    __tablename__ = 'hn_user'

    id = Column(types.Text, primary_key=True, default=make_uuid())
    user_id = Column(types.Integer, index=True)
    login_name = Column(types.Text, index=True)
    user_name = Column(types.Text)
    sex = Column(types.Text)
    birthday = Column(types.Text)
    phone = Column(types.Text)
    mail = Column(types.Text)
    check_email = Column(types.Text)
    has_authentication = Column(types.Text)
    user_role = Column(types.Text)
    user_status = Column(types.Text)
    update_date = Column(types.Text)
    create_date = Column(types.Text)
    version = Column(types.Text)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def get_by_login_name(cls, name):
        return model.Session.query(cls).filter(
            cls.login_name == name).first()


def init_tables(e):
    Base.metadata.create_all(e)
