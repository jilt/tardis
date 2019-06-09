from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = '\x89s\xed\x9e\xf7\x9b\xf5\xd4n\xab\xa1\x8e\x08\x95\xfd\x8fD\xe3\x8a\xe5\xa69V\xbe'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:pippo@tardis.cuhorxnidu3b.us-west-2.rds.amazonaws.com/tardis_base'
db = SQLAlchemy(app)

class User(db.Model):
    iduser = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(200), nullable=True)
    date_ins = db.Column(db.DateTime, nullable=True)
    date_ult_mod = db.Column(db.DateTime, nullable=True)
    token_expire = db.Column(db.String(200), nullable=True)
    user_log = db.relationship('user_logs', backref='user', lazy=True)

class user_logs(db.Model):
    idlog = db.Column(db.Integer, primary_key=True)
    usrid_type_op = db.Column(db.Integer, primary_key=False)
    date_log_stamp = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.String(200), nullable=True)
    iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=True)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/duke')
def duke():
    users = User.query.all()
    users_log = user_logs.query.all()
    return render_template('duke.html', users=users)

@app.route('/duke', methods=['POST'])
def duke_post():
    email = request.form.get('user_mail')
    #return render_template('duke.html', user=user)

    duke_post = User(email=email)
    db.session.add(duke_post)
    db.session.commit()

    usrid_type_op = 2
    #return render_template('duke.html', user=user)
    datelognowtime = datetime.now()
    duke_post = user_logs(usrid_type_op=usrid_type_op, date_log_stamp=datelognowtime)
    db.session.add(duke_post)
    db.session.commit()

    return duke() 

if __name__== "__main__":
    app.run(debug=True)
