from flask.helpers import flash
import psycopg2
import smtplib, ssl
from flask import Flask, redirect, url_for, render_template, request, session

port = 465  # for SSL
smtp_server = "smtp.gmail.com"
sender_encrypted_email = "l`mhrgfnvc16?fl`hk-bnl"
sender_encrypted_password = "l`mhrg/8?odrT"
message = """Subject: Hi there
Thank you for signing up. Excited to serve you"""
user_name = "postgres"
user_password = "2020"


def str_inc(string):
    res_string = ""
    for i in string:
        res_string += chr(ord(i) + 1)
    return res_string


sender_email = str_inc(sender_encrypted_email)
sender_decrypted_password = str_inc(sender_encrypted_password)


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
        entered_aadhar = request.form["aadhar"]
        entered_password = request.form["password"]

        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )

        cur = connection.cursor()
        list_of_users_statement = f"SELECT login_public_adhar_no_id FROM LOGIN_PUBLIC"
        cur.execute(list_of_users_statement)

        list_of_users = cur.fetchall()
        list_of_users = [i[0] for i in list_of_users]

        if str(entered_aadhar) not in list_of_users:
            flash("Invalid credentials")
            return redirect(url_for("general_public_login"))

        session["aadhar"] = entered_aadhar

        select_statement = f"SELECT login_public_password FROM LOGIN_PUBLIC WHERE login_public_adhar_no_id = '{entered_aadhar}'"
        cur.execute(select_statement)

        actual_password = cur.fetchone()[0]

        if entered_password == actual_password:
            flash("Successfully logged in")
            return redirect(url_for("general_public_login_operation"))
        else:
            flash("Invalid credentials")
            return redirect(url_for("general_public_login"))
    else:
        return render_template("login/general_public.html")


@app.route("/login/general-public/operation", methods=["POST", "GET"])
def general_public_login_operation():
    if request.method == "POST":
        operation = request.form["name"]
        if operation == "select":
            return redirect(url_for("general_public_login_select"))
        elif operation == "insertQuery":
            return redirect(url_for("general_public_login_insert_query"))
    else:
        return render_template("login/general_public/operation.html")


@app.route("/login/general-public/insert-query", methods=["POST", "GET"])
def general_public_login_insert_query():
    if request.method == "POST":
        query = request.form["query"]
        operation = request.form["proceed-submit"]
        if operation == "proceed":
            aadhar = session["aadhar"]
            connection = psycopg2.connect(
                user=user_name, password=user_password, database="project"
            )
            cur = connection.cursor()
            select_statement = "SELECT queries_query_id from QUERIES"
            cur.execute(select_statement)
            results = cur.fetchall()
            prev_id = int(results[-1][0])
            cur_id = str(prev_id + 1)
            insert_statement = (
                f"INSERT INTO QUERIES VALUES ('{cur_id}','{query}','{aadhar}')"
            )
            cur.execute(insert_statement)
            cur.close()
            connection.commit()
            connection.close()
            flash("Successfully posted query")
            return redirect(url_for("general_public_login_operation"))
    else:
        return render_template("login/general_public/insert_query.html")


@app.route("/login/general-public/select", methods=["POST", "GET"])
def general_public_login_select():
    if request.method == "POST":
        operation = request.form["name"]
        if operation == "forAdoption":
            return redirect(url_for("general_public_login_select_for_adoption"))
        elif operation == "forSponsorship":
            return redirect(url_for("general_public_login_select_for_sponsorship"))
        elif operation == "petCareProducts":
            return redirect(url_for("incharge_pet_shop_login_select_pet_care_products"))
        elif operation == "queryAnswers":
            return redirect(url_for("doctor_login_query_answers_select"))
    else:
        return render_template("login/general_public/select.html")


