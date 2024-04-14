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
- validate email is unique on signup
- search page based on suburb, school, busroute
- create 'please login message' after signup
- upload page for cvs - use code form the import scripts
 - admin user, and make admin page only work if authenticated and admin

TO DOs
- Pages
    - create a edit profile page that works of signup userForm
    - data and definition of terms, including copyright ack from list of open source libraris as above, and images from chatgpt
    - simple forgot pwd page, with route that just dummy sends email
- Updates
    - review pages for useability
        - titles on every page
        - headings on every page
        - images alt text, except decoration images - done, just review at end
        - test non-mouse tabbing - works now but test at the end
        - add required fields on signup page * (also the screen readers will understand the 'required' html tag)
    - copyright footer
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


extensions
- be able to search on all the other data, ie lke a park for brad persona, and crime statistics in area, place all on a map
- connect to the gov api instead of download a csv to get faster updates if bus stop changes for example
- use a map for visualizing property, school and bus location - could use arcgis from gov api
- use a database that has native map support like postgress (postgis) that will speed up distance and mapping quieries
- support google and other major sso instead of creating users and storing pwd to increase security via two factor authenticaion
- create an admin page, than an existing admin can convert normal user to an admin user to reduce time to make admin
- extend admin page to allow updated and submission of properties so office team can do updates instead of IT
- implement forgot pwd/reset pwd fucntionality using flask-login extensions, also rememberme functionality 



setup instructions
- download vscode
- follow get started prompt
    - python extension
    - download python from microsfot store or python site for mac
    - connect to github
- install copilot extension
- got to source control tab
    - follow instructions to install git on windows/mac
    - open command promopt, set defults
        - git config --global user.email "caitlin.pett@gmail.com"
        - git config --global user.name "Caitlin Pett"
    - clone repo - QPC

- setup python env to run app
    - go to requirements.txt in VsCode and create env -or use teh command
    - open app.py - select debug and run, python
    - go to 127.0.0.1:5000 or right click link

intall extra extensions
- python indent
- jinja for jinja syntax hightlight
- intellicode
- sqlite - simplest db view - many other choices
- csv rainbow - for csv colour highlighting
- live share - for in vscode live sharing
