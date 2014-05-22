import datetime

from simpleflake import simpleflake, parse_simpleflake
from werkzeug.utils import cached_property
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.declarative import declared_attr

from unfeed.ext import db


class EntityModel(db.Model):

    __abstract__ = True

    def __repr__(self):
        cls_name = self.__class__.__name__
        attrs = ('%s=%r' % (attr.key, attr.value)
                 for attr in inspect(self).attrs)
        joined_attrs = ', '.join(attrs)
        return '%s(%s)' % (cls_name, joined_attrs)

    @declared_attr
    def id(cls):
        return db.Column(db.Integer, primary_key=True, default=simpleflake)

    @cached_property
    def simpleflake(self):
        return parse_simpleflake(self.id)

    @cached_property
    def creation_time(self):
        return datetime.datetime.fromtimestamp(self.simpleflake.timestamp)

    @classmethod
    def get_or_create(cls, auto_commit=True, **data):
        exists = cls.query.filter_by(**data).first()
        if exists is None:
            exists = cls(**data)
            db.session.add(exists)
            if auto_commit:
                db.session.commit()
        return exists