# to be modified
@app.route("/login/general-public/select/for-adoption", methods=["POST", "GET"])
def general_public_login_select_for_adoption():
    if request.method == "POST":
        if request.form["proceed-submit"] == "logout":
            flash("Logged out")
            return redirect(url_for("home"))
        else:
            animal_id = request.form["proceed-submit"]
            update_statement = f"UPDATE ANIMAL set animal_adopted = true WHERE animal_id ='{animal_id}'"

            connection = psycopg2.connect(
                user=user_name, password=user_password, database="project"
            )
            cur = connection.cursor()
            cur.execute(update_statement)
            cur.close()
            connection.commit()
            connection.close()
            flash("Successfully adopted")
            return redirect(url_for("general_public_login_select_for_adoption"))
    else:
        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )
        cur = connection.cursor()

        select_statement = f"SELECT A.animal_id,A.animal_image_link,A.animal_gender,A.animal_weight,A.animal_age,A.animal_price,B.animal_type_breed,B.animal_type_type FROM ANIMAL AS A,ANIMAL_TYPE AS B WHERE A.animal_adopted = false AND A.animal_from_zoos = false AND A.animal_type_id = B.animal_type_id"
        cur.execute(select_statement)

        results = cur.fetchall()

        cur.execute(f"{select_statement} LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        connection.commit()
        connection.close()
        return render_template(
            "login/general_public/select/for_adoption.html",
            colnames=colnames,
            results=results,
        )


# to be modified
@app.route("/login/general-public/select/for-sponsorship", methods=["POST", "GET"])
def general_public_login_select_for_sponsorship():
    if request.method == "POST":
        if request.form["proceed-submit"] == "logout":
            flash("Logged out")
            return redirect(url_for("home"))
        else:
            flash("Successfully sponsored")
            return redirect(url_for("general_public_login_select_for_sponsorship"))
    else:
        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )
        cur = connection.cursor()

        select_statement = f"SELECT A.animal_id,A.animal_image_link,A.animal_gender,A.animal_weight,A.animal_age,B.animal_type_breed,B.animal_type_type, C.zoos_name FROM ANIMAL AS A,ANIMAL_TYPE AS B,ZOOS AS C WHERE A.animal_adopted = false AND A.animal_from_zoos = true AND A.animal_type_id = B.animal_type_id AND A.animal_zoos_id = C.zoos_id"
        cur.execute(select_statement)

        results = cur.fetchall()

        cur.execute(f"{select_statement} LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        connection.commit()
        connection.close()

        return render_template(
            "login/general_public/select/for_sponsorship.html",
            colnames=colnames,
            results=results,
        )


@app.route("/login/doctor", methods=["POST", "GET"])
def doctor_login():
    if request.method == "POST":
        entered_certificate_no = request.form["certificateNo"]
        entered_password = request.form["password"]

        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )

        cur = connection.cursor()
        list_of_users_statement = (
            f"SELECT login_doctor_certificate_no_id FROM LOGIN_DOCTORS"
        )
        cur.execute(list_of_users_statement)

        list_of_users = cur.fetchall()
        list_of_users = [i[0] for i in list_of_users]

        if str(entered_certificate_no) not in list_of_users:
            flash("Invalid credentials")
            return redirect(url_for("doctor_login"))

        session["certificate_no"] = entered_certificate_no

        select_statement = f"SELECT login_doctor_password FROM LOGIN_DOCTORS WHERE login_doctor_certificate_no_id = '{entered_certificate_no}'"
        cur.execute(select_statement)

        actual_password = cur.fetchone()[0]

        if entered_password == actual_password:
            flash("Successfully logged in")
            return redirect(url_for("doctor_login_table"))
        else:
            flash("Invalid credentials")
            return redirect(url_for("doctor_login"))
    else:
        return render_template("login/doctor.html")


