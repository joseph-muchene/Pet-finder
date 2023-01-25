from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, DateTime, Boolean
import datetime
app = Flask(__name__)
db = SQLAlchemy()

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///petFinder.db"

# initialize the app with the extension
db.init_app(app)


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    found = Column(Boolean, default=False)

    def __init__(self):
        return f"{id} {self.name}"


@app.route("/")
def index():
    pets = db.session.execute(db.select(Pet).order_by(Pet.name)).scalars()
    return render_template('index.html', pets=pets)


@app.route('/pet/create')
def pet_create():
    if request.method == "POST":
        pet = Pet(
            name=request.form["name"],
            age=request.form["age"],
            created_date=request.form["created_date"],
            found=request.form["found"]

        )

        db.session.add(pet)
        db.session.commit()
        # redirect user to homepage
        return redirect(url_for("detail", id=pet.id))

    return render_template('create.html')


@app.route("/pet/<int:id>")
def user_detail(id):
    pet = db.get_or_404(Pet, id)
    return render_template("detail.html", pet=pet)

    # with app.app_context():
    #     db.create_all()


@app.route("/pet/<int:id>/delete", methods=["GET", "POST"])
def pet_delete(id):
    pet = db.get_or_404(Pet, id)

    if request.method == "POST":
        db.session.delete(pet)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("user/delete.html", pet=pet)


@app.route("/pet/<int:id>/delete", methods=["GET", "POST"])
def pet_update(id):
    pet = Pet.query.filter_by(id=id).first()

    if request.method == "POST":
        pet.found = request.form["found"]
        db.session.commit()
        return redirect(url_for("index.html"))

    return render_template("user/delete.html", pet=pet)


@app.route("/found")
def Found():
    pets = Pet.query.filter_by(found=True)
    return render_template('found.html', pets=pets)


@app.route("/update")
def Update():

    return render_template('update.html')


if __name__ == '__main__':
    app.run(debug=True)
    app.run()
