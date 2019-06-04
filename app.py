from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/duke')
def duke():
    return render_template('duke.html')

if __name__== "__main__":
    app.run(debug=True)
