import os

import psycopg
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "FastAPI app is running"}


@app.get("/db-check")
def db_check():
    database_url = os.environ["DATABASE_URL"]

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]

    return {
        "status": "ok",
        "postgres_version": version,
    }
