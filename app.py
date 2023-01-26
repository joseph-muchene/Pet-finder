from flask import Flask
from flask import render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
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
    lost = db.Column(db.DateTime(timezone=True),
                     server_default=func.now())
    found = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"{id} {self.name}"


@app.route("/")
def index():
    pets = db.session.execute(db.select(Pet).order_by(Pet.name)).scalars()
    return render_template('index.html', pets=pets)


@app.route('/pet/create', methods=['GET', 'POST'])
def pet_create():
    # print(request.method)
    if request.method == "POST":
        pet = Pet(
            name=request.form["name"],
            age=request.form["age"],
            # lost=request.form["lost"],


        )

        db.session.add(pet)
        db.session.commit()
        # redirect user to homepage
        return redirect(url_for("index", id=pet.id))

    return render_template('create.html')


@app.route("/pet/<int:id>")
def user_detail(id):
    pet = db.get_or_404(Pet, id)
    return render_template("detail.html", pet=pet)


@app.route("/pet/<int:id>/delete", methods=["GET", "POST"])
def pet_delete(id):
    pet = db.get_or_404(Pet, id)

    if request.method == "POST":
        db.session.delete(pet)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("user/delete.html", pet=pet)


@app.route("/pet/<int:id>/update", methods=["GET", "POST"])
def pet_update(id):
    pet = Pet.query.filter_by(id=id).first()

    if request.method == "POST":

        pet.found = bool(request.form["found"].capitalize())
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("update.html", pet=pet)


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
