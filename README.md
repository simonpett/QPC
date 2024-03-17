# QPC
Queensland Property Comparison

The Web application is based on python and the Flask framework
https://flask.palletsprojects.com/en/3.0.x/

The web pages are rendered using hte Jinja teamplate that integrates with Flask
https://jinja.palletsprojects.com/en/3.1.x/templates/

The database used is SQLite which comes with python
https://www.sqlite.org/index.html

This is how log in was completed to utilize a 'session' variable
https://flask-login.readthedocs.io/en/latest/

This is how validation is done on signup form with python web tool forms WTforms  
https://wtforms.readthedocs.io/en/3.0.x/#   

This library is used to hash the pwd and is included in Flask
https://werkzeug.palletsprojects.com/en/2.3.x/utils/

This library is used to determine distance between two lat long points
https://pypi.org/project/geopy/


Questions
- "editing and updating the dataset" - does the csv files need to be edited, perhaps like edit one school/bus stop then overwright at next upload?
    - 'code' requirement says just read a csv file and store - not edit


Done
- import csv to the database for the busstop and the schools
- create test properties and populate the database propoerty table
- implement browse property functionality, a browse page that loads all propoerties from the database and displays them in a boostrap grid system using bootstrap cards 
- implement signup functionality, signup page with browser and server validation and stores new user in user table in database, hashes the pwd so it cant be read in db 
- implement login page, check email, pwd v database version, stores user in session 
- implement logout, accessed from menu
- check user is logged in 


TO DOs
- Pages
    - search page based on suburb, school, busroute
    - upload page for cvs - use code form the import scripts
    - create a edit profile page that works of signup userForm
    - data and definition of terms, including copyright ack from list of open source libraris as above, and images from chatgpt
    - simple forgot pwd page, with route that just dummy sends email
- Updates
    - validate email is unique on signup
    - create 'please login message' after signup
    - review pages for useability
        - titles on every page
        - headings on every page
        - images alt text, except decoration images - done, just review at end
        - test non-mouse tabbing - works now but test at the end
        - add required fields on signup page * (also the screen readers will understand the 'required' html tag)
    - copyright footer
    - admin user, and make admin page only work if authenticated and admin
    - change property description to be limited length so its ths same size cards
    - change logo from school to a cool logo



Notes for demo
- validation - sigup
    - use spaces to bypass in browser and show server side
    - also password match and business flag without a body
    - same email validate error
- validation - upload
    - the wtforms validators implement client side html5 std validation like
    - required feilds 
    - no file name or non csv browser stops
    - use school file for busses validation on service side
- search 
    - find a suburb with no schools
- login in session and authenticated access
    - show admin and logout menus are shown if user is in session
    - rest of menu kept the same for ux familiarity
    - so attempting to browse when not logged in directs user to login
- authenticated access
    - compare normal access for most pages
    - admin required for admin upload page
    - cant create admin user on the same interface as normal user - for now its a backend script 
- usability 
    - tab through sign up
    - select the label (using the for in label makes it work as well as the actual text box)
    - zoom 
        - using boostrap responsibve css will work for zoom and other resizing
    - could use a plugin for testing accessibility


options to extend
- use WTform on the signup 
- connect to the gov api instead of download a csv
- use a map for visualizing property, school and bus location - could use arcgis from gov api
- use a database that has native map support like postgress (postgis) that will speed up distance and mapping quieries
- support google and other major sso instead of creating users and storing pwd
- create an admin page to convert user to an admin user, and submission of properties
- or even better if there are more user types, seperate user and role and use authentication for sign on of a user
     and authorization system for role of the user (admin, realestate user, public user)
- implement forgot pwd/reset pwd fucntionality using flask-login extensions, also rememberme functionality 