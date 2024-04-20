from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import csv
from userform import UserForm
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from userlogin import User
from flask import flash
from geopy.distance import geodesic
from markupsafe import Markup

app = Flask(__name__)                           # create a Flask app
app.secret_key = 'aodhfbdfhvbw8357y8735bjehlf'  # set the secret key for the app to sign the session cookie
login_manager = LoginManager()                  # create a LoginManager object to manage session authentication
login_manager.init_app(app)                     # initialise the LoginManager object with the app
login_manager.login_view = 'login'              # link the login route the login manager users when finds unauthenticated user

if __name__ == '__main__':                      # run the app
    app.run()
    
@app.route('/')                                 # route to the home page                                                              
def index():                                                                    
    return render_template('index.html')  
                                                              
@login_manager.user_loader                      # LoginManager load the user implementation
def load_user(user_id):                         # Load the user by user_id
    return get_user_by_id(user_id)              # get the user from the db

@app.route('/login', methods=['GET', 'POST'])   # route to the login page
def login():
    if current_user.is_authenticated:           # check if the user is already logged in
        return redirect(url_for('browse'))      # redirect to the browse page if logged in
    if request.method == 'POST':                # if not loggin in, check if data posted
        user = get_user_by_email(request.form['email'])             # get the user by email
        if user and user.check_password(request.form['password']):  # check user and pwd
            login_user(user)                    # login the user
            return redirect(url_for('search'))  # redirect to the search page
        else:
            flash('Invalid email or password', 'error') # password not match, send error
            return redirect(url_for('login'))   # redirect back the login page
    return render_template('login.html')        # render the login page if get

@app.route('/logout')                           # route to logout the user
@login_required                                 # login required to access this route, else auto error
def logout():
    logout_user()                               # logout the user with LoginManager 
    return redirect(url_for('login'))           # redirect to the login page

@app.route('/signup', methods=['GET', 'POST'])  # route to the signup page
def signup():
    form = None                                 
    if request.method == 'POST':                # if data posted populate the UserForm
        form = UserForm(request.form)
    else:
        form = UserForm()                       # create a new UserForm object
    # algorithm to validate the user data and check if the users already exists using UserForm validators
    if request.method == 'POST' and form.validate():
        user = get_user_by_email(form.email.data) # check if user already exists
        if user != None:                          # if user exists, send error message
            flash(Markup('User already exists, please use a different email, or try forgotten password <a href="'+url_for('forgotpassword')+'" class="alert-link">here</a>'), 'error')
            return render_template('signUp.html', form=form)
        password = request.form['password'] # get password to hash
        conn = get_db_connection()              # connect to the database
        cursor = conn.cursor()                  # create a cursor object and insert the validated data into hte database as a new user
        cursor.execute('INSERT INTO users (first_name, last_name, occupation, email, password, businessname) VALUES (?, ?, ?, ?, ?, ?)',
                       (request.form['first_name'], request.form['last_name'], request.form['occupation'], request.form['email'], generate_password_hash(password), request.form['businessname']))
        conn.commit()                           # commit the changes and close the database connection
        conn.close()                            # close the database connection and send a welcome message
        flash('Thanks for signing up! Please login to continue', 'info') 
        return redirect(url_for('login'))       # after signing up send them to the page to login
    else:
        return render_template('signup.html', form=form)    # if get request, render the signup page

@app.route('/admin')                            # route to the admin page
@login_required                                 # login required to access this route, else auto error
def admin():
    if current_user.is_admin == False:          # check if the user is an admin, else send error
        flash('You do not have permission to access this page', 'error') 
        return redirect(url_for('browse'))      # if not admin send to browse with error
    return render_template('admin.html')        # if admin, render the admin page

