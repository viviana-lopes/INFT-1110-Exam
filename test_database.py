from flask import Flask, render_template, request, jsonify
import psycopg2
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome"

@app.route('/data/')
def index():
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
