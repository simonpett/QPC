from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from userform import UserForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from userlogin import User
from flask import flash
from geopy.distance import geodesic

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
            return redirect(url_for('search'))
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

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    suburbs = get_unique_suburbs()
    if request.method == 'POST':
        suburb = request.form['suburb']
        properties = get_properties_in_suburb(suburb)
        property_to_schools = {}
        property_to_bus_stops = {}
        target_distance_school = int(request.form['school_distance'])
        target_distance_bus_stops = float(request.form['bus_stop_distance'])
        
        for property in properties:
            property_lat = property['lat']
            property_long = property['long']
            schools_within_distance = get_schools_within_distance(target_distance_school, property_lat, property_long)
            property_to_schools[property['id']] = schools_within_distance
            bus_stops_within_distance = get_bus_stops_within_distance(target_distance_bus_stops, property_lat, property_long)
            property_to_bus_stops[property['id']] = bus_stops_within_distance

        return render_template('search.html', properties=properties, suburbs=suburbs, property_to_schools=property_to_schools, property_to_bus_stops=property_to_bus_stops, selected_suburb=suburb, selected_distance_school=target_distance_school, selected_distance_bus=target_distance_bus_stops)
    return render_template('search.html', suburbs=suburbs)

def get_schools_within_distance(target_distance_school, property_lat, property_long):
    all_schools = get_all_schools()
    schools_within_distance = []
    for school in all_schools:
        school_lat = school['latitude']
        school_long = school['longitude']
        distance = geodesic((property_lat, property_long), (school_lat, school_long)).kilometers
        if distance < target_distance_school:
            schools_within_distance.append(school)
    return schools_within_distance

def get_bus_stops_within_distance(target_distance_bus_stops, property_lat, property_long):
    all_bus_stops = get_all_bus_stops()
    bus_stops_within_distance = []
    for bus_stop in all_bus_stops:
        bus_stop_lat = bus_stop['latitude']
        bus_stop_long = bus_stop['longitude']
        distance = geodesic((property_lat, property_long), (bus_stop_lat, bus_stop_long)).kilometers
        if distance < target_distance_bus_stops:
            bus_stops_within_distance.append(bus_stop)
    return bus_stops_within_distance

def get_all_schools():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM schools')
    all_schools = cursor.fetchall()
    conn.close()
    return all_schools

def get_unique_suburbs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT suburb FROM properties')
    suburbs = cursor.fetchall()
    conn.close()
    return suburbs

def get_properties_in_suburb(suburb):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM properties WHERE suburb = ?', (suburb,))
    properties = cursor.fetchall()
    conn.close()
    return properties

def get_all_bus_stops():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bus_stops')
    all_bus_stops = cursor.fetchall()
    conn.close()
    return all_bus_stops

def get_db_connection():
    conn = sqlite3.connect('QPC.db')
    conn.row_factory = sqlite3.Row
    return conn