@app.route("/login/doctor/table", methods=["POST", "GET"])
def doctor_login_table():
    if request.method == "POST":
        session["doctor_login_table"] = request.form["name"]
        if session["doctor_login_table"] == "animalDiseaseHistory":
            return redirect(url_for("doctor_login_animal_disease_history_operation"))
        elif session["doctor_login_table"] == "queryAnswers":
            return redirect(url_for("doctor_login_query_answers_operation"))
        elif session["doctor_login_table"] == "animalTypeCare":
            return redirect(url_for("doctor_login_animal_type_care_operation"))
        elif session["doctor_login_table"] == "doctors":
            return redirect(url_for("doctor_login_doctor_details_operation"))
    else:
        return render_template("login/doctor/table.html")


@app.route("/login/doctor/operation", methods=["POST", "GET"])
def doctor_login_doctor_details_operation():
    if request.method == "POST":
        operation = request.form["name"]
        if operation == "select":
            return redirect(url_for("doctor_login_doctor_details_select"))
    else:
        return render_template("login/doctor/doctor_details/operation.html")


@app.route("/login/doctor/select/doctor-details", methods=["POST", "GET"])
def doctor_login_doctor_details_select():
    if request.method == "POST":
        flash("Logged out")
        return redirect(url_for("home"))
    else:
        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )
        cur = connection.cursor()

        select_statement = f"""
        SELECT
            doctor_name,
            doctor_email,
            doctor_hospital_address,
            doctor_domain
        FROM
            DOCTORS"""

        cur.execute(select_statement)

        results = cur.fetchall()

        cur.execute(f"{select_statement} LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        connection.commit()
        connection.close()
        return render_template(
            "login/doctor/doctor_details.html", colnames=colnames, results=results
        )


@app.route(
    "/login/doctor/adopted-animals-with-disease-history/select", methods=["POST", "GET"]
)
def doctor_login_people_adopted_animals_with_disease_history():
    if request.method == "POST":
        flash("Logged out")
        return redirect(url_for("home"))
    else:
        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )
        cur = connection.cursor()

        select_statement = f"""
        SELECT
            animal_adopted_animal_id,animal_adopted_animal,general_public_name,general_public_email
	
        FROM
            ANIMAL_ADOPTED,GENERAL_PUBLIC
        WHERE
            animal_adopted_general_public_aadhar = general_public_aadhar_no
            AND animal_adopted_animal_id IN (
                SELECT
                    animal_animal_disease_history_animal_id
                FROM
                    ANIMAL_ANIMAL_DISEASE_HISTORY
            )"""

        cur.execute(select_statement)

        results = cur.fetchall()

        cur.execute(f"{select_statement} LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        connection.commit()
        connection.close()
        return render_template(
            "login/doctor/animal_disease_history/select/people_adopted_animals_with_disease_history.html",
            colnames=colnames,
            results=results,
        )


@app.route("/login/doctor/animal-disease-history/operation", methods=["POST", "GET"])
def doctor_login_animal_disease_history_operation():
    if request.method == "POST":
        operation = request.form["name"]
        if operation == "select":
            return redirect(url_for("doctor_login_animal_disease_history_select_table"))
    else:
        return render_template("login/doctor/animal_disease_history/operation.html")


@app.route("/login/doctor/animal-disease-history/select/table", methods=["POST", "GET"])
def doctor_login_animal_disease_history_select_table():
    if request.method == "POST":
        operation = request.form["name"]
        if operation == "results":
            return redirect(url_for("doctor_login_animal_disease_history_select"))
        elif operation == "selectPeople":
            return redirect(
                url_for("doctor_login_people_adopted_animals_with_disease_history")
            )
    else:
        return render_template("login/doctor/animal_disease_history/select/table.html")


@app.route("/login/doctor/animal-type-care/operation", methods=["POST", "GET"])
def doctor_login_animal_type_care_operation():
    if request.method == "POST":
        operation = request.form["name"]
        if operation == "select":
            return redirect(url_for("doctor_login_animal_type_care_select"))
        elif operation == "update":
            return redirect(url_for("doctor_login_animal_type_care_update"))
        elif operation == "insert":
            return redirect(url_for("doctor_login_animal_type_care_insert"))
    else:
        return render_template("login/doctor/animal_type_care/operation.html")


@app.route("/login/doctor/query-answer/operation", methods=["POST", "GET"])
def doctor_login_query_answers_operation():
    if request.method == "POST":
        operation = request.form["name"]
        if operation == "select":
            return redirect(url_for("doctor_login_query_answers_select"))
        elif operation == "update":
            return redirect(url_for("doctor_login_query_answers_update"))
        elif operation == "insert":
            return redirect(url_for("doctor_login_query_answers_insert"))
        elif operation == "queriesNotAnswered":
            return redirect(url_for("doctor_login_queries_not_answered"))
    else:
        return render_template("login/doctor/query_answer/operation.html")


@app.route("/login/doctor/animal-disease-history/select", methods=["POST", "GET"])
def doctor_login_animal_disease_history_select():
    if request.method == "POST":
        flash("Logged out")
        return redirect(url_for("home"))
    else:
        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )
        cur = connection.cursor()

        select_statement = f"SELECT animal_animal_disease_history_animal_id, animal_animal_disease_history_animal_disease_name, animal_animal_disease_history_animal_disease_no_of_months FROM ANIMAL_ANIMAL_DISEASE_HISTORY"
        cur.execute(select_statement)

        results = cur.fetchall()

        cur.execute(f"{select_statement} LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        connection.commit()
        connection.close()
        return render_template(
            "login/doctor/animal_disease_history/select/results.html",
            colnames=colnames,
            results=results,
        )


@app.route("/login/doctor/animal-type-care/select", methods=["POST", "GET"])
def doctor_login_animal_type_care_select():
    if request.method == "POST":
        flash("Logged out")
        return redirect(url_for("home"))
    else:
        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
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
            user=user_name, password=user_password, database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO ANIMAL_TYPE_ANIMAL_TYPE_CARE VALUES ('{id}', '{type_of_care}', '{breed}')"
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()

        flash("Successfully inserted")
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
            user=user_name, password=user_password, database="project"
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

        flash("Successfully updated")
        return redirect(url_for("home"))
    else:
        return render_template("login/doctor/animal_type_care/update.html")


@app.route("/login/doctor/query-answer/select", methods=["POST", "GET"])
def doctor_login_query_answers_select():
    if request.method == "POST":
        flash("Logged out")
        return redirect(url_for("home"))
    else:
        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )
        cur = connection.cursor()

        select_statement = f"SELECT * FROM QUERIES LEFT OUTER JOIN QUERIES_QUERY_ANSWER on QUERIES.queries_query_id = QUERIES_QUERY_ANSWER.queries_query_answer_query_id"
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
        query_answered_by = session["certificate_no"]

        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO QUERIES_QUERY_ANSWER VALUES ('{id}', '{query_answer}', '{query_id}', '{query_answered_by}')"
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()

        flash("Successfully inserted")
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
        query_answered_by = session["certificate_no"]

        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
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

        flash("Successfully updated")
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

        entered_certificate_no = request.form["certificateNo"]
        entered_password = request.form["password"]

        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )

        cur = connection.cursor()

        list_of_users_statement = (
            f"SELECT login_animal_shelter_certificate_no_id FROM LOGIN_ANIMAL_SHELTER"
        )
        cur.execute(list_of_users_statement)

        list_of_users = cur.fetchall()
        list_of_users = list(map(lambda x: x[0], list_of_users))

        if str(entered_certificate_no) not in list_of_users:
            flash("Invalid credentials")
            return redirect(url_for("incharge_animal_shelter_login"))

        select_statement = f"SELECT login_animal_shelter_password FROM LOGIN_ANIMAL_SHELTER WHERE login_animal_shelter_certificate_no_id = '{entered_certificate_no}'"
        cur.execute(select_statement)

        actual_password = cur.fetchone()[0]

        if entered_password == actual_password:
            flash("Successfully logged in")
            return redirect(url_for("incharge_animal_shelter_login_operation"))
        else:
            flash("Invalid credentials")
            return redirect(url_for("incharge_animal_shelter_login"))
    else:
        return render_template("login/incharge/animal_shelter.html")


