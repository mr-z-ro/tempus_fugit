from sqlalchemy import text

from app.models import db, Base


class Ticket(Base):

    __tablename__ = 'ticket'

    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date())
    updated = db.Column(db.DateTime(timezone=True))
    um = db.Column(db.String(10))
    cost = db.Column(db.Float(scale=17, precision=3))
    total = db.Column(db.Float(scale=17, precision=3))
    total_tax_paid = db.Column(db.Float(scale=16, precision=2))
    total_no_tax = total - total_tax_paid
    project_task_id = db.Column(db.Integer())
    project_task_name = db.Column(db.String(200))
    user_id = db.Column(db.Integer())
    project_id = db.Column(db.Integer())
    project_name = db.Column(db.String(200))
    currency = db.Column(db.String(3))
    city = db.Column(db.String(75))
    quantity = db.Column(db.Float(scale=12, precision=2))
    acct_date = db.Column(db.Date())

    @staticmethod
    def get_my_tickets(user_email):
        query = '''SELECT DISTINCT
                      t.id,
                      t.date,
                      t.updated,
                      t.um,
                      t.cost,
                      t.total,
                      t.total_tax_paid,
                      t.project_task_id,
                      pt.name AS project_task_name,
                      t.user_id,
                      t.project_id,
                      p.name AS project_name,
                      t.currency,
                      t.city,
                      t.quantity,
                      t.acct_date
                    FROM ticket t
                    INNER JOIN envelope e ON t.envelope_id = e.id
                    INNER JOIN project p ON e.project_id = p.id
                    LEFT JOIN project_task pt ON t.project_task_id = t.id
                    LEFT JOIN user u ON t.user_id=u.id
                    WHERE
                    u.email = :email OR
                    p.id IN (SELECT DISTINCT p2.id FROM project p2
                         LEFT JOIN project_task pt2 ON pt2.project_id = p2.id
                         LEFT JOIN project_task_assign pta ON pta.project_task_id = pt2.id
                         LEFT JOIN booking b ON b.project_id = p2.id
                         LEFT JOIN user u ON (p2.user_id = u.id OR pta.user_id = u.id OR b.user_id = u.id)
                         WHERE u.email = :email AND p2.active="1");'''
        return Ticket.query.from_statement(text(query)).params(email=user_email).all()

    def __repr__(self):
        return '<Ticket %r>' % self.id
