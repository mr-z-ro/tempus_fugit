from app.models import db, Base
from sqlalchemy import text


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

    @staticmethod
    def get_my_projects(user_email):
        query = '''SELECT DISTINCT
                          p.id,
                          p.name,
                          p.active,
                          p.budget,
                          p.budget_time,
                          p.user_id,
                          p.currency,
                          p.start_date,
                          p.finish_date,
                          p.project_stage_id,
                          p.updated
                        FROM project p
                        LEFT JOIN project_task pt ON pt.project_id = p.id
                        LEFT JOIN project_task_assign pta ON pta.project_task_id = pt.id
                        LEFT JOIN booking b ON b.project_id = p.id
                        LEFT JOIN user u ON (p.user_id = u.id OR pta.user_id = u.id OR b.user_id = u.id)
                        WHERE u.email = :email AND p.active="1";'''
        return Project.query.from_statement(text(query)).params(email=user_email).all()

    def __repr__(self):
        return '<Project %r>' % self.id
