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
    user_id = db.Column(db.Integer())
    project_id = db.Column(db.Integer())
    currency = db.Column(db.String(3))
    city = db.Column(db.String(75))
    quantity = db.Column(db.Float(scale=12, precision=2))
    acct_date = db.Column(db.Date())

    def __repr__(self):
        return '<Ticket %r>' % self.id
