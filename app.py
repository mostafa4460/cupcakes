"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

@app.route('/')
def index_page():
    """Shows the index page"""
    return render_template('index.html')

@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns JSON of all cupcakes"""

    all_cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in all_cupcakes]
    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Returns JSON of a specific cupcake"""

    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def add_cupcake():
    """Adds a new cupcake to DB then returns JSON of new cupcake with status_code = 201"""

    cupcake = Cupcake(
        flavor = request.json["flavor"],
        size = request.json["size"],
        rating = request.json["rating"],
        image = request.json["image"]      
    )

    db.session.add(cupcake)
    db.session.commit()
    response = jsonify(cupcake=cupcake.serialize())
    return (response, 201)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Updates a Cupcake record in DB then returns JSON of updated cupcake"""

    cupcake = Cupcake.query.get_or_404(id)
    db.session.query(Cupcake).filter_by(id=id).update(request.json)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Deletes a Cupcake record from DB then returns JSON message"""

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Cupcake was successfully deleted")