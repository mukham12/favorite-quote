from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:postgres@localhost/quotes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Quotes(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author = db.Column(db.String(30))
	quote = db.Column(db.String(300))


@app.route('/')
def index():
	result = Quotes.query.all()
	return render_template('index.html', result=result)


@app.route('/quotes')
def quotes():
	return render_template('quotes.html')


@app.route('/process', methods=['POST'])
def process():
	author = request.form['author']
	quote = request.form['quote']
	data = Quotes(author=author, quote=quote)
	db.session.add(data)
	db.session.commit()

	return redirect(url_for('index'))
