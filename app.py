## postgres database stuffie
import os 
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

## eg code, get the actual connection string from vercel 


db=SQLAlchemy(app)

class Neighborhood(db.Model):
   id=db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
   name = db.Column(db.String(100), nullable=False)
   address = db.Column(db.String(1000), unique=True, nullable=False)
   fruit_name = db.Column(db.String(100), nullable=False)
   stock = db.Column(db.Integer)

   # person 
   def __repr__(self):
       return f"<id: {self.id} name: {self.name}, address: {self.address}, fruit name: {self.fruit_name}, number of fruit: {self.stock})>"

@app.route('/test')
def test():
    return 'hello World'

@app.route('/')
def index():
    people = Neighborhood.query.all()
    print(people)
    return render_template('./index.html', people=people)

@app.route('/aboutme/')
def aboutme():
    people = Neighborhood.query.all()
    return render_template('./aboutme.html', people=people)

@app.route('/contactus/')
def contactus():
    people = Neighborhood.query.all()
    return render_template('./contactus.html', people=people)


@app.route('/addfruit', methods=['POST'])
def add_fruit():
   print(request.json)
   name = request.json['name']
   address = request.json['address']
   fruit_name=request.json['fruit_name']
   stock=request.json['stock']
   if name == None or address == None or fruit_name == None or stock == None: 
       return "No 'person_id'", 400
   
   neighborhood = Neighborhood.query.filter_by(id=name).first()

   if neighborhood == None:
       return f"None such person '{name}'", 400
   
   db.session.add(neighborhood)
   db.session.commit()
   return "done", 200


## running flask app thingy 
# export FLASK_APP=app
