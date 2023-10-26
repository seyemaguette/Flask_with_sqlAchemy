from flask import Flask
import sqlite3

app=Flask(__name__)

connection=sqlite3.connect("mybase.db")
print("connecter")
connection.execute("""create table employer(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
    ) """)
print("table creer ave succes")

if __name__=="__main__":
    app.run(debug=True)

