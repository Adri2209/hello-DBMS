import csv
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class CountryTab(db.Model):
    Country = db.Column(db.String(255), primary_key=True, nullable=False)
    Coal = db.Column(db.Float)
    Gas = db.Column(db.Float)
    Oil = db.Column(db.Float)
    Hydro = db.Column(db.Float)
    Renewable = db.Column(db.Float)
    Nuclear = db.Column(db.Float)

class WorldTab(db.Model):
    Country = db.Column(db.String(255), primary_key=True, nullable=False)
    Coal = db.Column(db.Float)
    Gas = db.Column(db.Float)
    Oil = db.Column(db.Float)
    Hydro = db.Column(db.Float)
    Renewable = db.Column(db.Float)
    Nuclear = db.Column(db.Float)

def init_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()

