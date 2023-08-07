from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(100))
    price = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.name} is ${self.price}'


@app.route('/')
def homepage():
    return '<h1> Hello! Welcome to my api page </h1>'


@app.route('/drinks', methods=['POST', 'GET'])
def get_drinks():
    if request.method == 'POST':
        drink = Drink(name=request.json['name'], description=request.json['description'], price=request.json['price'])
        db.session.add(drink)
        db.session.commit()
        return {'id': drink.id, 'name': drink.name,
                "msg": "drink successfully added"}
    elif request.method == 'GET':
        drinks = Drink.query.all()
        output = []
        for drink in drinks:
            drink_data = {'id':drink.id, 'name':drink.name, 'description': drink.description, 'price':drink.price}
            output.append(drink_data)
        return {'drink': output}
    else:
        return {"msg": 'not a valid method'}


@app.route('/drinks/<id>')
def get_drinksBy_id(id):
    drink = Drink.query.get_or_404(id)
    return {'id':drink.id, 'name':drink.name, 'description': drink.description, 'price':drink.price}


# @app.route('/drinks', methods=['POST'])
# def create_drink():
#     drink = Drink(name=request.json['name'], description=request.json['description'], price=request.json['price'])
#     db.session.add(drink)
#     db.session.commit()
#     return {'id':drink.id, 'name':drink.name}


@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drinks(id):
    drink = Drink.query.get(id)
    if drink is None:
        return "Drink with such id isn't available....please input a valid id"
    db.session.delete(drink)
    db.session.commit()
    return "Drink with such id is now deleted"


@app.route('/drinks/<id>', methods=['PUT'])
def put_drinks(id):
    drink = Drink(name=request.json['name'], description=request.json['description'], price=request.json['price'])
    db.session.add(drink)
    db.session.commit()
    return {'id':drink.id, 'name':drink.name}


if __name__ == "__main__":
    app.run(debug=True)