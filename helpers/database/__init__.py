from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
import psycopg2

def getConnection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="censoescolar",
        user="postgres",
        password="123456"
    )

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()  

#flask db init
#flask db migrate -m "mensagem"
#flask db upgrade
