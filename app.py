from flask import Flask, render_template, request, redirect
import sqlite3

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
    if request.method == 'POST':
         # Handle the form submission
        username = request.form['username']
        password = request.form['password']
        # Perform signup logic here
        # ...
        return redirect('/login')  # Redirect to login page after successful signup
    else:
        # Render the signup page
        return render_template('signup.html')


def get_db_connection():
    conn = sqlite3.connect('QPC.db')
    conn.row_factory = sqlite3.Row
    return conn
