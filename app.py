from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    with app.app_context():
        notes = Note.query.all()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    text = request.form['text']
    with app.app_context():
        note = Note(text=text)
        db.session.add(note)
        db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['GET'])
def delete_note(id):
    with app.app_context():
        note = Note.query.get(id)
        db.session.delete(note)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
