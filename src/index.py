import psycopg2
from psycopg2 import Error, connect
from flask import Flask, redirect, url_for, render_template, request, session

# initiating the flask app
app = Flask(__name__)

# not necessary (just there)
app.secret_key = "hello"


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if request.form["proceed-submit"] == "login-flag":
            return redirect(url_for("login"))
        elif request.form["proceed-submit"] == "signup-flag":
            return redirect(url_for("signup"))
    else:
        return render_template("welcome.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return redirect(url_for("home"))
    else:
        return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        option = request.form["name"]
        if option == "generalPublic":
            return redirect(url_for("general_public_signup"))
        elif option == "incharge":
            return redirect(url_for("incharge_signup"))
        elif option == "doctor":
            return redirect(url_for("doctor_signup"))
    else:
        return render_template("signup.html")


@app.route("/signup/general-public", methods=["POST", "GET"])
def general_public_signup():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        address = request.form.get("address")
        age = int(request.form.get("age"))
        aadhar_no = request.form.get("aadhar")

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        # create a cursor to perform database operations
        cur = connection.cursor()

        insert_statement = f"INSERT INTO GENERAL_PUBLIC VALUES ('{name}', '{phone}', '{email}', '{address}', {age}, '{aadhar_no}')"

        # executing an SQL query
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()

        return redirect(url_for("home"))
    else:
        return render_template("general_public_signup.html")


@app.route("/signup/doctor", methods=["POST", "GET"])
def doctor_signup():
    if request.method == "POST":
        domain = request.form.get("domain")
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        hospital_address = request.form.get("hospitalAddress")
        certificate_no = request.form.get("certificateNo")

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        # create a cursor to perform database operations
        cur = connection.cursor()

        insert_statement = f"INSERT INTO DOCTORS VALUES ('{domain}', '{name}', '{phone}', '{email}', '{hospital_address}', '{certificate_no}')"

        # executing an SQL query
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()
        return redirect(url_for("home"))
    else:
        return render_template("doctor_signup.html")


@app.route("/signup/incharge", methods=["POST", "GET"])
def incharge_signup():
    if request.method == "POST":
        option = request.form["name"]
        if option == "animalShelter":
            return redirect(url_for("animal_shelter_signup"))
        elif option == "petShop":
            return redirect(url_for("pet_shop_signup"))
        elif option == "zoo":
            return redirect(url_for("zoo_signup"))
    else:
        return render_template("incharge_signup.html")


@app.route("/signup/incharge/animal_shelter", methods=["POST", "GET"])
def animal_shelter_signup():
    if request.method == "POST":
        certificate_no = request.form.get("certificateNo")
        no_of_pets = request.form.get("noOfPets")
        address = request.form.get("address")
        phone = request.form.get("phone")
        name = request.form.get("name")
        city = request.form.get("city")

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        # create a cursor to perform database operations
        cur = connection.cursor()

        insert_statement = f"INSERT INTO ANIMAL_SHELTER VALUES ('{certificate_no}', {no_of_pets}, '{address}', '{phone}', '{name}', '{city}')"

        # executing an SQL query
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()

        return redirect(url_for("home"))
    else:
        return render_template("animal_shelter_signup.html")


@app.route("/signup/incharge/pet_shop", methods=["POST", "GET"])
def pet_shop_signup():
    if request.method == "POST":
        certificate_no = request.form.get("certificateNo")
        no_of_pets = request.form.get("noOfPets")
        address = request.form.get("address")
        phone = request.form.get("phone")
        name = request.form.get("name")
        city = request.form.get("city")

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        # create a cursor to perform database operations
        cur = connection.cursor()

        insert_statement = f"INSERT INTO PET_SHOP VALUES ({no_of_pets}, '{certificate_no}', '{phone}', '{name}', '{address}', '{city}')"

        # executing an SQL query
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()

        return redirect(url_for("home"))
    else:
        return render_template("pet_shop_signup.html")


@app.route("/signup/incharge/zoo", methods=["POST", "GET"])
def zoo_signup():
    if request.method == "POST":
        id = request.form.get("id")
        name = request.form.get("name")
        address = request.form.get("address")
        phone = request.form.get("phone")
        no_of_animals = request.form.get("noOfAnimals")
        visiting_hours = request.form.get("visitingHours")

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        # create a cursor to perform database operations
        cur = connection.cursor()

        insert_statement = f"INSERT INTO ZOOS VALUES ('{id}', '{name}', '{address}', '{phone}', {no_of_animals}, '{visiting_hours}')"

        # executing an SQL query
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()

        return redirect(url_for("home"))
    else:
        return render_template("zoo_signup.html")


app.run(debug=True)
