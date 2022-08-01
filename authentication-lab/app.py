from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'



config = { "apiKey": "AIzaSyCKJ8ZNmuprEXtfWpSk7guFhAZjinouWkQ",
  "authDomain": "cs-firebase-lab.firebaseapp.com",
  "projectId": "cs-firebase-lab",
  "storageBucket": "cs-firebase-lab.appspot.com",
  "messagingSenderId": "214220498671",
  "appId": "1:214220498671:web:b2050acb0a9e3771ab1d1a",
  "measurementId": "G-X7DC7NL03J", "databaseURL": "https://cs-firebase-lab-default-rtdb.europe-west1.firebasedatabase.app/" 
  }


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = { "full_name": request.form["full_name"], "username": request.form["username"], "bio": request.form["bio"] }
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            db.child("Users").child(login_session['user']["localId"]).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        tweet = {"title": request.form["title"], "content": request.form["content"], "uid": login_session["user"]["localId"]}
        db.child("Tweet").push(tweet)
    return render_template("add_tweet.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None

    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/all_tweets')
def all_tweets():
    print(db.child('Tweet').get().val())
    return render_template("tweets.html",tweets =  db.child('Tweet').get().val())

if __name__ == '__main__':
    app.run(debug=True)