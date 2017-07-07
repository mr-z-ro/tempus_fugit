from sqlalchemy import text

from app.models import db, Base
import uuid
import pdb

class AccessKey(Base):

    __bind_key__ = 'access_keys'

    id = db.Column(db.Integer(), primary_key=True)
    pid = db.Column(db.Integer())
    tid = db.Column(db.Integer())
    uuid = db.Column(db.String(64))

    def __init__(self, pid=None, tid=None):
        self.pid = pid
        self.tid = tid
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return "<AccessKey(uuid='%s', tid='%r', pid='%r'>" % (self.uuid, self.tid, self.pid)

    @staticmethod
    def info_for_access_key(uuid):
        pdb.set_trace()

        query = '''SELECT 
                      tid, pid
                    FROM access_keys
                    WHERE
                    uuid = :uuid'''
        return AccessKey.query.from_statement(text(query)).params(uuid=uuid).all()

    @staticmethod
    def all():
        query = '''SELECT * FROM access_keys'''
        return AccessKey.query.from_statement(text(query)).params().all()