@app.route("/login/incharge/animal-shelter/operation", methods=["POST", "GET"])
def incharge_animal_shelter_login_operation():
    if request.method == "POST":
        operation = request.form["name"]
        if operation == "select":
            return redirect(url_for("incharge_animal_shelter_login_select_table"))
        elif operation == "update":
            return redirect(url_for("incharge_animal_shelter_login_update"))
        elif operation == "insert":
            return redirect(url_for("incharge_animal_shelter_login_insert"))
        elif operation == "peopleNotAdopted":
            return redirect(url_for("incharge_animal_shelter_login_people_not_adopted"))
    else:
        return render_template("login/incharge/animal_shelter/operation.html")


@app.route("/login/incharge/animal-shelter/select/table", methods=["POST", "GET"])
def incharge_animal_shelter_login_select_table():
    if request.method == "POST":
        operation = request.form["name"]
        if operation == "results":
            return redirect(url_for("incharge_animal_shelter_login_select_results"))
        elif operation == "peopleNotAdopted":
            return redirect(url_for("incharge_animal_shelter_login_people_not_adopted"))
    else:
        return render_template("login/incharge/animal_shelter/select/table.html")


@app.route("/login/incharge/animal-shelter/select/results", methods=["POST", "GET"])
def incharge_animal_shelter_login_select_results():
    if request.method == "POST":
        flash("Logged out")
        return redirect(url_for("home"))
    else:
        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
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
            "login/incharge/animal_shelter/select/results.html",
            colnames=colnames,
            results=results,
        )


