from flask import Flask, jsonify, request, Response
import configparser
import os
import sqlite3
import json
from sqlite3 import Error

SQLITE_PATH = "flask_demo.db"
error_code = {
    "1000": {
        "error_code": 1000,
        "message": "OK",
        "http_status_code": 200,
        },
    "1001": {
        "error_code": 1001,
        "message": "User exist.",
        "http_status_code": 200,
        },
}

app = Flask(__name__)

@app.route("/")
def home():
    return "testPage"


@app.route('/userinfo', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def userinfo():
    data = request.json

    if request.method == 'GET':
        a = userinfo_read( data["name"] )
    elif request.method == 'POST':
        a = userinfo_create( data )
    elif request.method == 'PUT':
        a = userinfo_update()
    elif request.method == 'DELETE':
        a = userinfo_delete()
    else:
        a = "methodn not allowed"

    result = {}
    result["message"] = error_code[a]
    result["request_body"] = data

    return jsonify(result), error_code[a]["http_status_code"]


def userinfo_create( data ):
    con = create_connection( SQLITE_PATH )
    cur = con.cursor()
    sql_query = """
    INSERT INTO userinfo( name, job_title ) VALUES( :name, :job_title )
    """
    sql_data = {}
    sql_data["name"] = data["name"]
    sql_data["job_title"] = data["job_title"]

    try:
        cur.execute( sql_query, sql_data )
        result = "1000"
    except Error as e:
        if "UNIQUE constraint failed" in str(e):
            result = "1001"

    con.commit()
    con.close()

    return result


def userinfo_read( name ):
    return name


def userinfo_update():
    return "update ..."


def userinfo_delete():
    return "delete"


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def database_init(database):
    print("Start database init ...")
    sql_create_userinfo_table = """
    CREATE TABLE IF NOT EXISTS userinfo (
        id integer PRIMARY KEY,
        name text UNIQUE NOT NULL,
        job_title text
    )
    """
    sql_create_comminfo_table = """
    CREATE TABLE IF NOT EXISTS comminfo (
        id integer PRIMARY KEY,
        userinfo_id text NOT NULL,
        comm_method text,
        comm_data text,
        FOREIGN KEY (userinfo_id) REFERENCES userinfo (id)
    )
    """

    conn = create_connection(database)
    
    if conn is not None:
        create_table(conn, sql_create_userinfo_table)
        create_table(conn, sql_create_comminfo_table)
    else:
        print("Error! cannot create the database connection.")

    return


if __name__ == '__main__':
    if os.path.isfile( SQLITE_PATH ):
        print("DB exist, skip init")
    else:
        print("DB not exist")
        database_init( SQLITE_PATH )

    app.run( debug=True )