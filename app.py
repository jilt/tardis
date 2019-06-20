from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms import Form, StringField, validators
from flask_wtf.csrf import CSRFProtect
#from flask.ext.dropbox import Dropbox, DropboxBlueprint
import dropbox
import posixpath
from dropbox.exceptions import ApiError
import configparser



    
app = Flask(__name__)
dukee = 'Email'
config = configparser.ConfigParser()
config.read('example.cfg')

app.secret_key = '\x89s\xed\x9e\xf7\x9b\xf5\xd4n\xab\xa1\x8e\x08\x95\xfd\x8fD\xe3\x8a\xe5\xa69V\xbe'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://'+ config['MySqlConnection']['username']+':'+config['MySqlConnection']['pwd']+'@'+ config['MySqlConnection']['url']
db = SQLAlchemy(app)
csrf = CSRFProtect(app)



#Model
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

class user_logs_op_type(db.Model):
    id_op_type = db.Column(db.Integer, primary_key=True)
    op_description = db.Column(db.String(200), nullable=True)

#Forms
class RegistrationForm(Form):
    user_mail = StringField(dukee,[validators.Length(min=4, max=25)])


#URL
@app.route('/')
def index():
    
    def process_folder_entries(current_state, entries):
        for entry in entries:
            if isinstance(entry, dropbox.files.DeletedMetadata):
                current_state[entry.path_lower] = entry
                print(entry)
            elif isinstance(entry, dropbox.files.DeletedMetadata):
                current_state.pop(entry.path_lower, None) # ignore KeyError if missing
                
        return current_state
    def path_exists(path):
        try:
            dbx.files_get_metadata(path)
            return True
        except ApiError as e:
            if e.error.get_path().is_not_found():
                return False
            raise
    print("Scanning for files......")
    dbx = dropbox.Dropbox("MXKKw4wYA7cAAAAAAAADHBryaFe3ycl-hzQODtzPd2QqXScQtflFhIld0zLN4sUq")

    result = dbx.files_list_folder(path="/prova", include_deleted = True, recursive = False)
    files = process_folder_entries({}, result.entries)
    

    # check for and collect any additional entries
    
    while result.has_more:
        print("Collecting additional files...""""  """)
        result = dbx.files_list_folder_continue(result.cursor)
        files = process_folder_entries(files, result.entries)
    #print(files)

    for entry in files.values():
        # use modified time of file to build destination path
        destination_path = "/_Expenses"

    # check to see if we need to create the destination folder
        if not path_exists(destination_path):
            print("Creating folder: {}".format(destination_path))
            dbx.files_create_folder(destination_path)

        print("Moving {} to {}".format(entry.path_lower, destination_path))
        
        destination_path = posixpath.join(destination_path+"/")
        return render_template('index.html', files=files) # Agnes da qui va in errore....!!!
        revs = dropbox.files.ListRevisionsMode(entry.path_lower)
        #revisions = dbx.files_list_revisions(entry.path_lower, mode=revs.id , limit=1)
        dbx.files_restore(destination_path, revs.id)
    print("Complete!")

    return render_template('index.html', files=files)

@app.route('/duke', methods=['GET', 'POST'])
def duke():
    form = RegistrationForm(request.form)
    if(request.method == 'POST'):
        form = RegistrationForm(request.form)
        if(form.validate()):
            email = request.form.get('user_mail')
            if user_exists(email):
                e = "errore: questa email è già stata utilizzata, se lo hai fatto tu clicca il seguente link per loggarti o fare il recupero della password. ALtrimenti cambia email!"
                return render_template('error.html', e=e)
            else:
                duke_post = User(email=email)    
                db.session.add(duke_post)
                db.session.commit()
                usrid_type_op = 3
                #return render_template('duke.html', user=user)
                datelognowtime = datetime.now()
                duke_post = user_logs(usrid_type_op=usrid_type_op, date_log_stamp=datelognowtime)
                db.session.add(duke_post)
                db.session.commit()
        else:
            e = 'errore: i dati inseriti non sono validi'
            return render_template('error.html', e=e)
    else:
        users = User.query.all()
        user_log = user_logs.query.all()
        user_logs_type = user_logs_op_type.query.all()
        return render_template('duke.html', users=users, user_logs_type=user_logs_type, form=form)

def user_exists(e_mail):
    if(User.query.filter(User.email == e_mail).first() is not None):
        return True
    else:
        return False

if __name__== "__main__":
    app.run(debug=True)
