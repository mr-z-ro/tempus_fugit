from app.models import db, Base


class Project(Base):

    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    active = db.Column(db.String(1))
    budget = db.Column(db.Float(scale=16, precision=2))
    budget_time = db.Column(db.Float(scale=12, precision=2))
    user_id = db.Column(db.Integer())
    currency = db.Column(db.String(3))
    start_date = db.Column(db.Date())
    finish_date = db.Column(db.Date())
    project_stage_id = db.Column(db.Integer())
    updated = db.Column(db.DateTime())

    def __repr__(self):
        return '<Project %r>' % self.id
