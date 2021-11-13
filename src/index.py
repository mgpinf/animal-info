import psycopg2
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
        option = request.form["name"]
        if option == "generalPublic":
            return redirect(url_for("general_public_login"))
        elif option == "doctor":
            return redirect(url_for("doctor_login"))
        elif option == "incharge":
            return redirect(url_for("incharge_login"))
    else:
        return render_template("login.html")


@app.route("/login/general-public", methods=["POST", "GET"])
def general_public_login():
    if request.method == "POST":
        aadhar = "postgres"
        password = "2020"
        session["general_public_login_credential"] = (aadhar, password)
        return redirect(url_for("general_public_login_select"))
    else:
        return render_template("login/general_public.html")


@app.route("/login/general-public/select", methods=["POST", "GET"])
def general_public_login_select():
    if request.method == "POST":
        return redirect(url_for("home"))
    else:
        aadhar, password = session["general_public_login_credential"]
        connection = psycopg2.connect(
            user=aadhar, password=password, database="project"
        )
        cur = connection.cursor()

        select_statement = f"SELECT * FROM ANIMAL WHERE animal_adopted = false"
        cur.execute(select_statement)

        results = cur.fetchall()

        cur.execute(f"{select_statement} LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        connection.commit()
        connection.close()
        return render_template(
            "login/general_public/select.html",
            colnames=colnames,
            results=results,
        )


@app.route("/login/doctor", methods=["POST", "GET"])
def doctor_login():
    if request.method == "POST":
        certificate_no = "postgres"
        password = "2020"
        session["doctor_login_credential"] = (certificate_no, password)
        return redirect(url_for("doctor_login_table"))
    else:
        return render_template("login/doctor.html")


@app.route("/login/doctor/table", methods=["POST", "GET"])
def doctor_login_table():
    if request.method == "POST":
        session["doctor_login_table"] = request.form["name"]
        if session["doctor_login_table"] == "animalDiseaseHistory":
            return redirect(url_for("doctor_login_animal_disease_history_select"))
        else:
            return redirect(url_for("doctor_login_operation"))
    else:
        return render_template("login/doctor/table.html")


@app.route("/login/doctor/operation", methods=["POST", "GET"])
def doctor_login_operation():
    if request.method == "POST":
        table = session["doctor_login_table"]
        operation = request.form["name"]
        if table == "animalTypeCare":
            if operation == "select":
                return redirect(url_for("doctor_login_animal_type_care_select"))
            elif operation == "update":
                return redirect(url_for("doctor_login_animal_type_care_update"))
            elif operation == "insert":
                return redirect(url_for("doctor_login_animal_type_care_insert"))
        elif table == "queryAnswers":
            if operation == "select":
                return redirect(url_for("doctor_login_query_answers_select"))
            elif operation == "update":
                return redirect(url_for("doctor_login_query_answers_update"))
            elif operation == "insert":
                return redirect(url_for("doctor_login_query_answers_insert"))
    else:
        return render_template("login/doctor/operation.html")


@app.route("/login/doctor/animal-disease-history/select", methods=["POST", "GET"])
def doctor_login_animal_disease_history_select():
    if request.method == "POST":
        return redirect(url_for("home"))
    else:
        certificate_no, password = session["doctor_login_credential"]
        connection = psycopg2.connect(
            user=certificate_no, password=password, database="project"
        )
        cur = connection.cursor()

        select_statement = f"SELECT animal_animal_disease_history_animal_disease_name, animal_animal_disease_history_animal_id, animal_animal_disease_history_animal_disease_no_of_months FROM ANIMAL_ANIMAL_DISEASE_HISTORY"
        cur.execute(select_statement)

        results = cur.fetchall()

        cur.execute(f"{select_statement} LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        connection.commit()
        connection.close()
        return render_template(
            "login/doctor/animal_disease_history/select.html",
            colnames=colnames,
            results=results,
        )


@app.route("/login/doctor/animal-disease-history/insert", methods=["POST", "GET"])
def doctor_login_animal_disease_history_insert():
    if request.method == "POST":
        animal_disease_name = request.form.get("animalDiseaseName")
        animal_id = request.form.get("animalId")
        animal_disease_no_of_months = int(request.form.get("animalDiseaseNoOfMonths"))
        animal_disease_history_genral_public_aadhar = request.form.get(
            "animalDiseaseHistoryGeneralPublicAadhar"
        )
        pet_shop_certificate_no = request.form.get("petShopCertificateNo")
        animal_shelter_certificate_no = request.form.get("animalShelterCertificateNo")
        zoo_id = request.form.get("zooId")

        if animal_disease_history_genral_public_aadhar == "":
            animal_disease_history_genral_public_aadhar = "NULL"
        else:
            animal_disease_history_genral_public_aadhar = (
                "'" + animal_disease_history_genral_public_aadhar + "'"
            )

        if pet_shop_certificate_no == "":
            pet_shop_certificate_no = "NULL"
        else:
            pet_shop_certificate_no = "'" + pet_shop_certificate_no + "'"

        if animal_shelter_certificate_no == "":
            animal_shelter_certificate_no = "NULL"
        else:
            animal_shelter_certificate_no = "'" + animal_shelter_certificate_no + "'"

        if zoo_id == "":
            zoo_id = "NULL"
        else:
            zoo_id = "'" + zoo_id + "'"

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO ANIMAL_ANIMAL_DISEASE_HISTORY VALUES ('{animal_disease_name}', '{animal_id}', {animal_disease_no_of_months}, {animal_disease_history_genral_public_aadhar}, {pet_shop_certificate_no}, {animal_shelter_certificate_no}, {zoo_id})"
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()
        return redirect(url_for("home"))
    else:
        return render_template("login/doctor/animal_disease_history/insert.html")


@app.route("/login/doctor/animal-disease-history/update", methods=["POST", "GET"])
def doctor_login_animal_disease_history_update():
    if request.method == "POST":
        animal_disease_name = request.form.get("animalDiseaseName")
        animal_id = request.form.get("animalId")
        animal_disease_no_of_months = request.form.get("animalDiseaseNoOfMonths")
        animal_disease_history_genral_public_aadhar = request.form.get(
            "animalDiseaseHistoryGeneralPublicAadhar"
        )
        pet_shop_certificate_no = request.form.get("petShopCertificateNo")
        animal_shelter_certificate_no = request.form.get("animalShelterCertificateNo")
        zoo_id = request.form.get("zooId")

        if animal_disease_history_genral_public_aadhar == "":
            animal_disease_history_genral_public_aadhar = "NULL"
        else:
            animal_disease_history_genral_public_aadhar = (
                "'" + animal_disease_history_genral_public_aadhar + "'"
            )

        if pet_shop_certificate_no == "":
            pet_shop_certificate_no = "NULL"
        else:
            pet_shop_certificate_no = "'" + pet_shop_certificate_no + "'"

        if animal_shelter_certificate_no == "":
            animal_shelter_certificate_no = "NULL"
        else:
            animal_shelter_certificate_no = "'" + animal_shelter_certificate_no + "'"

        if zoo_id == "":
            zoo_id = "NULL"
        else:
            zoo_id = "'" + zoo_id + "'"

        values = (
            animal_disease_name,
            animal_id,
            animal_disease_no_of_months,
            animal_disease_history_genral_public_aadhar,
            pet_shop_certificate_no,
            animal_shelter_certificate_no,
            zoo_id,
        )

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        cur = connection.cursor()
        cur.execute("SELECT * FROM ANIMAL_ANIMAL_DISEASE_HISTORY LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        value_string = ""

        for i in range(2):
            value_string += f"{colnames[i]}='{values[i]}',"
        for i in range(2, 6):
            value_string += f"{colnames[i]}={values[i]},"
        i += 1
        value_string += (
            f"{colnames[i]}={values[i]} WHERE {colnames[1]} = '{animal_id}';"
        )

        update_statement = f"UPDATE ANIMAL_ANIMAL_DISEASE_HISTORY SET {value_string}"
        cur.execute(update_statement)

        cur.close()
        connection.commit()
        connection.close()
        return redirect(url_for("home"))
    else:
        return render_template("login/doctor/animal_disease_history/update.html")


@app.route("/login/doctor/animal-type-care/select", methods=["POST", "GET"])
def doctor_login_animal_type_care_select():
    if request.method == "POST":
        return redirect(url_for("home"))
    else:
        certificate_no, password = session["doctor_login_credential"]
        connection = psycopg2.connect(
            user=certificate_no, password=password, database="project"
        )
        cur = connection.cursor()

        select_statement = f"SELECT animal_type_animal_type_care_animal_type_care, animal_type_animal_type_care_animal_type_breed FROM ANIMAL_TYPE_ANIMAL_TYPE_CARE"
        cur.execute(select_statement)

        results = cur.fetchall()

        cur.execute(f"{select_statement} LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        connection.commit()
        connection.close()
        return render_template(
            "login/doctor/animal_type_care/select.html",
            colnames=colnames,
            results=results,
        )


@app.route("/login/doctor/animal-type-care/insert", methods=["POST", "GET"])
def doctor_login_animal_type_care_insert():
    if request.method == "POST":
        id = request.form.get("id")
        type_of_care = request.form.get("typeOfCare")
        breed = request.form.get("breed")

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO ANIMAL_TYPE_ANIMAL_TYPE_CARE VALUES ('{id}', '{type_of_care}', '{breed}')"
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()
        return redirect(url_for("home"))
    else:
        return render_template("login/doctor/animal_type_care/insert.html")


@app.route("/login/doctor/animal-type-care/update", methods=["POST", "GET"])
def doctor_login_animal_type_care_update():
    if request.method == "POST":
        id = request.form.get("id")
        type_of_care = request.form.get("typeOfCare")
        breed = request.form.get("breed")

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        cur = connection.cursor()

        cur.execute("SELECT * FROM ANIMAL_TYPE_ANIMAL_TYPE_CARE LIMIT 0")
        colnames = [desc[0] for desc in cur.description]
        value_string = ""

        values = (id, type_of_care, breed)

        for i in range(2):
            value_string += f"{colnames[i]}='{values[i]}',"
        i += 1

        value_string += f"{colnames[i]}='{values[i]}' WHERE {colnames[0]} = '{id}';"

        update_statement = f"UPDATE ANIMAL_TYPE_ANIMAL_TYPE_CARE SET {value_string}"
        cur.execute(update_statement)

        cur.close()
        connection.commit()
        connection.close()

        return redirect(url_for("home"))
    else:
        return render_template("login/doctor/animal_type_care/update.html")


@app.route("/login/doctor/query-answer/select", methods=["POST", "GET"])
def doctor_login_query_answers_select():
    if request.method == "POST":
        return redirect(url_for("home"))
    else:
        certificate_no, password = session["doctor_login_credential"]
        connection = psycopg2.connect(
            user=certificate_no, password=password, database="project"
        )
        cur = connection.cursor()

        select_statement = f"SELECT queries_query_question, queries_query_answer_query_answer, queries_query_answer_query_answered_by FROM QUERIES, QUERIES_QUERY_ANSWER WHERE  queries_query_id = queries_query_answer_query_id"
        cur.execute(select_statement)

        results = cur.fetchall()

        cur.execute(f"{select_statement} LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        connection.commit()
        connection.close()
        return render_template(
            "login/doctor/query_answer/select.html",
            colnames=colnames,
            results=results,
        )


@app.route("/login/doctor/query-answer/insert", methods=["POST", "GET"])
def doctor_login_query_answers_insert():
    if request.method == "POST":
        id = request.form.get("id")
        query_answer = request.form.get("queryAnswer")
        query_id = request.form.get("queryId")
        query_answered_by = request.form.get("queryAnsweredBy")

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO QUERIES_QUERY_ANSWER VALUES ('{id}', '{query_answer}', '{query_id}', '{query_answered_by}')"
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()

        return redirect(url_for("home"))
    else:
        return render_template(
            "login/doctor/query_answer/insert.html",
        )


@app.route("/login/doctor/query-answer/update", methods=["POST", "GET"])
def doctor_login_query_answers_update():
    if request.method == "POST":
        id = request.form.get("id")
        query_answer = request.form.get("queryAnswer")
        query_id = request.form.get("queryId")
        query_answered_by = request.form.get("queryAnsweredBy")

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        cur = connection.cursor()

        cur.execute("SELECT * FROM QUERIES_QUERY_ANSWER LIMIT 0")
        colnames = [desc[0] for desc in cur.description]
        value_string = ""

        values = (id, query_answer, query_id, query_answered_by)

        for i in range(3):
            value_string += f"{colnames[i]}='{values[i]}',"
        i += 1

        value_string += f"{colnames[i]}='{values[i]}' WHERE {colnames[0]} = '{id}';"

        update_statement = f"UPDATE QUERIES_QUERY_ANSWER SET {value_string}"
        cur.execute(update_statement)

        cur.close()
        connection.commit()
        connection.close()

        return redirect(url_for("home"))
    else:
        return render_template(
            "login/doctor/query_answer/update.html",
        )


@app.route("/login/incharge", methods=["POST", "GET"])
def incharge_login():
    if request.method == "POST":
        option = request.form["name"]
        if option == "animalShelter":
            return redirect(url_for("incharge_animal_shelter_login"))
        elif option == "petShop":
            return redirect(url_for("incharge_pet_shop_login"))
        elif option == "zoo":
            return redirect(url_for("incharge_zoo_login"))
    else:
        return render_template("login/incharge.html")


@app.route("/login/incharge/animal-shelter", methods=["POST", "GET"])
def incharge_animal_shelter_login():
    if request.method == "POST":
        certificate_no = "postgres"
        password = "2020"
        session["incharge_animal_shelter_login_credential"] = (certificate_no, password)
        return redirect(url_for("incharge_animal_shelter_login_operation"))
    else:
        return render_template("login/incharge/animal_shelter.html")


@app.route("/login/incharge/animal-shelter/operation", methods=["POST", "GET"])
def incharge_animal_shelter_login_operation():
    if request.method == "POST":
        operation = request.form["name"]
        if operation == "select":
            return redirect(url_for("incharge_animal_shelter_login_select"))
        elif operation == "update":
            return redirect(url_for("incharge_animal_shelter_login_update"))
        elif operation == "insert":
            return redirect(url_for("incharge_animal_shelter_login_insert"))
    else:
        return render_template("login/incharge/animal_shelter/operation.html")


@app.route("/login/incharge/animal-shelter/select", methods=["POST", "GET"])
def incharge_animal_shelter_login_select():
    if request.method == "POST":
        return redirect(url_for("home"))
    else:
        certificate_no, password = session["incharge_animal_shelter_login_credential"]
        connection = psycopg2.connect(
            user=certificate_no, password=password, database="project"
        )
        cur = connection.cursor()

        select_statement = f"SELECT * FROM ANIMAL_SHELTER"
        cur.execute(select_statement)

        results = cur.fetchall()

        cur.execute(f"{select_statement} LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        connection.commit()
        connection.close()
        return render_template(
            "login/incharge/animal_shelter/select.html",
            colnames=colnames,
            results=results,
        )


@app.route("/login/incharge/animal-shelter/insert", methods=["POST", "GET"])
def incharge_animal_shelter_login_insert():
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

        cur = connection.cursor()

        insert_statement = f"INSERT INTO ANIMAL_SHELTER VALUES ('{certificate_no}', {no_of_pets}, '{address}', '{phone}', '{name}', '{city}')"
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()

        return redirect(url_for("home"))
    else:
        return render_template(
            "login/incharge/animal_shelter/insert.html",
        )


@app.route("/login/incharge/animal-shelter/update", methods=["POST", "GET"])
def incharge_animal_shelter_login_update():
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

        cur = connection.cursor()

        cur.execute("SELECT * FROM ANIMAL_SHELTER LIMIT 0")
        colnames = [desc[0] for desc in cur.description]
        value_string = ""

        values = (certificate_no, no_of_pets, address, phone, name, city)

        value_string = f"{colnames[0]}='{values[0]}',{colnames[1]}={values[1]},"
        for i in range(2, 5):
            value_string += f"{colnames[i]}='{values[i]}',"
        i += 1
        value_string += (
            f"{colnames[i]}='{values[i]}' WHERE {colnames[0]} = '{certificate_no}';"
        )

        update_statement = f"UPDATE ANIMAL_SHELTER SET {value_string}"

        print(update_statement)
        cur.execute(update_statement)

        cur.close()
        connection.commit()
        connection.close()

        return redirect(url_for("home"))
    else:
        return render_template(
            "login/incharge/animal_shelter/update.html",
        )


@app.route("/login/incharge/pet-shop", methods=["POST", "GET"])
def incharge_pet_shop_login():
    if request.method == "POST":
        certificate_no = "incharge_pet_shop" + request.form.get("certificateNo")
        password = request.form.get("password")
        certificate_no = "postgres"
        password = "2020"
        session["incharge_pet_shop_login_credential"] = (certificate_no, password)
        return redirect(url_for("incharge_pet_shop_login_operation"))
    else:
        return render_template("login/incharge/pet_shop.html")


@app.route("/login/incharge/pet-shop/operation", methods=["POST", "GET"])
def incharge_pet_shop_login_operation():
    if request.method == "POST":
        operation = request.form["name"]
        if operation == "select":
            return redirect(url_for("incharge_pet_shop_login_select"))
        elif operation == "update":
            return redirect(url_for("incharge_pet_shop_login_update"))
        elif operation == "insert":
            return redirect(url_for("incharge_pet_shop_login_insert"))
    else:
        return render_template("login/incharge/pet_shop/operation.html")


@app.route("/login/incharge/pet-shop/select", methods=["POST", "GET"])
def incharge_pet_shop_login_select():
    if request.method == "POST":
        return redirect(url_for("home"))
    else:
        certificate_no, password = session["incharge_pet_shop_login_credential"]
        connection = psycopg2.connect(
            user=certificate_no, password=password, database="project"
        )
        cur = connection.cursor()

        select_statement = f"SELECT * FROM PET_SHOP"
        cur.execute(select_statement)

        results = cur.fetchall()

        cur.execute(f"{select_statement} LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        connection.commit()
        connection.close()
        return render_template(
            "login/incharge/pet_shop/select.html",
            colnames=colnames,
            results=results,
        )


@app.route("/login/incharge/pet-shop/insert", methods=["POST", "GET"])
def incharge_pet_shop_login_insert():
    if request.method == "POST":
        no_of_pets = request.form.get("noOfPets")
        certificate_no = request.form.get("certificateNo")
        phone = request.form.get("phone")
        name = request.form.get("name")
        address = request.form.get("address")
        city = request.form.get("city")

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO PET_SHOP VALUES ('{no_of_pets}', {certificate_no}, '{phone}', '{name}', '{address}', '{city}')"
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()

        return redirect(url_for("home"))
    else:
        return render_template(
            "login/incharge/pet_shop/insert.html",
        )


@app.route("/login/incharge/pet-shop/update", methods=["POST", "GET"])
def incharge_pet_shop_login_update():
    if request.method == "POST":
        no_of_pets = request.form.get("noOfPets")
        certificate_no = request.form.get("certificateNo")
        phone = request.form.get("phone")
        name = request.form.get("name")
        address = request.form.get("address")
        city = request.form.get("city")

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        cur = connection.cursor()

        cur.execute("SELECT * FROM PET_SHOP LIMIT 0")
        colnames = [desc[0] for desc in cur.description]
        value_string = ""

        values = (no_of_pets, certificate_no, phone, name, address, city)

        value_string = f"{colnames[0]}={values[0]},{colnames[1]}='{values[1]}',"
        for i in range(2, 5):
            value_string += f"{colnames[i]}='{values[i]}',"
        i += 1
        value_string += (
            f"{colnames[i]}='{values[i]}' WHERE {colnames[1]} = '{certificate_no}';"
        )

        update_statement = f"UPDATE PET_SHOP SET {value_string}"

        print(update_statement)
        cur.execute(update_statement)

        cur.close()
        connection.commit()
        connection.close()

        return redirect(url_for("home"))
    else:
        return render_template(
            "login/incharge/pet_shop/update.html",
        )


@app.route("/login/incharge/zoo", methods=["POST", "GET"])
def incharge_zoo_login():
    if request.method == "POST":
        id = "postgres"
        password = "2020"
        session["incharge_zoo_login_credential"] = (id, password)
        return redirect(url_for("incharge_zoo_login_operation"))
    else:
        return render_template("login/incharge/zoo.html")


@app.route("/login/incharge/zoo/operation", methods=["POST", "GET"])
def incharge_zoo_login_operation():
    if request.method == "POST":
        operation = request.form["name"]
        if operation == "select":
            return redirect(url_for("incharge_zoo_login_select"))
        elif operation == "update":
            return redirect(url_for("incharge_zoo_login_update"))
        elif operation == "insert":
            return redirect(url_for("incharge_zoo_login_insert"))
    else:
        return render_template("login/incharge/zoo/operation.html")


@app.route("/login/incharge/zoo/select", methods=["POST", "GET"])
def incharge_zoo_login_select():
    if request.method == "POST":
        return redirect(url_for("home"))
    else:
        id, password = session["incharge_zoo_login_credential"]
        connection = psycopg2.connect(user=id, password=password, database="project")
        cur = connection.cursor()

        select_statement = f"SELECT * FROM ZOOS"
        cur.execute(select_statement)

        results = cur.fetchall()

        cur.execute(f"{select_statement} LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        connection.commit()
        connection.close()
        return render_template(
            "login/incharge/zoo/select.html",
            colnames=colnames,
            results=results,
        )


@app.route("/login/incharge/zoo/insert", methods=["POST", "GET"])
def incharge_zoo_login_insert():
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

        cur = connection.cursor()

        insert_statement = f"INSERT INTO ZOOS VALUES ('{id}', '{name}', '{address}', '{phone}', {no_of_animals}, '{visiting_hours}')"
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()
        return redirect(url_for("home"))
    else:
        return render_template(
            "login/incharge/zoo/insert.html",
        )


@app.route("/login/incharge/zoo/update", methods=["POST", "GET"])
def incharge_zoo_login_update():
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

        cur = connection.cursor()

        cur.execute("SELECT * FROM ZOOS LIMIT 0")
        colnames = [desc[0] for desc in cur.description]
        value_string = ""

        values = (id, name, address, phone, no_of_animals, visiting_hours)

        for i in range(4):
            value_string += f"{colnames[i]}='{values[i]}',"
        i += 1

        value_string += f"{colnames[i]}={values[i]},"

        i += 1
        value_string += f"{colnames[i]}='{values[i]}' WHERE {colnames[0]} = '{id}';"

        update_statement = f"UPDATE ZOOS SET {value_string}"

        cur.execute(update_statement)

        cur.close()
        connection.commit()
        connection.close()

        return redirect(url_for("home"))
    else:
        return render_template(
            "login/incharge/zoo/update.html",
        )


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
        password = request.form.get("password")

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO GENERAL_PUBLIC VALUES ('{name}', '{phone}', '{email}', '{address}', {age}, '{aadhar_no}')"
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()

        return redirect(url_for("home"))
    else:
        return render_template("signup/general_public.html")


@app.route("/signup/doctor", methods=["POST", "GET"])
def doctor_signup():
    if request.method == "POST":
        domain = request.form.get("domain")
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        hospital_address = request.form.get("hospitalAddress")
        certificate_no = request.form.get("certificateNo")
        password = request.form.get("password")

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO DOCTORS VALUES ('{domain}', '{name}', '{phone}', '{email}', '{hospital_address}', '{certificate_no}')"
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()
        return redirect(url_for("home"))
    else:
        return render_template("signup/doctor.html")


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
        return render_template("signup/incharge.html")


@app.route("/signup/incharge/animal_shelter", methods=["POST", "GET"])
def animal_shelter_signup():
    if request.method == "POST":
        certificate_no = request.form.get("certificateNo")
        no_of_pets = request.form.get("noOfPets")
        address = request.form.get("address")
        phone = request.form.get("phone")
        name = request.form.get("name")
        city = request.form.get("city")
        password = request.form.get("password")

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO ANIMAL_SHELTER VALUES ('{certificate_no}', {no_of_pets}, '{address}', '{phone}', '{name}', '{city}')"
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()

        return redirect(url_for("home"))
    else:
        return render_template("signup/animal_shelter.html")


@app.route("/signup/incharge/pet_shop", methods=["POST", "GET"])
def pet_shop_signup():
    if request.method == "POST":
        certificate_no = request.form.get("certificateNo")
        no_of_pets = request.form.get("noOfPets")
        address = request.form.get("address")
        phone = request.form.get("phone")
        name = request.form.get("name")
        city = request.form.get("city")
        password = request.form.get("password")

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO PET_SHOP VALUES ({no_of_pets}, '{certificate_no}', '{phone}', '{name}', '{address}', '{city}')"
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()

        return redirect(url_for("home"))
    else:
        return render_template("signup/pet_shop.html")


@app.route("/signup/incharge/zoo", methods=["POST", "GET"])
def zoo_signup():
    if request.method == "POST":
        id = request.form.get("id")
        name = request.form.get("name")
        address = request.form.get("address")
        phone = request.form.get("phone")
        no_of_animals = request.form.get("noOfAnimals")
        visiting_hours = request.form.get("visitingHours")
        password = request.form.get("password")

        connection = psycopg2.connect(
            user="postgres", password="2020", database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO ZOOS VALUES ('{id}', '{name}', '{address}', '{phone}', {no_of_animals}, '{visiting_hours}')"
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()

        return redirect(url_for("home"))
    else:
        return render_template("signup/zoo.html")


app.run(debug=True)
