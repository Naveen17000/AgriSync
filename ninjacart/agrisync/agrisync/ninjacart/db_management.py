from flask import Flask, render_template, request, flash, session,redirect,url_for
import sqlite3
import os


app = Flask(__name__)
app.secret_key = 'ninjacart'


def create_connection():
        conn = sqlite3.connect('farmer_data.db')
        return conn

@app.route("/")
def main():
    return render_template("main.html")
@app.route("/index")
def home():
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def farmersignup():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        farm_size = request.form['farm_size']
        storage_type = request.form['storage_type']
        aadhar_pic = request.files['aadhar_pic'].read()
        farm_pic = request.files['farm_pic'].read()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO farmers (name, phone, address, farm_size, storage_type, aadhar_pic, farm_pic) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, phone, address, farm_size, storage_type, sqlite3.Binary(aadhar_pic), sqlite3.Binary(farm_pic)))
        conn.commit()
        return redirect(url_for('farmer_com'))

    return render_template('farmer-signup.html')


@app.route('/ssignup', methods=['GET', 'POST'])
def sellersignup():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO seller (name, phone, address) VALUES (?, ?, ?)",
            (name, phone, address))
        conn.commit()
        return render_template('sell-home.html')

    return render_template('seller-signup.html')

@app.route('/lsignup', methods=['GET', 'POST'])
def logsignup():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO logistic (name, phone, address) VALUES (?, ?, ?)",
            (name, phone, address))
        conn.commit()
        return render_template('log-home.html')

    return render_template('log-sign.html')

@app.route('/flogin', methods=['GET', 'POST'])
def farmer_login():
    if request.method == "POST":
        phone = request.form['mobile']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM farmers WHERE phone = ?", (phone,))
        existing_farmer = cursor.fetchone()
        conn.close()
        if existing_farmer:
            return redirect(url_for("farmer_com"))
        else:
            flash("Invalid phone number. Please try again.")
    return render_template('farmer-login.html')


@app.route('/slogin', methods=['GET', 'POST'])
def seller_login():
    if request.method == "POST":
        phone = request.form['mobile']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM seller WHERE phone = ?", (phone,))
        existing_farmer = cursor.fetchone()
        conn.close()
        if existing_farmer:
            return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged in :)")
            return redirect(url_for("user"))

    return render_template('sell-logon.html')

@ app.route('/llogin', methods=['GET', 'POST'])

def log_login():
    if request.method == "POST":
        phone = request.form['mobile']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logistic WHERE phone = ?", (phone,))
        existing_farmer = cursor.fetchone()
        conn.close()
        if existing_farmer:
            return redirect(url_for("log-home"))
    else:
            if "user" in session:
                flash("Already Logged in :)")
                return redirect(url_for("log-home.html"))

    return render_template('log-login.html')

@app.route('/fecom')
def farmer_com():
    return render_template('farmer-ecom.html')

@app.route('/fhome')
def farmer_home():
    return render_template('farmer-home.html')

@app.route('/shome')
def seller_home():
    return render_template('sell-home.html')

@app.route('/lhome')
def log_home():
    return render_template('log-home.html')

if __name__ == '__main__':
    create_connection()
    app.run(debug=True)
