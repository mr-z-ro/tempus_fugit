from sqlalchemy import text

from app.models import db, Base


class Daily(Base):

    __bind_key__ = 'dailies'
    __tablename__ = 'timesheets_vs_bookings_daily'

    id = db.Column(db.Integer(), primary_key=True)
    timesheets_id = db.Column(db.Integer())
    bookings_daily_id = db.Column(db.Integer())
    associate = db.Column(db.String(200))
    practice = db.Column(db.String(200))
    client_name = db.Column(db.String(200))
    project_name = db.Column(db.String(200))
    task_name = db.Column(db.String(200))
    date = db.Column(db.Date())
    week_of_booking = db.Column(db.Integer())
    week_of_year_iso = db.Column(db.String(3))
    booking_hours = db.Column(db.Float(scale=12, precision=8))
    booking_fees = db.Column(db.Float(scale=12, precision=2))
    timesheet_hours = db.Column(db.Float(scale=12, precision=2))
    associate_currency = db.Column(db.String(3))


    @staticmethod
    def get_dailies(project_name, task_name, associate):
        query = '''SELECT DISTINCT
                      id,
                      timesheets_id,
                      bookings_daily_id,
                      associate,
                      practice,
                      client_name,
                      project_name,
                      task_name,
                      date,
                      week_of_booking,
                      week_of_year_iso,
                      booking_hours
                      booking_fees,
                      timesheet_hours,
                      associate_currency
                    FROM timesheets_vs_bookings_daily
                    WHERE project_name=:project_name AND task_name=:task_name AND associate=:associate
                    ORDER BY date ASC'''
        return Daily.query.from_statement(text(query)).params(project_name=project_name,
                                                              task_name=task_name,
                                                              associate=associate).all()

    def __repr__(self):
        return '<Daily %r>' % self.id
