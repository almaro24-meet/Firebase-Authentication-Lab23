from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping

    
config = {
  "apiKey": "AIzaSyA2RGS3KhIS_in0K4hHAuM_PseyuIgW_T8",
  "authDomain": "fir-meet-acfb8.firebaseapp.com",
  "projectId": "fir-meet-acfb8",
  "storageBucket": "fir-meet-acfb8.appspot.com",
  "messagingSenderId": "978020303411",
  "appId": "1:978020303411:web:3d123576cad6946c535946",
  "measurementId": "G-VEB34ENKSN"
}

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
if __name__ == '__main__':
    app.run(debug=True)