from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)
app.secret_key = 'key'


# Cafe TABLE Configuration
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






with app.app_context():
    db.create_all()


@app.route("/")
def home():
    all_cafes = Cafe.query.all()
    return render_template("index.html", all_cafes=all_cafes)

@app.route("/add_new_cafe", methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        cafe_name = request.form['name']
        map_url = request.form['map_url']
        img_url = request.form['img_url']
        location = request.form['location']
        has_sockets = int(request.form['has_sockets'])
        has_toilet = int(request.form['has_toilet'])
        has_wifi = int(request.form['has_wifi'])
        can_take_calls = int(request.form['can_take_calls'])
        seats = request.form['seats']
        coffee_price = request.form['coffee_price']

        new_cafe = Cafe(name=cafe_name,
                        map_url=map_url,
                        img_url=img_url,
                        location=location,
                        has_sockets=has_sockets,
                        has_toilet=has_toilet,
                        has_wifi=has_wifi,
                        can_take_calls=can_take_calls,
                        seats=seats,
                        coffee_price=coffee_price)
        db.session.add(new_cafe)
        db.session.commit()
        flash('New cafe added successfully!', 'success')
        return redirect(url_for("home"))
    return render_template('add_cafe.html')

@app.route("/delete_cafe/<int:cafe_id>", methods=["GET", "POST"])
def delete(cafe_id):
    if request.method == 'POST':
        entered_api_key = request.form['apiKey']
        if entered_api_key == app.secret_key:
            cafe_to_delete = Cafe.query.get(cafe_id)
            if cafe_to_delete:
                db.session.delete(cafe_to_delete)
                db.session.commit()
                flash('Cafe Deleted!', 'success')
                return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('delete_cafe.html', cafe_id=cafe_id)


if __name__ == '__main__':
    app.run(debug=True)