@app.route("/login/incharge/animal-shelter/insert", methods=["POST", "GET"])
def incharge_animal_shelter_login_insert():
    if request.method == "POST":
        animal_id = request.form.get("animalId")
        animal_shelter_certificate_no = request.form.get("animalShelterCertificateNo")
        animal_type_id = request.form.get("animalTypeId")
        animal_disease_history_exists = request.form.get("animalDiseaseHistoryExists")
        animal_gender = request.form.get("animalGender")
        animal_weight = request.form.get("animalWeight")
        animal_age = request.form.get("animalAge")
        animal_price = request.form.get("animalPrice")
        animal_image_link = request.form.get("animalImageLink")
        print(animal_shelter_certificate_no)
        print(animal_image_link)

        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO ANIMAL VALUES ('{animal_id}', NULL, NULL, '{animal_shelter_certificate_no}', false, '{animal_type_id}', false, true, false, {animal_disease_history_exists}, '{animal_gender}', {animal_weight}, {animal_age}, {animal_price}, '{animal_image_link}')"

        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()

        flash("Successfully inserted")
        return redirect(url_for("home"))
    else:
        return render_template(
            "login/incharge/animal_shelter/insert.html",
        )


@app.route("/login/incharge/animal-shelter/update", methods=["POST", "GET"])
def incharge_animal_shelter_login_update():
    if request.method == "POST":
        animal_id = request.form.get("animalId")
        animal_shelter_certificate_no = request.form.get("animalShelterCertificateNo")
        animal_type_id = request.form.get("animalTypeId")
        animal_disease_history_exists = request.form.get("animalDiseaseHistoryExists")
        animal_gender = request.form.get("animalGender")
        animal_weight = request.form.get("animalWeight")
        animal_age = request.form.get("animalAge")
        animal_price = request.form.get("animalPrice")
        animal_image_link = request.form.get("animalImageLink")

        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )

        cur = connection.cursor()

        cur.execute(
            "SELECT animal_id, animal_animal_shelter_certificate_no, animal_type_id, animal_disease_history_exist, animal_gender, animal_weight, animal_age, animal_price, animal_image_link FROM ANIMAL LIMIT 0"
        )
        colnames = [desc[0] for desc in cur.description]
        value_string = ""

        values = (
            animal_id,
            animal_shelter_certificate_no,
            animal_type_id,
            animal_disease_history_exists,
            animal_gender,
            animal_weight,
            animal_age,
            animal_price,
            animal_image_link,
        )

        for i in range(3):
            value_string += f"{colnames[i]}='{values[i]}',"
        value_string += f"{colnames[3]}={values[3]},"
        value_string += f"{colnames[4]}='{values[4]}',"
        for i in range(5, 7):
            value_string += f"{colnames[i]}={values[i]},"
        value_string += f"{colnames[8]}='{values[8]}'"
        value_string += f" WHERE {colnames[0]} = '{animal_id}';"

        # update_statement = f"UPDATE ANIMAL_SHELTER SET (animal_id, animal_shelter_certificate_no, animal_type_id, animal_disease_history_exists, animal_gender, animal_weight, animal_age, animal_price, animal_image_link) = {value_string}"
        update_statement = f"UPDATE ANIMAL SET {value_string}"

        print(update_statement)
        cur.execute(update_statement)

        cur.close()
        connection.commit()
        connection.close()

        flash("Successfully inserted")
        return redirect(url_for("home"))
    else:
        return render_template(
            "login/incharge/animal_shelter/update.html",
        )


