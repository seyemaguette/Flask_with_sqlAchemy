from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Depense (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    montant = db.Column(db.String(100), nullable=False)
    def __repr__(self) :
          return f'<Depense {self.titre}>'

class Revenu (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    montant = db.Column(db.String(100), nullable=False)
    def __repr__(self) :
          return f'<Revenu {self.titre}>'



@app.route("/")
def index():
     # ------------------------------compteur des depenses--------------------------
    depense=0
    depense_details=Depense.query.all()
    for depenses in depense_details:
        depense+=int(depenses.montant)
    # ------------------------------compteur des revenus (budget)-----------------------------
    revenu=0
    revenu_details=Revenu.query.all()
    for revenus in revenu_details:
        revenu+=int(revenus.montant)
    # ------------------------------le solde-------------------------
    solde= revenu -depense
    return render_template("index.html", depense_details=depense_details, revenu_details=revenu_details, revenu=revenu, depense=depense, solde=solde)


@app.route("/depense", methods=['GET', 'POST'])
def depense():
    error_message=""
    if request.method=='POST':
        titre=request.form['titre']
        montant=request.form['montant']
        # ------------------le titre ne doit pas vide et le montant ne doit pas contenir des caracteres------------------
        if montant.isdigit() and  titre!="":
            
            # -----------------------le montant ne doit pas etre nul-------------------------------------------------
            if int(montant)>0:
                revenu=0
                revenu_details=Revenu.query.all()
                for revenus in revenu_details:
                    revenu+=int(revenus.montant)
                depense=0
                depense_details=Depense.query.all()
                for depenses in depense_details:
                    depense+=int(depenses.montant)
                solde=revenu -depense
                # ---------------------depense ne doit pas etre superieur au solde-----------------------------
                if int(montant)<=solde:
                    Depenses = Depense(titre=titre, montant=montant)
                    db.session.add(Depenses)
                    db.session.commit()
                    return redirect('/')
                else:
                    error_message=" la depense est superieur a votre budget"
            else:
                error_message="la depense doit etre superieure à 0 !!! "

        else:
                error_message="le titre  et montant doivent  etre valide !!! "

    return render_template("depense.html", error_message=error_message)

@app.route("/revenu",methods=['GET','POST'])
def revenu():
    error_message=""
    if request.method=='POST':
        titre= request.form['titre']
        montant= request.form['montant']
        # ------------------le titre ne doit pas vide et le montant ne doit pas contenir des caracteres------------------
        if montant.isdigit() and titre!="":
            # -----------------------le montant ne doit pas etre nul-------------------------------------------------
            if  int(montant)>0:
                Revenus = Revenu(titre=titre, montant=montant)
                db.session.add(Revenus)
                db.session.commit()
                return redirect("/")
            else:
                error_message=" le revenu doit etre superieur à 0 "

        else:
            error_message="le titre  et montant doivent  etre valide !!! "

    return render_template("revenu.html",error_message=error_message)


@app.route("/update_depense/<int:id>", methods=['GET','POST'])
def update_depense(id):
    update_depense= Depense.query.get_or_404(id)
    montant_delete=int(update_depense.montant)
    error_message=""
    if request.method=='POST':
        titre=request.form['titre']
        montant=request.form['montant']
        # ------------------le titre ne doit pas vide et le montant ne doit pas contenir des caracteres------------------
        if montant.isdigit() and  titre!="":
            # -----------------------le montant ne doit pas etre nul-------------------------------------------------
            if int(montant)>0:
                revenu=0
                revenu_details=Revenu.query.all()
                for revenus in revenu_details:
                    revenu+=int(revenus.montant)
                depense=0
                depense_details=Depense.query.all()
                for depenses in depense_details:
                    depense+=int(depenses.montant)
                depense-=montant_delete
                depense +=int(montant)

                solde=revenu -depense
                # ---------------------depense ne doit pas etre superieur au solde-----------------------------
                if solde>=0:
                    Depense.query.filter(Depense.id==id).update({'titre':titre, 'montant':montant})
                    # db.session.add(update_depense)
                    db.session.commit()
                    return redirect("/")
                else:
                    error_message=" la depense est superieur a votre budget"

            else:
                error_message="la depense doit etre superieure à 0 !!! "


        else:
           error_message="le titre  et montant doivent  etre valide !!! "

    return render_template("update_depense.html",update_depense=update_depense, error_message=error_message)

@app.route("/update_revenu/<int:id>", methods=['GET', 'POST'])
def update_revenu(id):
    error_message=""
    update_revenu=Revenu.query.get_or_404(id)
    montant_delete=int(update_revenu.montant)
    if request.method=='POST':
        # ------------------------------modification des donnees----------------------------
        titre=request.form['titre']
        montant=request.form['montant']
        # ------------------le titre ne doit pas vide et le montant ne doit pas contenir des caracteres------------------
        if montant.isdigit() and titre!="" :
            # -----------------------le montant ne doit pas etre nul-------------------------------------------------
            if int(montant)>0:
                revenu=0
                revenu_details=Revenu.query.all()
                for revenus in revenu_details:
                    revenu+=int(revenus.montant)
                depense=0
                depense_details=Depense.query.all()
                for depenses in depense_details:
                    depense+=int(depenses.montant)
                    
                revenu-=montant_delete
                revenu +=int(montant)

                solde=revenu -depense

                # ---------------------depense ne doit pas etre superieur au solde-----------------------------
                if  solde>=0 :
                    Revenu.query.filter(Revenu.id==id).update({'titre':titre, 'montant':montant})
                    db.session.commit()
                    return redirect("/")
                else:
                    error_message="vous ne pouvez reduire le montant car votre solde sera negatif!!! "
            else:
                error_message="le revenu de doit pas etre nul !!! "
        else:
            error_message="le titre  et montant doivent  etre valide !!! "
    
    
    return render_template("update_revenu.html", update_revenu=update_revenu, error_message=error_message)


@app.route("/delete_depense/<int:id>")
def delete_depense(id):
    # ------------------suppression des donnees-----------------
    delete = Depense.query.get_or_404(id)
    db.session.delete(delete)
    db.session.commit()
    return redirect("/")


@app.route("/delete_revenu/<int:id>")
def delete_revenu(id):
    # ------------------suppression des donnees-----------------

    Revenus=Revenu.query.get_or_404(id)
    montant_delete=int(Revenus.montant)
    revenu=0
    revenu_details=Revenu.query.all()
    for revenus in revenu_details:
        revenu+=int(revenus.montant)
    revenu-=montant_delete
    depense=0
    depense_details=Depense.query.all()
    for depenses in depense_details:
        depense+=int(depenses.montant)
    solde=revenu -depense
    if solde>=0:
        db.session.delete(Revenus)
        db.session.commit()
    return redirect("/")



if __name__=="__main__":

    app.run(debug=True)

