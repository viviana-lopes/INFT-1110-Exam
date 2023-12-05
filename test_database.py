from flask import Flask, render_template, request, jsonify
import psycopg2
import pandas as pd
from flask_restful import reqparse

app = Flask(__name__)

data_put_args = reqparse.RequestParser()
data_put_args.add_argument("query", type=str, help="Query Typed")

@app.route('/')
def index():
    return "Welcome"

@app.route('/data')
def data():
    # This function renders the index.html template.
    table_name = 'lopesTable'
    query = f"SELECT * FROM {table_name}"
    connection = create_connection()
    df = pd.read_sql_query(query, connection)
    # Display the DataFrame
    print(df)

    # Close the connection
    connection.close()
    data_json = df.to_json(orient='records')

    # Return JSON response
    return data_json

@app.route('/create', methods=['POST'])
def create():
    # This function creates a table in the database.
    args = data_put_args.parse_args()
    query = args['query']
    connection = create_connection()
    execute_query(connection, query)
    connection.close()
    print(query)
    return "Table created successfully"
    
@app.route('/insert', methods=['POST'])
def insert():
    # This function inserts data into the table.
    args = data_put_args.parse_args()
    query = args['query']
    print(query)
    connection = create_connection()
    execute_query(connection, query)
    connection.close()
    return "Data inserted successfully"

def create_connection():
    # This function creates a connection to the PostgreSQL database.
    db_params = {
        'dbname': 'lopesDB',
        'user': 'vlopes',
        'password': '12345678',
        'host': 'lopes-database.cluster-cdieyikyynhr.us-east-1.rds.amazonaws.com',  # Replace with your RDS endpoint
        'port': '5432'
    }
    conn = psycopg2.connect(**db_params)
    return conn

def execute_query(conn, query):
    # This function executes a query on the database.
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
