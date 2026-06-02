import os
import mysql.connector

mydb = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "host.docker.internal"),
    port=int(os.environ.get("DB_PORT", "33061")),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ["DB_PASSWORD"],
)