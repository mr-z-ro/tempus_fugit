from app.models import db, Base


class Task(Base):

    __tablename__ = 'task'

    id = db.Column(db.Integer(), primary_key=True)
    project_id = db.Column(db.Integer())
    project_task_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer())
    date = db.Column(db.Date())
    updated = db.Column(db.DateTime(timezone=True))
    hour = db.Column(db.Float(scale=12, precision=2))
    minute = db.Column(db.Float(scale=6, precision=0))
    timesheet_id = db.Column(db.Integer())
    cost_center_id = db.Column(db.Integer())
    decimal_hours = hour + minute/60.00

    def __repr__(self):
        return '<Task %r>' % self.id
