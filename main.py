from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CREATE TABLE
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/all")
def get_all_cafes():
    cafes = db.session.query(Cafe).all()
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])

@app.route("/")
def index():
    cafes = db.session.query(Cafe).all()
    return render_template("index.html", cafes=cafes)

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        name = request.form.get('name')
        url_map = request.form.get('url_map')
        url_image = request.form.get('url_image')
        location = request.form.get('location')
        has_sockets = request.form.get('has_sockets')
        has_toilet = request.form.get('has_toilet')
        can_take_calls = request.form.get('can_take_calls')
        has_wifi = request.form.get('has_wifi')
        seats = request.form.get('seats')
        coffee_price = request.form.get('coffee_price')

        if has_sockets == "has_sockets":
            has_sockets = True
        else:
            has_sockets = False

        if has_toilet == "has_toilet":
            has_toilet = True
        else:
            has_toilet = False

        if can_take_calls == "can_take_calls":
            can_take_calls = True
        else:
            can_take_calls = False

        if has_wifi == "has_wifi":
            has_wifi = True
        else:
            has_wifi = False

        new_coffee = Cafe(
            name = name,
            map_url = url_map,
            img_url = url_image,
            location = location,
            seats = seats,
            has_toilet = has_toilet,
            has_wifi = has_wifi,
            has_sockets = has_sockets,
            can_take_calls = can_take_calls,
            coffee_price = coffee_price
        )

        db.session.add(new_coffee)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True)