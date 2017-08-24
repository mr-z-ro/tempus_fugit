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
        query = '''SELECT 
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

    @staticmethod
    def get_booking(user_id, project_id, project_task_id):
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
                    b.user_id = :user_id AND b.project_id = :project_id AND b.project_task_id = :project_task_id;'''
        return Booking.query.from_statement(text(query)).params(user_id=user_id, project_id=project_id,
                                                                project_task_id=project_task_id).first()

    @staticmethod
    def get_active_booking_sum(user_id, project_id, project_task_id):
        # Note: query is [ill-advisedly] hacked to allow a Booking object to be returned that contains
        # _sum_ of bookings for a given user/project/task. MAX(b.id) is returned as id so that it's not
        # recognized as None or as a duplicate with any other results.
        query = '''SELECT
                      MAX(b.id) AS 'id',
                      NULL AS 'owner_id',
                      b.user_id,
                      b.project_id,
                      NULL AS 'project_name',
                      NULL AS 'startdate',
                      NULL AS 'enddate',
                      NULL AS 'percentage',
                      SUM(b.hours) AS 'hours',
                      b.project_task_id,
                      NULL AS 'project_task_name',
                      NULL AS 'as_percentage',
                      NULL AS 'approval_status'
                    FROM booking b
                    WHERE
                    b.user_id = :user_id AND b.project_id = :project_id AND b.project_task_id = :project_task_id AND b.deleted = 0
                    GROUP BY b.user_id;'''
        return Booking.query.from_statement(text(query)).params(user_id=user_id, project_id=project_id,
                                                                project_task_id=project_task_id).first()


    def __repr__(self):
        return '<Booking %r>' % self.id
