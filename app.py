from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vet_clinic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.Date, nullable=False)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.Date, nullable=False)

class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    consultation_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True)

@app.route('/')
def index():
    clients = Client.query.all()
    return render_template('index.html', clients=clients)

@app.route('/add_client', methods=['POST'])
def add_client():
    document = request.form['document']
    surname = request.form['surname']
    first_name = request.form['first_name']
    patronymic = request.form['patronymic']
    birthday = datetime.strptime(request.form['birthday'], '%Y-%m-%d').date()

    new_client = Client(document=document, surname=surname, first_name=first_name, patronymic=patronymic, birthday=birthday)
    db.session.add(new_client)
    db.session.commit()

    flash('Клиент успешно добавлен', 'success')
    return redirect(url_for('index'))

# Добавляем метод удаления клиента
@app.route('/delete_client/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Клиент успешно удален', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
