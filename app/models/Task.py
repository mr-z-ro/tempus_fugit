from sqlalchemy import text

from app.models import db, Base

import Project


class Task(Base):

    __tablename__ = 'task'

    id = db.Column(db.Integer(), primary_key=True)
    project_id = db.Column(db.Integer())
    project_name = db.Column(db.String(200))
    project_task_id = db.Column(db.Integer())
    project_task_name = db.Column(db.String(200))
    user_id = db.Column(db.Integer())
    date = db.Column(db.Date())
    updated = db.Column(db.DateTime(timezone=True))
    hour = db.Column(db.Float(scale=12, precision=2))
    minute = db.Column(db.Float(scale=6, precision=0))
    timesheet_id = db.Column(db.Integer())
    cost_center_id = db.Column(db.Integer())
    decimal_hours = hour + minute/60.00

    @staticmethod
    def get_my_tasks(user_email):
        query = '''SELECT DISTINCT
                      t.id,
                      t.project_id,
                      p.name AS project_name,
                      t.project_task_id,
                      pt.name AS project_task_name,
                      t.user_id,
                      t.date,
                      t.updated,
                      t.hour,
                      t.minute,
                      t.timesheet_id,
                      t.cost_center_id
                    FROM task t
                    INNER JOIN project_task pt ON t.project_task_id = pt.id
                    INNER JOIN project p ON pt.project_id = p.id
                    LEFT JOIN user u ON t.user_id = u.id
                    WHERE
                    u.email = :email OR
                    p.id IN (SELECT DISTINCT p2.id FROM project p2
                         LEFT JOIN project_task pt2 ON pt2.project_id = p2.id
                         LEFT JOIN project_task_assign pta ON pta.project_task_id = pt2.id
                         LEFT JOIN booking b ON b.project_id = p2.id
                         LEFT JOIN user u ON (p2.user_id = u.id OR pta.user_id = u.id OR b.user_id = u.id)
                         WHERE u.email = :email AND p2.active="1");'''
        return Task.query.from_statement(text(query)).params(email=user_email).all()


    @staticmethod
    def get_task(task_id):
        query = '''SELECT
                      t.id,
                      t.project_id,
                      p.name AS project_name,
                      t.project_task_id,
                      pt.name AS project_task_name,
                      t.user_id,
                      t.date,
                      t.updated,
                      t.hour,
                      t.minute,
                      t.timesheet_id,
                      t.cost_center_id
                    FROM task t
                    INNER JOIN project_task pt ON t.project_task_id = pt.id
                    INNER JOIN project p ON pt.project_id = p.id
                    WHERE
                    t.id = :task_id'''
        return Task.query.from_statement(text(query)).params(task_id=task_id).first()


    @staticmethod
    def tasks_for_project_id(project_id):
        query = '''SELECT
                      t.id,
                      t.project_id,
                      p.name AS project_name,
                      t.project_task_id,
                      pt.name AS project_task_name,
                      t.user_id,
                      t.date,
                      t.updated,
                      t.hour,
                      t.minute,
                      t.timesheet_id,
                      t.cost_center_id
                    FROM task t
                    INNER JOIN project_task pt ON t.project_task_id = pt.id
                    INNER JOIN project p ON pt.project_id = p.id
                    WHERE
                    t.project_id = :project_id'''
        return Task.query.from_statement(text(query)).params(project_id=project_id).all()


    def __repr__(self):
        return '<Task %r>' % self.id
