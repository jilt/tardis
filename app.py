from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:pippo@tardis.cuhorxnidu3b.us-west-2.rds.amazonaws.com/tardis_base'
db = SQLAlchemy(app)

class User(db.Model):
    iduser = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(200), nullable=True)
    date_ins = db.Column(db.DateTime, nullable=True)
    date_ult_mod = db.Column(db.DateTime, nullable=True)
    token_expire = db.Column(db.String(200), nullable=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/duke')
def duke():
    users = User.query.all()
    return render_template('duke.html', users=users)

@app.route('/duke', methods=['POST'])
def duke_post():
    email = request.form.get('user_mail')
    #return render_template('duke.html', user=user)

    duke_post = User(iduser=2023, email=email)
    db.session.add(duke_post)
    db.session.commit()

    return duke()

if __name__== "__main__":
    app.run(debug=True)