@app.route("/login/incharge/animal-shelter/people-not-adopted", methods=["POST", "GET"])
def incharge_animal_shelter_login_people_not_adopted():
    if request.method == "POST":
        flash("Logged out")
        return redirect(url_for("home"))
    else:
        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )
        cur = connection.cursor()

        select_statement = f"""
        SELECT
            general_public_name,
            general_public_email
        FROM
            GENERAL_PUBLIC
        WHERE
            general_public_aadhar_no NOT IN (
                SELECT
                    animal_adopted_general_public_aadhar
                FROM
                    ANIMAL_ADOPTED
                WHERE
                    animal_adopted_general_public_aadhar IS NOT NULL
        )"""
        cur.execute(select_statement)

        results = cur.fetchall()

        cur.execute(f"{select_statement} LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        connection.commit()
        connection.close()
        return render_template(
            "login/incharge/animal_shelter/select/people_not_adopted.html",
            colnames=colnames,
            results=results,
        )


@app.route("/login/incharge/pet-shop", methods=["POST", "GET"])
def incharge_pet_shop_login():
    if request.method == "POST":
        entered_certificate_no = request.form["certificateNo"]
        entered_password = request.form["password"]

        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )

        cur = connection.cursor()

        list_of_users_statement = (
            f"SELECT login_pet_shop_certificate_no_id FROM LOGIN_PET_SHOP"
        )
        cur.execute(list_of_users_statement)

        list_of_users = cur.fetchall()
        list_of_users = [i[0] for i in list_of_users]

        if str(entered_certificate_no) not in list_of_users:
            flash("Invalid credentials")
            return redirect(url_for("incharge_pet_shop_login"))

        select_statement = f"SELECT login_pet_shop_password FROM LOGIN_PET_SHOP WHERE login_pet_shop_certificate_no_id = '{entered_certificate_no}'"
        cur.execute(select_statement)

        actual_password = cur.fetchone()[0]

        if entered_password == actual_password:
            flash("Successfully logged in")
            return redirect(url_for("incharge_pet_shop_login_operation"))
        else:
            flash("Invalid credentials")
            return redirect(url_for("incharge_pet_shop_login"))
    else:
        return render_template("login/incharge/pet_shop.html")


