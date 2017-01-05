from app.models import db, Base


class User(Base):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    nickname = db.Column(db.String(50))
    active = db.Column(db.String(1))
    timezone = db.Column(db.String(6))
    line_manager_id = db.Column(db.Integer())
    department_id = db.Column(db.Integer())

    def __repr__(self):
        return '<User %r>' % self.id
