from flask import Flask, render_template, request
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




def get_db_connection():
    conn = sqlite3.connect('QPC.db')
    conn.row_factory = sqlite3.Row
    return conn
