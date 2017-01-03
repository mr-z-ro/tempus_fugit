import datetime
import MySQLdb
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Base(db.Model):

    __abstract__ = True

    def to_dict(self):
        obj_dict = {}
        for c in self.__table__.columns:
            key = c.name
            val = getattr(self, key)

            if isinstance(val, datetime.datetime):
                val = val.strftime("%d/%m/%Y %H:%M:%S")
            elif isinstance(val, datetime.date):
                val = val.strftime("%d/%m/%Y")
            elif isinstance(val, MySQLdb.converters.conversions[MySQLdb.constants.FIELD_TYPE.DECIMAL]):
                val = float(val)
            else:
                pass

            obj_dict[key] = val
        return obj_dict