@app.route('/upload_schools', methods=['POST']) # route to upload the schools data csv file
@login_required                                 # login required to access this route, else auto error
def upload_schools():
    if current_user.is_admin == False:          # check if the user is an admin, else send error
        flash('You do not have permission to access this page', 'error')
        return redirect(url_for('browse'))      # if not admin send to browse with error
    if request.method == 'POST':                # if data posted, check the csv file
        if 'schools_csv_file' not in request.files: 
            flash('No file provided', 'error')  # if no file create an error
            return render_template('admin.html') # send user back to admin to try again
        schools_csv_file = request.files['schools_csv_file'] 
        if schools_csv_file.filename == '':     # if file provided, check the filename
            flash('No filename provided', 'error') # if no filename create an error
            return render_template('admin.html')   # send user back to admin to try again
        filename = request.files['schools_csv_file'] # if filename provided, open the file and read the data
        schools_data = csv.DictReader(filename.stream.read().decode('utf-8-sig').splitlines())
        header = schools_data.fieldnames        # check if the file is has the required header fields
        if header[0] != "_id" or header[2] != 'Centre Name' or header[18] != 'Actual Address Line 3' or header[38] != 'Latitude' or header[37] != 'Longitude': 
            flash("The file headers do not contain the required school fields", 'error') 
            return render_template('admin.html')
        conn = get_db_connection()              # file exists and in correct format to update the database
        cursor = conn.cursor()                  # connect to the database and create a cursor object
        cursor.execute('DELETE FROM schools')   # delete the old schools data and insert the new data
        schools = 0                             # count the number of schools uploaded
        for row in schools_data:                # iterate over the rows and insert schools into the database
            cursor.execute('INSERT INTO schools (id, name, suburb, latitude, longitude) VALUES (?, ?, ?, ?, ?)',
                            (row['_id'], row['Centre Name'], row['Actual Address Line 3'], row['Latitude'], row['Longitude']))
            schools += 1                        # increment the schools count in the loop
        conn.commit()                           # commit the changes which deletes the old and inserts the new data
        conn.close()                            # close the database connection and send a success message
        flash(str(schools)+' Schools uploaded successfully', 'info')
    return redirect(url_for('admin'))
    
    
@app.route('/upload_bus_stops', methods=['POST'])   # route to upload the bus stops data csv file
@login_required                                     # login required to access this route, else auto error
def upload_bus_stops():                     
    if current_user.is_admin == False:              # check if the user is an admin, else send error
        flash('You do not have permission to access this page', 'error')
        return redirect(url_for('browse'))          # if not admin send to browse with error
    if request.method == 'POST':                    # if data posted, check the csv file
        if 'bus_stops_csv_file' not in request.files: # check the file is provided
            flash('No file provided', 'error')      # if no file create an error and
            return render_template('admin.html')    # send user back to admin to try again
        bus_stops_csv_file = request.files['bus_stops_csv_file'] 
        if bus_stops_csv_file.filename == '':       # if file provided, check the filename
            flash('No filename provided', 'error')  # if no filename create an error, and
            return render_template('admin.html')    # send user back to admin to try again
        filename = request.files['bus_stops_csv_file']  # if filename provided, open the file and read the data
        bus_stops_data = csv.DictReader(filename.stream.read().decode('utf-8-sig').splitlines())
        header = bus_stops_data.fieldnames          # check if the file is has the required header fields
        if header[0] != "_id" or header[2] != 'HASTUS' or header[3] != 'DESCRIPTION' or header[10] != 'SUBURB' or header[8] != 'LATITUDE' or header[9] != 'LONGITUDE': 
            flash("The file headers do not contain the required bus stop fields", 'error') 
            return render_template('admin.html')
        conn = get_db_connection()                  # file exists and in correct format to update the database
        cursor = conn.cursor()                      # connect to the database and create a cursor object
        cursor.execute('DELETE FROM bus_stops')     # delete the old bus stops data and insert the new data
        bus_stops = 0                               # count the number of bus stops uploaded
        for row in bus_stops_data:                  # iterate over the rows and insert bus stops into the database
            cursor.execute('INSERT INTO bus_stops (id, bus_stop_number, name, suburb, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)',
                            (row['_id'], row['HASTUS'], row['DESCRIPTION'], row['SUBURB'], row['LATITUDE'], row['LONGITUDE']))
            bus_stops += 1                          # increment the bus stops count in the loop
        conn.commit()                               # commit the changes which deletes the old and inserts the new data
        conn.close()                                # close the database connection and send a success message
        flash(str(bus_stops)+' Bus Stops uploaded successfully', 'info')
    return redirect(url_for('admin'))

@app.route('/browse')                     # route to the browse real estate propoerties page    
@login_required                           # login required to access this route, else auto error
def browse():  
    conn = get_db_connection()            # connect to the database and get all the properties
    properties = conn.execute('SELECT * FROM properties ORDER BY suburb').fetchall()                
    conn.close()                          # close the db and send properties to the page
    return render_template('browse.html', properties=properties)    

