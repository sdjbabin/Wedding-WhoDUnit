import sqlite3

# Connect to SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Execute your SQL commands from the .sql file
with open('query_quest.sql', 'r') as file:  # Replace 'your_file.sql' with the path to your .sql file
    sql_script = file.read()

# Execute the SQL script
cursor.executescript(sql_script)

# Commit and close the connection
conn.commit()
conn.close()

print("Database setup completed successfully.")
