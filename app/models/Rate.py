from sqlalchemy import text

from app.models import db, Base


class Rate(Base):

    __tablename__ = 'up_rate'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer)
    project_name = db.Column(db.String(200))
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(200))
    rate = db.Column(db.Float(scale=16, precision=2))
    currency = db.Column(db.String(3))

    @staticmethod
    def get_all_rates():
        query = '''SELECT
                      ur.id,
                      ur.project_id,
                      p.name AS project_name,
                      ur.user_id,
                      u.name AS user_name,
                      ur.rate AS rate,
                      ur.currency
                    FROM up_rate ur
                    LEFT JOIN user u ON ur.user_id = u.id
                    LEFT JOIN project p ON ur.project_id = p.id
                    WHERE ur.user_id IS NOT NULL;'''
        return Rate.query.from_statement(text(query)).all()

    @staticmethod
    def get_rate(user_id, project_id):
        query = '''SELECT
                      ur.id,
                      ur.project_id,
                      p.name AS project_name,
                      ur.user_id,
                      u.name AS user_name,
                      ur.rate AS rate,
                      ur.currency
                    FROM up_rate ur
                    LEFT JOIN user u ON ur.user_id = u.id
                    LEFT JOIN project p ON ur.project_id = p.id
                    WHERE ur.user_id = :user_id AND ur.project_id = :project_id;'''
        return Rate.query.from_statement(text(query)).params(user_id=user_id, project_id=project_id).first()


    def __repr__(self):
        return '<Rate %r>' % self.id
