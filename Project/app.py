import sqlite3
from flask import Flask, render_template, request, g

app = Flask(__name__)
app.secret_key = "key"

array = ["PESEL", "FirstName", "LastName", "Street", "City", "ZipCode"]

@app.route("/")
def index():
    data = get_db().cursor().execute("SELECT * FROM DataBase")
    return render_template("index.html", array=array)


@app.route("/add_patient", methods=["post"])
def add_patient():
    pesel = request.form.get('pesel')
    first_name = request.form.get('name')
    last_name = request.form.get('last_name')
    street = request.form.get('street')
    city = request.form.get('city')
    zip_code = request.form.get('zipcode')

    try:
        connection = get_db()
        connection.execute(
            "INSERT INTO DataBase (PESEL, FirstName, LastName, Street, City, ZipCode) VALUES (?, ?, ?, ?, ?, ?)",
            (pesel, first_name, last_name, street, city, zip_code))
        connection.commit()
    except:
        data = get_db().cursor().execute("SELECT * FROM DataBase")
        return render_template("index.html", array=array)

    data = get_db().cursor().execute("SELECT * FROM DataBase")
    return render_template("index.html", array=array)


@app.route("/del_patient", methods=["post"])
def del_patient():
    pesel = request.form.get('pesel1')
    connection = get_db()
    connection.execute("DELETE FROM DataBase WHERE PESEL=?", (pesel,))
    connection.commit()
    data = get_db().cursor().execute("SELECT * FROM DataBase")
    return render_template("index.html", array=array)


@app.route("/edit_patient", methods=["post", "get"])
def edit_patient():
    pesel = request.form.get("pesel2")
    change_field = request.form.get("edit_patient")
    value = request.form.get("new_val")

    if pesel is None or change_field is None or value is None:
        return render_template("index.html", array=array)

    connection = get_db()
    try:
        connection.execute(f"UPDATE DataBase SET {change_field}=? WHERE PESEL=?", (value, pesel))
        connection.commit()
    except Exception as e:
        return render_template("index.html", array=array)

    data = get_db().cursor().execute("SELECT * FROM DataBase")
    return render_template("index.html", array=array)


@app.route("/print", methods=["post"])
def printed():
    data = get_db().cursor().execute("SELECT * FROM DataBase").fetchall()
    type = request.form.get("sort_type")
    var = int(request.form.get("sort_by"))
    if(type=="Decreasing"):
        data = sorted(data, key=lambda x: x[var-1], reverse=True)
    elif(type=="Increasing"):
        data = sorted(data, key=lambda x: x[var-1])
    return render_template("index.html", data=data, array=array)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('DataBase.db')
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run()
