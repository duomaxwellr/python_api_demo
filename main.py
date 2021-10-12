from flask import Flask, jsonify, request, Response
from dotenv import load_dotenv
import os
import sqlite3
from sqlite3 import Error

load_dotenv( dotenv_path=".env", override=True )

SQLITE_FILE = os.path.join( os.getenv("DB_FILE_PATH"), os.getenv("DB_FILE_NAME") )

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
    "1002": {
        "error_code": 1002,
        "message": "User data not exist.",
        "http_status_code": 404,
        },
    "1003": {
        "error_code": 1003,
        "message": "User data deleted.",
        "http_status_code": 200,
        },
    "1004": {
        "error_code": 1004,
        "message": "User data updated.",
        "http_status_code": 200,
        },
    "1005": {
        "error_code": 1005,
        "message": "No user data updated.",
        "http_status_code": 200,
        },
    "9999": {
        "error_code": 9999,
        "message": "Exceptions.",
        "http_status_code": 503,
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
        response = userinfo_read( data )
    elif request.method == 'POST':
        response = userinfo_create( data )
    elif request.method == 'PUT':
        response = userinfo_update( data )
    elif request.method == 'DELETE':
        response = userinfo_delete( data )
    else:
        response = {}
        response["code"] = "1001"
        response["data"] = "methodn not allowed"

    # print( response )
    result = {}
    result["message"] = error_code[ response["code"] ]
    result["response_data"] = response["data"]
    result["request_body"] = data

    return jsonify(result["response_data"]), error_code[response["code"]]["http_status_code"]


def userinfo_create( data ):
    con = create_connection( SQLITE_FILE )
    cur = con.cursor()
    sql_query = """
    INSERT INTO userinfo (
            name,
            job_title,
            commu_email,
            commu_mobile
        ) VALUES (
            :name,
            :job_title,
            :commu_email,
            :commu_mobile
        )
    """
    sql_data = {}
    sql_data["name"] = data["name"]
    sql_data["job_title"] = data["job_title"]
    sql_data["commu_email"] = data["communicate_information"]["email"]
    sql_data["commu_mobile"] = data["communicate_information"]["mobile"]

    try:
        cur.execute( sql_query, sql_data )
        result_code = "1000"
        result_data = "User Created."
    except Error as e:
        if "UNIQUE constraint failed" in str(e):
            result_code = "1001"
            result_data = str(e)

    con.commit()
    con.close()

    result = {}
    result["code"] = result_code
    result["data"] = result_data

    return result


def userinfo_read( data ):
    con = create_connection( SQLITE_FILE )
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    sql_query = """
    SELECT 
        name,
        job_title,
        commu_email,
        commu_mobile
        FROM userinfo
        WHERE name = :name;
    """
    sql_data = {}
    sql_data["name"] = data["name"]

    try:
        sql_exec = cur.execute( sql_query, sql_data )
        rows = sql_exec.fetchall()
        if len(rows) == 1 :
            result_code = "1000"
            for row in rows:
                # result_data = dict( zip( row.keys(), row ) )
                result_data = {}
                result_data["name"] = row["name"]
                result_data["job_title"] = row["job_title"]
                result_data["communicate_information"] = {}
                result_data["communicate_information"]["email"] = row["commu_email"]
                result_data["communicate_information"]["mobile"] = row["commu_mobile"]
        else:
            result_code = "1002"
            result_data = "User data not exist."
    except Error as e:
        result_code = "9999"
        result_data = str(e)

    con.commit()
    con.close()

    result = {}
    result["code"] = result_code
    result["data"] = result_data

    return result


def userinfo_update( data ):
    con = create_connection( SQLITE_FILE )
    cur = con.cursor()
    sql_query = """
    UPDATE userinfo SET
            job_title = :job_title,
            commu_email = :commu_email,
            commu_mobile = :commu_mobile
        WHERE name = :name
    """
    sql_data = {}
    sql_data["name"] = data["name"]
    sql_data["job_title"] = data["job_title"]
    sql_data["commu_email"] = data["communicate_information"]["email"]
    sql_data["commu_mobile"] = data["communicate_information"]["mobile"]

    try:
        sql_exec = cur.execute( sql_query, sql_data )
        if sql_exec.rowcount == 1:
            result_code = "1004"
            result_data = "User data updated."
        elif sql_exec.rowcount == 0:
            result_code = "1005"
            result_data = "No user data updated."
        else:
            result_code = "9999"
            result_data = "User data error."
    except Error as e:
        result_code = "9999"
        result_data = str(e)

    con.commit()
    con.close()

    result = {}
    result["code"] = result_code
    result["data"] = result_data

    return result


def userinfo_delete( data ):
    con = create_connection( SQLITE_FILE )
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    sql_query = """
    DELETE FROM userinfo WHERE name = :name;
    """
    sql_data = {}
    sql_data["name"] = data["name"]

    try:
        sql_exec =  cur.execute( sql_query, sql_data )
        if sql_exec.rowcount == 1:
            result_code = "1003"
            result_data = "User data deleted."
        elif sql_exec.rowcount == 0:
            result_code = "1002"
            result_data = "User data not exist."
        else:
            result_code = "9999"
            result_data = "User data deleted."
    except Error as e:
        result_code = "9999"
        result_data = str(e)

    con.commit()
    con.close()

    result = {}
    result["code"] = result_code
    result["data"] = result_data

    return result


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
        job_title text,
        commu_email text,
        commu_mobile text
    )
    """

    conn = create_connection(database)
    
    if conn is not None:
        create_table(conn, sql_create_userinfo_table)
    else:
        print("Error! cannot create the database connection.")

    return


if __name__ == '__main__':
    if os.path.isfile( SQLITE_FILE ):
        print("DB exist, skip init")
    else:
        print("DB not exist")
        database_init( SQLITE_FILE )

    app.run( host="0.0.0.0", port="5000", debug=True )