@app.route("/login/incharge/pet-shop/operation", methods=["POST", "GET"])
def incharge_pet_shop_login_operation():
    if request.method == "POST":
        operation = request.form["name"]
        if operation == "select":
            return redirect(url_for("incharge_pet_shop_login_select_operation"))
        elif operation == "update":
            return redirect(url_for("incharge_pet_shop_login_update"))
        elif operation == "insert":
            return redirect(url_for("incharge_pet_shop_login_insert"))
    else:
        return render_template("login/incharge/pet_shop/operation.html")


@app.route("/login/incharge/pet-shop/select/table", methods=["POST", "GET"])
def incharge_pet_shop_login_select_operation():
    if request.method == "POST":
        operation = request.form["name"]
        if operation == "peopleAdoptedWithMore":
            return redirect(
                url_for("incharge_pet_shop_login_select_people_adopted_with_more")
            )
    else:
        return render_template("login/incharge/pet_shop/select/table.html")


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
            user=user_name, password=user_password, database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO PET_SHOP VALUES ('{no_of_pets}', {certificate_no}, '{phone}', '{name}', '{address}', '{city}')"
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()

        flash("Successfully inserted")
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
            user=user_name, password=user_password, database="project"
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

        flash("Successfully updated")
        return redirect(url_for("home"))
    else:
        return render_template(
            "login/incharge/pet_shop/update.html",
        )


