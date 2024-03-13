from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from userform import UserForm

app = Flask(__name__)



if __name__ == '__main__':
    app.run()
    
@app.route('/')                                                                
def index():                                                                    
    return render_template('index.html')  
                                                              

@app.route('/browse')                                                                
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
        businessname = request.form['businessname']
        # Perform signup logic here
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (first_name, last_name, occupation, email, password, businessname) VALUES (?, ?, ?, ?, ?, ?)',
                       (first_name, last_name, occupation, email, password, businessname))
        conn.commit()
        conn.close()
        return redirect(url_for('browse')) # Redirect to login page after successful signup
    
    else:
        # Render the signup page
        return render_template('signup.html', form=form)


def get_db_connection():
    conn = sqlite3.connect('QPC.db')
    conn.row_factory = sqlite3.Row
    return conn