@app.route('/search', methods=['GET', 'POST'])  # route to the search page
@login_required                                 # login required to access this route, else auto error
def search():
    suburbs = get_unique_suburbs()              # get the unique suburbs from the database
    if request.method == 'POST':                # if data posted,
        suburb = request.form['suburb']         # get the seleted suburb from the form
        properties = get_properties_in_suburb(suburb) # get the properties from db in the selected suburb
        property_to_schools = {}                # create empty dictionaries to store the schools and bus stops
        property_to_bus_stops = {}
        target_distance_school = int(request.form['school_distance']) # get the target distances from form
        target_distance_bus_stops = float(request.form['bus_stop_distance'])
        for property in properties:             # iterate over the properties and get the schools and bus stops within the target distance
            property_lat = property['lat']      # get the latitude and longitude of the property
            property_long = property['long']    # next get the schools and bus stops within the target distance and assign to the dict
            schools_within_distance = get_schools_within_distance(target_distance_school, property_lat, property_long)
            property_to_schools[property['id']] = schools_within_distance
            bus_stops_within_distance = get_bus_stops_within_distance(target_distance_bus_stops, property_lat, property_long)
            property_to_bus_stops[property['id']] = bus_stops_within_distance
        # send the found properties, the associated schools and bus stops, and the search criteria, selected suburb, distances to form
        return render_template('search.html', properties=properties, suburbs=suburbs, property_to_schools=property_to_schools, property_to_bus_stops=property_to_bus_stops, 
                               selected_suburb=suburb, selected_distance_school=target_distance_school, selected_distance_bus=target_distance_bus_stops)
    return render_template('search.html', suburbs=suburbs)  # if get request, render the search page with unique suburbs

@app.route('/profile', methods=['GET', 'POST']) # route to the user profile page so users can update their details
@login_required                                 # login required to access this route, else auto error
def profile():
    userform = None
    if request.method == 'GET':                 # if get request, get the user details and populate the UserForm
        user = get_user_by_id(current_user.id)  # get the user by id
        userform = UserForm(obj=user)           # populate the UserForm with the user details
        if user.businessname:                   # check if the user is in real estate and set the is_in_realestate field
            userform.is_in_realestate.data = True
    else:                                       # if post request, validate the form and update the user details
        userform = UserForm(request.form)       # get the user details from the form
        if userform.validate():                 # algorithm to validate the user data, and create errors if invalid
            userfromDB = get_user_by_id(current_user.id) # get the user from the database
            if userfromDB.check_password(request.form['password']): # check if the password is correct
                conn = get_db_connection()      # everything is valid, connect to the database and update the user details
                cursor = conn.cursor()          # create a cursor object and update the user details in the database
                cursor.execute('UPDATE users SET first_name = ?, last_name = ?, occupation = ?, email = ?, businessname = ? WHERE id = ?',
                        (request.form['first_name'], request.form['last_name'], request.form['occupation'], request.form['email'], request.form['businessname'], current_user.id))
                conn.commit()                   # commit the changes and close the database connection
                conn.close()                    # close the database connection and send a success message
                flash('Changes have been saved', 'info') # send a success message
            else:
                flash('Invalid password', 'error') # if password is incorrect, send an error message
        else:        
            flash('Invalid input', 'error')     # if the form is invalid, send an error message, (userForm will auto include the field errors)
    return render_template('profile.html', form=userform) # if get render the profile page with the UserForm

@app.route('/datapolicy') # route to the data policy page
def datapolicy():
    return render_template('datapolicy.html')

@app.route('/forgotpassword', methods=['GET', 'POST']) # mock up of forgot password page, doesnt send email 
def forgotpassword():               
    if request.method == 'POST':                # if data posted, get the user by email and send a password reset email
        flash('An email has been sent to you with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('forgotpassword.html')

################### Helper functions for the routes ####################

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

def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    if user == None:
        return None
    return User(user['id'], user['first_name'], user['last_name'], user['occupation'], user['email'], user['password'], user['businessname'], user['is_admin'])

def get_user_by_id(id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    conn.close()
    if user == None:
        return None
    return User(user['id'], user['first_name'], user['last_name'], user['occupation'], user['email'], user['password'], user['businessname'], user['is_admin'])

def get_db_connection():
    conn = sqlite3.connect('QPC.db')
    conn.row_factory = sqlite3.Row
    return conn


