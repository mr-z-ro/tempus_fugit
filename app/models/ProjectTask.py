from sqlalchemy import text

from app.models import db, Base

import Project


class ProjectTask(Base):

    __tablename__ = 'project_task'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200))
    project_id = db.Column(db.Integer())
    project_name = db.Column(db.String(200))
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())

    @staticmethod
    def get_by_id(project_task_id):
        query = '''SELECT DISTINCT
                      pt.id,
                      pt.name,
                      pt.project_id,
                      p.name AS project_name,
                      pt.start_date,
                      pt.end_date
                    FROM project_task pt
                    INNER JOIN project p ON pt.project_id = p.id
                    WHERE
                    pt.id = :project_task_id;'''
        return ProjectTask.query.from_statement(text(query)).params(project_task_id=project_task_id).all()


    def __repr__(self):
        return '<ProjectTask %r>' % self.id
