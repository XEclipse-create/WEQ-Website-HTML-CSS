from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import mongo


app = Flask(__name__, static_url_path="/static")
app.debug = True
app.secret_key = 'Nothing'


@app.route("/")
def home():
    check = False
    if "name" in session:
        check = True
    return render_template("home.html")


@app.route("/login")
def LoginPage():
    if "name" in session:
        return redirect("/home2")
    return render_template("customer.html")


@app.route("/home2")
def home2():
    return render_template("home2.html")


@app.route("/customer")
def custom():
    return render_template("choice.html")


@app.route("/signup")
def signin():
    if "name" in session:
        return redirect("/home2")
    return render_template("business.html")


@app.route("/booking")
def book():
    return render_template("booking.html")


@app.route("/logout")
def LogOut():
    session.clear()
    return redirect("/")


@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404


@app.route('/login_action', methods=['POST'])
def login_action():

    email = request.form['email']
    password = request.form['pass']
    print(email, password)
    data = {}
    result = mongo.CustLogin(email, password)
    if result['check']:
        session['email'] = email
        session['name'] = result['name']

        data['check'] = True
        data['link'] = "/dashboard"

    return data


@app.route('/login2_action', methods=['POST'])
def login2_action():

    usrname = request.form['usrname']
    password = request.form['password']

    print(usrname, password)
    data = {}
    result = mongo.ShopLogin(usrname, password)
    if result['check']:
        session['usrname'] = usrname
        session['name'] = result['name']

        data['check'] = True
        data['link'] = "/home2"

    return data


@app.route('/sign_action', methods=['POST'])
def sign_action():

    name = request.form['name']
    email = request.form['email']
    ph_no = request.form['contact']
    city = request.form['city']
    pincode = request.form['pincode']

    print(name, email, ph_no, city, pincode)
    data = {}
    if mongo.CustRegister(name, email, ph_no, city, pincode):
        session['email'] = email
        session['name'] = name
        session['contact'] = ph_no
        session['city'] = city
        session['pincode'] = pincode
        data['check'] = True
        data['link'] = '/home2'

    return data


@app.route('/sign2_action', methods=['POST'])
def sign2_action():

    name = request.form['name']
    email = request.form['email']
    ph_no = request.form['contact']
    city = request.form['city']
    pincode = request.form['pincode']

    print(name, email, ph_no, city, pincode)
    data = {}
    if mongo.ShopRegister(name, email, ph_no, city, pincode):
        session['email'] = email
        session['name'] = name
        session['contact'] = ph_no
        session['city'] = city
        session['pincode'] = pincode
        data['check'] = True
        data['link'] = '/home2'

    return data


if __name__ == "__main__":
    app.run(debug=True)
