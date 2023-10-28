from flask import Flask, render_template, request, flash, redirect
import sqlite3

app=Flask(__name__)

# conn = sqlite3.connect('database.db')
# print("connecter")
# conn.execute("""create table revenu(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     titre TEXT NOT NULL, 
#     montant TEXT  NOT NULL
#     ) """)
# print("table creer ave succes")
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/depense", methods=['GET', 'POST'])
def depense():
    if request.method=='POST':
        depenseDetails=request.form
        titre=depenseDetails['titre']
        montant=depenseDetails['montant']
        if titre!="" and montant!="":
            cursor=get_db_connection()
            cursor.execute("(INSERT INTO depense (titre, montant) VALUES(?,?))",(titre, montant))
            cursor.commit()
            return redirect('/')
    return render_template("depense.html")

if __name__=="__main__":
    app.run(debug=True)

