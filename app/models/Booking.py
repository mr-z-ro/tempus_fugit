from app.models import db, Base


class Booking(Base):

    __tablename__ = 'booking'

    id = db.Column(db.Integer(), primary_key=True)
    owner_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer())
    project_id = db.Column(db.Integer())
    startdate = db.Column(db.Date())
    enddate = db.Column(db.Date())
    percentage = db.Column(db.Float(scale=12, precision=2))
    hours = db.Column(db.Float(scale=12, precision=2))
    project_task_id = db.Column(db.Integer())
    as_percentage = db.Column(db.String(1))
    approval_status = db.Column(db.String(1))

    def __repr__(self):
        return '<Booking %r>' % self.id
