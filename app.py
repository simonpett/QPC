from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from userform import UserForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from userlogin import User
from flask import flash

app = Flask(__name__)
app.secret_key = 'aodhfbdfhvbw8357y8735bjehlf'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


if __name__ == '__main__':
    app.run()
    
@app.route('/')                                                                
def index():                                                                    
    return render_template('index.html')  
                                                              


@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        user = User(user_data['id'], user_data['first_name'], user_data['last_name'], user_data['email'], user_data['password'])
        return user
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('browse'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data['id'], user_data['first_name'], user_data['last_name'], user_data['email'], user_data['password'])
            login_user(user)
            return redirect(url_for('browse'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/browse')     
@login_required                                                           
def browse():  
    conn = get_db_connection()                                                  
    properties = conn.execute('SELECT * FROM properties').fetchall()                
    conn.close()                       
    return render_template('browse.html', properties=properties)    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = None
    if request.method == 'POST':
        form = UserForm(request.form)
    else:
        form = UserForm()
    if request.method == 'POST' and form.validate():
         # Handle the form submission
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        occupation = request.form['occupation']
        email = request.form['email']
        password = request.form['password']
        passwordhash = generate_password_hash(password)
        businessname = request.form['businessname']
        # Perform signup logic here
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (first_name, last_name, occupation, email, password, businessname) VALUES (?, ?, ?, ?, ?, ?)',
                       (first_name, last_name, occupation, email, passwordhash, businessname))
        conn.commit()
        conn.close()
        return redirect(url_for('login')) # Redirect to login page after successful signup
    
    else:
        # Render the signup page
        return render_template('signup.html', form=form)


def get_db_connection():
    conn = sqlite3.connect('QPC.db')
    conn.row_factory = sqlite3.Row
    return conn

