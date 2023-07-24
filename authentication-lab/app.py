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
  "measurementId": "G-VEB34ENKSN",
  "databaseURL": "https://fir-meet-acfb8-default-rtdb.europe-west1.firebasedatabase.app"
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
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"full_name" : full_name, "username" : username, "bio" : bio}
            UID = login_session['user']['localId']
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error = ""
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        try:
            UID = login_session['user']['localId']
            tweet = {"title" : title, "text" : text, "UID" : UID}
            db.child("Tweets").push(tweet)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("add_tweet.html")

@app.route('/all_tweets')
def alltweets():
    g = db.child("Tweets").get().val()
    return render_template("tweet.html", tw = g)

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
if __name__ == '__main__':
    app.run(debug=True)