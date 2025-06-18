import psycopg2
from flask import g
from helpers.application import app

DATABASE_CONFIG = {
    'dbname': 'censoescolar',
    'user': 'postgres',
    'password': '123456',
    'host': 'localhost',
    'port': '5432'
}

def getConnection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(**DATABASE_CONFIG)
    return db

@app.teardown_appcontext
def closeConnection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

