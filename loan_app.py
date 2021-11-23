from flask import Flask, render_template, request,redirect,url_for,session, flash
from datetime import timedelta
import numpy as np
import pickle
import pandas as pd

app=Flask(__name__)
app.secret_key ="hello" #secret key: necessaire pour l'utilisation d'une session

@app.route("/home",methods=["POST" , "GET"])
def home():
    return render_template("index.html")

@app.route("/prediction",methods=["POST" , "GET"])
def predfunc():
    if request.method=="POST":
        l=[]
        col=['Sexe','Marié(e)','Enfant','Credit_History','Revenu1 ($)','Revenu2 ($)', 'Montant(K$)' ]
        for x in request.form.items():
            l.append(float(x[1]))
        clf = pickle.load(open('mon_model\my_model.sav', 'rb'))
        pred=clf.predict(np.array(l).reshape(1,-1))
        df=A=pd.DataFrame(np.array(l).reshape(1,-1),columns=col)
        dsexe={1:'Homme',0:'Femme'}
        dmarried= {1:'Oui',0:"Non"}
        denfant={0:'Un',1:'Un',2:'Deux',3:'Trois ou plus'}
        dhistcredit={0:'Oui',1:'Non'}
        df['Sexe'].replace(dsexe,inplace=True)
        df['Marié(e)'].replace(dmarried,inplace=True)
        df['Enfant'].replace(denfant,inplace=True)
        df['Credit_History'].replace(dhistcredit,inplace=True)
        session['data']=df.transpose().to_dict()[0]
        if pred[0]==0:
            return redirect(url_for("refuse"))
        elif pred[0]==1:
            return redirect(url_for("accept"))
    else:
        return render_template("index.html")

@app.route("/accepted")
def accept():
    mydata=session['data']
    return render_template("accepted.html",display=mydata)

@app.route("/refused")
def refuse():
    mydata=session['data']
    return render_template("refused.html",display=mydata)


if __name__=="__main__":
    app.run(debug=True)
