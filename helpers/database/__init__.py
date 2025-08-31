import sqlite3
from flask import g, current_app, Flask

DEFAULT_DB = "censoescolar.db"

def get_db() -> sqlite3.Connection:
    if "db_conn" not in g:
        path = current_app.config.get("DATABASE", DEFAULT_DB)
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row  
        g.db_conn = conn
    return g.db_conn

def close_db(_exc=None) -> None:
    conn = g.pop("db_conn", None)
    if conn is not None:
        conn.close()

def init_database(app: Flask, *, database_path: str | None = None) -> None:
    if database_path:
        app.config["DATABASE"] = database_path
    app.teardown_appcontext(close_db)