@app.route("/login/incharge/pet-shop/select-pet-care-products", methods=["POST", "GET"])
def incharge_pet_shop_login_select_pet_care_products():
    if request.method == "POST":
        flash("Logged out")
        return redirect(url_for("home"))
    else:
        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )
        cur = connection.cursor()

        select_statement = f"""
        SELECT
            pet_care_products_link,
            pet_care_products_link_website,
            pet_care_products_animal_type_id,
            pet_care_products_product_type
        FROM
            PET_CARE_PRODUCTS
        GROUP BY
            pet_care_products_link,
            pet_care_products_link_website,
            pet_care_products_animal_type_id,
            pet_care_products_product_type"""

        cur.execute(f"{select_statement}")
        results = cur.fetchall()

        cur.execute(f"{select_statement} LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        connection.commit()
        connection.close()
        return render_template(
            "login/incharge/pet_shop/select/pet_care_products.html",
            colnames=colnames,
            results=results,
        )


@app.route(
    "/login/incharge/pet-shop/select-people-adopted-with-more", methods=["POST", "GET"]
)
def incharge_pet_shop_login_select_people_adopted_with_more():
    if request.method == "POST":
        flash("Logged out")
        return redirect(url_for("home"))
    else:
        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )
        cur = connection.cursor()

        select_statement = f"""
        SELECT
            general_public_name,
            general_public_email
        FROM
            GENERAL_PUBLIC
        WHERE
            general_public_aadhar_no IN(
                SELECT
                    animal_adopted_general_public_aadhar
                FROM
                    ANIMAL_ADOPTED
                WHERE
                    animal_adopted_pet_shop_certificate_no IS NOT NULL
                    AND animal_adopted_pet_shop_certificate_no IN(
                        SELECT
                            pet_shop_certificate_no
                        FROM
                            PET_SHOP
                        WHERE
                            pet_shop_no_of_pets > 50
                    )
            )"""
        cur.execute(select_statement)

        results = cur.fetchall()

        cur.execute(f"{select_statement} LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        connection.commit()
        connection.close()
        return render_template(
            "login/incharge/pet_shop/select/people_adopted_with_more.html",
            colnames=colnames,
            results=results,
        )


@app.route("/login/incharge/zoo", methods=["POST", "GET"])
def incharge_zoo_login():
    if request.method == "POST":
        entered_id = request.form["id"]
        entered_password = request.form["password"]

        user_name = "postgres"
        user_password = "2020"

        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )

        cur = connection.cursor()

        list_of_users_statement = f"SELECT login_zoo_zoos_id FROM LOGIN_ZOO"
        cur.execute(list_of_users_statement)

        list_of_users = cur.fetchall()
        list_of_users = [i[0] for i in list_of_users]

        if str(entered_id) not in list_of_users:
            flash("Invalid credentials")
            return redirect(url_for("incharge_zoo_login"))

        select_statement = f"SELECT login_zoo_password FROM LOGIN_ZOO WHERE login_zoo_zoos_id = '{entered_id}'"
        cur.execute(select_statement)

        actual_password = cur.fetchone()[0]

        if entered_password == actual_password:
            flash("Successfully logged in")
            return redirect(url_for("incharge_zoo_login_operation"))
        else:
            flash("Invalid credentials")
            return redirect(url_for("incharge_zoo_login"))

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
        flash("Logged out")
        return redirect(url_for("home"))
    else:
        connection = psycopg2.connect(
            user=user_name, password=user_password, database="project"
        )
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
            user=user_name, password=user_password, database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO ZOOS VALUES ('{id}', '{name}', '{address}', '{phone}', {no_of_animals}, '{visiting_hours}')"
        cur.execute(insert_statement)

        cur.close()
        connection.commit()
        connection.close()

        flash("Successfully inserted")
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
            user=user_name, password=user_password, database="project"
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

        flash("Successfully updated")
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
            user=user_name, password=user_password, database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO GENERAL_PUBLIC VALUES ('{name}', '{phone}', '{email}', '{address}', {age}, '{aadhar_no}')"
        cur.execute(insert_statement)

        store_statement = (
            f"INSERT INTO LOGIN_PUBLIC VALUES ('{aadhar_no}', '{name}', '{password}')"
        )
        cur.execute(store_statement)

        cur.close()
        connection.commit()
        connection.close()

        receiver_email = email

        # send mail to newly signed up user
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, sender_decrypted_password)
            server.sendmail(sender_email, receiver_email, message)

        flash("Successfully signed up! Check out the welcome mail")
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
            user=user_name, password=user_password, database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO DOCTORS VALUES ('{domain}', '{name}', '{phone}', '{email}', '{hospital_address}', '{certificate_no}')"
        cur.execute(insert_statement)

        store_statement = f"INSERT INTO LOGIN_DOCTORS VALUES ('{certificate_no}', '{name}', '{password}')"
        cur.execute(store_statement)

        cur.close()
        connection.commit()
        connection.close()
        flash("Successfully signed up")
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
            user=user_name, password=user_password, database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO ANIMAL_SHELTER VALUES ('{certificate_no}', {no_of_pets}, '{address}', '{phone}', '{name}', '{city}')"
        cur.execute(insert_statement)

        store_statement = f"INSERT INTO LOGIN_ANIMAL_SHELTER VALUES ('{certificate_no}', '{name}', '{password}')"
        cur.execute(store_statement)

        cur.close()
        connection.commit()
        connection.close()

        flash("Successfully signed up")
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
            user=user_name, password=user_password, database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO PET_SHOP VALUES ({no_of_pets}, '{certificate_no}', '{phone}', '{name}', '{address}', '{city}')"
        cur.execute(insert_statement)

        store_statement = f"INSERT INTO LOGIN_PET_SHOP VALUES ('{certificate_no}', '{name}', '{password}')"
        cur.execute(store_statement)

        cur.close()
        connection.commit()
        connection.close()

        flash("Successfully signed up")
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
            user=user_name, password=user_password, database="project"
        )

        cur = connection.cursor()

        insert_statement = f"INSERT INTO ZOOS VALUES ('{id}', '{name}', '{address}', '{phone}', {no_of_animals}, '{visiting_hours}')"
        cur.execute(insert_statement)

        store_statement = (
            f"INSERT INTO LOGIN_ZOO VALUES ('{id}', '{name}', '{password}')"
        )
        cur.execute(store_statement)

        cur.close()
        connection.commit()
        connection.close()

        flash("Successfully signed up")
        return redirect(url_for("home"))
    else:
        return render_template("signup/zoo.html")


app.run(debug=True)
