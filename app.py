from flask import Flask, render_template, request, flash, redirect
import sqlite3

app=Flask(__name__)

# conn = sqlite3.connect('database.db')
# conn.execute("""create table depense(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     titre TEXT NOT NULL,
#     montant INTEGER NOT NULL  
#     ) """)
# conn.execute("""create table revenu(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     titre TEXT NOT NULL,
#     montant INTEGER NOT NULL
#     ) """)
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    cursor=get_db_connection()
     # ------------------------------compteur des depenses--------------------------
    depense=0
    depenseDetails=cursor.execute("SELECT * FROM depense").fetchall()
    for depenses in depenseDetails:
        depense+=depenses[2]
    # ------------------------------compteur des revenus (budget)-----------------------------
    revenu=0
    revenuDetails=cursor.execute("SELECT * FROM revenu").fetchall()
    for revenus in revenuDetails:
        revenu+=revenus[2]
    # ------------------------------le solde-------------------------
    solde= revenu -depense
    return render_template("index.html", depenseDetails=depenseDetails, revenuDetails=revenuDetails, revenu=revenu, depense=depense, solde=solde)


@app.route("/depense", methods=['GET', 'POST'])
def depense():
    if request.method=='POST':
        revenu=0
        cursor=get_db_connection()
        revenuDetails=cursor.execute("SELECT * FROM revenu").fetchall()
        for revenus in revenuDetails:
           revenu+=revenus[2]
        error_message=""
        depenseDetails=request.form
        titre=depenseDetails['titre']
        montant=depenseDetails['montant']
        if montant.isdigit() and  titre!="":
            montant=int(montant)
            if montant<revenu:
                cursor=get_db_connection()
                cursor.execute("INSERT INTO depense (titre, montant) VALUES(?,?)",(titre, montant))
                cursor.commit()
                return redirect('/')
            else:
                error_message=" la depense est superieur a votre budget"
                return render_template("depense.html", error_message=error_message)
        else:
           error_message="le titre  et montant doivent  etre valide !!! "
           return render_template("depense.html", error_message=error_message)
    return render_template("depense.html")

@app.route("/revenu",methods=['GET','POST'])
def revenu():
    error_message=""
    if request.method=='POST':
        revenuDetails=request.form
        titre= revenuDetails['titre']
        montant= revenuDetails['montant']
        if montant.isdigit() and titre!="":
            montant=int(montant)
            if  montant>0:
                cursor=get_db_connection()
                cursor.execute("INSERT INTO revenu (titre, montant) VALUES(?, ?)", (titre, montant))
                cursor.commit()
                cursor.close()
                return redirect("/")
            else:
                error_message=" le revenu doit etre superieur à 0 "
                return render_template("revenu.html",error_message=error_message)    
        else:
            error_message="le titre  et montant doivent  etre valide !!! "
            return render_template("revenu.html",error_message=error_message)
    return render_template("revenu.html")


@app.route("/updateDepense/<int:id>", methods=['GET','POST'])
def updateDepense(id):
    cursor=get_db_connection()
    updateDepense=cursor.execute("SELECT * FROM depense WHERE id= ?",(id,)).fetchone()
    if request.method=='POST':
        # ------------------------------modification des donnees----------------------------
        revenu=0
        cursor=get_db_connection()
        revenuDetails=cursor.execute("SELECT * FROM revenu").fetchall()
        for revenus in revenuDetails:
           revenu+=revenus[2]
        error_message=""
        titre=request.form['titre']
        montant=request.form['montant'] 
        if montant.isdigit() and  titre!="":
            montant=int(montant)
            if montant<revenu:
               cursor.execute("UPDATE depense SET titre= ?, montant= ?  WHERE id= ? ",(titre, montant, id))
               cursor.commit()
               return redirect("/")
            else:
                error_message=" la depense est superieur a votre budget"
                return render_template("updateDepense.html",updateDepense=updateDepense,error_message=error_message)
        else:
           error_message="le titre  et montant doivent  etre valide !!! "
           return render_template("updateDepense.html",updateDepense=updateDepense,error_message=error_message)       
    return render_template("updateDepense.html",updateDepense=updateDepense)

@app.route("/updateRevenu/<int:id>", methods=['GET', 'POST'])
def updateRevenu(id):
    cursor=get_db_connection()
    updateRevenu=cursor.execute("SELECT * FROM revenu WHERE id= ?",(id,)).fetchone()
    if request.method=='POST':
        # ------------------------------modification des donnees----------------------------
        titre=request.form['titre']
        montant=request.form['montant']
        error_message=""
        if montant.isdigit() and titre!="":
            montant=int(montant)
            if  montant>0:
                cursor.execute("UPDATE revenu SET titre= ?, montant= ?  WHERE id= ? ",(titre, montant, id))
                cursor.commit()
                return redirect("/")
            else:
                error_message=" le revenu doit etre superieur à 0 "
                return render_template("revenu.html", updateRevenu=updateRevenu, error_message=error_message)    
        else:
            error_message="le titre  et montant doivent  etre valide !!! "
            return render_template("revenu.html", updateRevenu=updateRevenu, error_message=error_message)
  
    return render_template("updateRevenu.html",updateRevenu=updateRevenu)


@app.route("/deleteDepense/<int:id>")
def deleteDepense(id):
    # ------------------suppression des donnees-----------------
    cursor=get_db_connection()
    cursor.execute("DELETE FROM depense WHERE id= ?",(id,))
    cursor.commit()
    return redirect("/")


@app.route("/deleteRevenu/<int:id>")
def deleteRevenu(id):
    # ------------------suppression des donnees-----------------
    cursor=get_db_connection()
    cursor.execute("DELETE FROM revenu WHERE id= ?",(id,))
    cursor.commit()
    return redirect("/")



if __name__=="__main__":

    app.run(debug=True)

