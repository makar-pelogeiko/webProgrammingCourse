from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Users(db.Model):
    name = db.Column(db.String(120), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(120), nullable=True)
    vkid = db.Column(db.String(120), unique=True, nullable=True)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow )

    def __repr__(self):
        return f'<User {self.name}>'

@app.route("/")
def index_page():
	return render_template('index.html')

@app.route("/personalPage")
def personalPage():
	return render_template('personalPage.html')

@app.route("/login_registration", methods=('GET', 'POST'))
def email_login():
    if request.method == 'POST':
        try:
            userEmail = request.form['email']
            #userPassword = generate_password_hash(request.form['password'])
            userPassword = request.form['password']
            print(request.form['password'])
            our_user = Users.query.filter_by(email=userEmail, password=userPassword).first()
            if our_user != None:
                print(f"{userEmail} found")
                return render_template('personalPage.html', user=our_user.name)
            else:
                print("jack IS NOT found")
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            print("Ошибка при поиске пользователя БД")
    return redirect(url_for('index_page')) #можно написать функцию index_page с аргументами??

@app.route("/email_registration", methods=('GET', 'POST'))
def email_registration():
    if request.method== 'POST':
        try:
            email = request.form['InputEmail']
            name = request.form['InputName']
            #hash = generate_password_hash(request.form['InputPassword'])
            hash = request.form['InputPassword']
            user = Users(email=email, password=hash, name=name)
            print(request.form['InputPassword'])
            print(hash)
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            print(error)
            print("Ошибка при добавлении пользователя в БД")
    return redirect(url_for('index_page'))
	
if __name__ == "__main__":
    app.run(debug=True, port=5000)
