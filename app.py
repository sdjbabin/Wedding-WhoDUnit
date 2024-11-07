from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    sql_query = request.form['sql_query']  # Get the SQL query from the form
    modified_query = sql_query.strip()

    # Remove all trailing semicolons, spaces, and newlines from the query
    modified_query = modified_query.rstrip("; \n")

    # Check if there's any remaining semicolon, which would indicate multiple statements
    if ";" in modified_query:
        return render_template('index.html', error="Only one SQL statement can be executed at a time.", query=sql_query)

    # If the query is a "SELECT *" statement, limit the results
    if modified_query.lower().startswith("select *"):
        modified_query += " LIMIT 10"  # Add limit for SELECT * queries

    try:
        conn = get_db_connection()
        results = conn.execute(modified_query).fetchall()  # Execute the SQL query
        conn.close()

        if not results:  # Check if results are empty
            message = ""
            return render_template('index.html', message=message, query=sql_query)

        return render_template('index.html', results=results, query=sql_query)  # Pass results and query to the template

    except Exception as e:
        return render_template('index.html', error=str(e), query=sql_query)  # Pass the error and the query


if __name__ == '__main__':
    app.run(debug=True)
