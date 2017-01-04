from sqlalchemy import text

from app.models import db, Base


class Booking(Base):

    __tablename__ = 'booking'

    id = db.Column(db.Integer(), primary_key=True)
    owner_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer())
    project_id = db.Column(db.Integer())
    project_name = db.Column(db.String(200))
    startdate = db.Column(db.Date())
    enddate = db.Column(db.Date())
    percentage = db.Column(db.Float(scale=12, precision=2))
    hours = db.Column(db.Float(scale=12, precision=2))
    project_task_id = db.Column(db.Integer())
    project_task_name = db.Column(db.String(200))
    as_percentage = db.Column(db.String(1))
    approval_status = db.Column(db.String(1))

    @staticmethod
    def get_my_bookings(user_email):
        query = '''SELECT DISTINCT
                      b.id,
                      b.owner_id,
                      b.user_id,
                      b.project_id,
                      p.name AS "project_name",
                      b.startdate,
                      b.enddate,
                      b.percentage,
                      b.hours,
                      b.project_task_id,
                      pt.name AS "project_task_name",
                      b.as_percentage,
                      b.approval_status
                    FROM booking b
                    INNER JOIN project_task pt ON b.project_task_id = pt.id
                    INNER JOIN project p ON b.project_id = p.id
                    LEFT JOIN user u ON b.user_id = u.id
                    WHERE
                    b.approval_status = "A" AND
                    (u.email = :email OR
                    p.id IN (SELECT DISTINCT p2.id FROM project p2
                         LEFT JOIN project_task pt2 ON pt2.project_id = p2.id
                         LEFT JOIN project_task_assign pta ON pta.project_task_id = pt2.id
                         LEFT JOIN booking b ON b.project_id = p2.id
                         LEFT JOIN user u ON (p2.user_id = u.id OR pta.user_id = u.id OR b.user_id = u.id)
                         WHERE u.email = :email AND p2.active="1"));'''
        return Booking.query.from_statement(text(query)).params(email=user_email).all()

    def __repr__(self):
        return '<Booking %r>' % self.id
