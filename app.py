from flask import Flask, render_template, flash , redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

from data import Articles
from classes.RegisterForm import RegisterForm
from classes.ArticleForm import ArticleForm

#---------- Config  -------------#
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

#---------- Config SQL   -------------#
app.config['MYSQL_HOST'] ="localhost"
app.config['MYSQL_USER'] ="root"
app.config['MYSQL_PASSWORD'] =""
app.config['MYSQL_DB'] ="blog_python"
app.config['MYSQL_CURSORCLASS'] ="DictCursor"
# Init MYSQL 
mysql = MySQL(app)

# ALERT DO CONTROLLERS #
#---------- ROUTES  -------------#
@app.route('/')
def index() :
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/articles")
def articles():
    articles = Articles()
    return render_template('articles/index.html', articles=articles)

@app.route("/articles/<string:id>")
def article(id):
    return render_template('articles/show.html', id=id)

@app.route("/articles/create.html", methods=['GET', "POST"])
@is_logged_in
def createArticle():
    form = ArticleForm(request.form)

    if request.method == 'POST' and form.validate: 
        title = form.title.data
        body = form.body.data

        #Create Cursor 
        cur = mysql.connection.cursor()
        #Execute 
        cur.execute("INSERT INTO articles(title,body,author) VALUES(%s, %s, %s)", (title, body, session['username']))
        #Commit to DB 
        mysql.connection.commit()
        #Close cursor
        cur.close()

        flash('Article crée', 'success')
        return redirect(url_for('dashboard'))

    return render_template('articles/create.html', form=form)
#------------------------------------------------------------------------------------------------------#
# Do a Controller Security 
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate() :
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(form.password.data)
        
        #Create cursor
        cur= mysql.connection.cursor()
        #Execute query
        cur.execute("INSERT INTO users(name,email,username,password) VALUES (%s, %s, %s,%s)", (name, email, username, password) )
        #Commit to DB
        mysql.connection.commit()
        #Close Connection 
        cur.close()

        flash('Vous êtes maintenant enregister et vous pouvez vous connecter', 'success')
        return redirect(url_for('index'))
        

    return render_template('register/signin.html', form=form)

#User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        #Create cursor 
        cur = mysql.connection.cursor()

        #Get User by Username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username] )

        if result > 0:
            #Get stored hash
            data = cur.fetchone()
            password = data['password']

            #compare password
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                flash('Vous êtes connecté', 'success')
                return redirect(url_for('dashboard'))
            else: 
                error = 'Mauvais Identifiant / mot de passe ', 'danger'
                app.logger.info('PASSWORD NOT MATCHED')
                return render_template('register/login.html', error=error)

            #Close Connection 
            cur.close()
        else:
            app.logger.info('NO USER')
            error = 'Mauvais Identifiant / mot de passe ', 'danger'
            return render_template('register/login.html', error=error)

        #Close Connection 
        cur.close()

    return render_template('register/login.html')

#Check if user logged_in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Veuillez-vous connecter', 'danger')
            return redirect(url_for('login'))
    return wrap


#User logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Vous êtes déconnecté', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('users/dashboard.html')





if __name__ == '__main__':
    app.run(debug=True)