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
- vs code pets :)


-----------------
Done
- import csv to the database for the busstop and the schools
- create test houses and properties and populate the database propoerty table
- implement browse property functionality, a browse page that loads all propoerties from the database and displays them in a boostrap grid system using bootstrap cards 
- implement login page, check email, pwd v database version, stores user in session, create test user script
- implement logout, accessed from menu
- check user is logged in on routes and nav
- implement signup functionality, signup page with browser and server validation and stores new user in user table in database, hashes the pwd so it cant be read in db 
- validate email is unique on signup, use form validators for every field
- search page based on suburb, school, busroute - using distance for schools/busstops form property, use hover css to make data viewable
- implement consistent flash messaging for info and error - eg create 'please login message' after signup
- upload page for cvs - use code form the import scripts, validate correct headers and filename
- admin user, and make admin page and routes only work if authenticated and admin
- create a edit profile page that works of signup userForm and validates against pwd for security
- data and definition of terms, including copyright ack from list of open source libraris as above, and images from chatgpt
- simple forgot pwd page, with route that just dummy sends email
- change property description to be limited length so its ths same size cards
- change logo from school to a cool logo
- copyright footer
- usablity review:
    - titles on every page - every page has a title for browser using the title block - DONE
    - headings on every page - every page has a H4 title - DONE
    - images alt text, except decoration images - DONE
    - test non-mouse tabbing - DONE
    - add required fields on signup page * (also the screen readers will understand the 'required' html tag 
        that is used by required validator - but * helps too) -  DONE
- upload to cloud - https://qpc-2024.azurewebsites.net/
- delete white lines to make it easier to screen shot for final report





extensions
- Brad - wants to be close to High School - change search to look for school types
- be able to search on all the other data, ie lke a park for brad persona, and crime statistics in area, place all on a map
- connect to the gov api instead of download a csv to get faster updates if bus stop changes for example
- use a map for visualizing property, school and bus location - could use arcgis from gov api
- use a database that has native map support like postgress (postgis) that will speed up distance and mapping quieries
- support google and other major sso instead of creating users and storing pwd to increase security via two factor authenticaion
- create an admin page, than an existing admin can convert normal user to an admin user to reduce time to make admin
- extend admin page to allow updated and submission of properties so office team can do updates instead of IT
- implement forgot pwd/reset pwd fucntionality using flask-login extensions, also rememberme functionality 
- reduce duplicate code in signup and profile to make it more readable and supportable
- divide up app.py into smaller files to make it easier to support
- create automated tests to make change faster by reducing testing time



----------------
Demo

Landing page - 
- firsly lets load the home page and get a friendly welcome
- here lets look at the elements of the page, there is a title in the browser, a the common navigtaion menu top right, the copywrite footer. These all come form the common base.html template. 
- this common template also ensures our common style using boostratp 5 is used on all pages
- If I look at the navigation menu, it only shows the main functions so people can see what they can do if signup/login but does not show the sensitve options like admin and profile update as the jinja code in the template checks if there is an authenticated user in the session before showing those. 
- also if you select browse or search without logging in, the QPC app sends you back to login with a helpful erro, as the login decorator is blocking non authenitcated access inthe route code. 
- the base.html also ensures general errors are showing in a common style and location. 


Demo signup
- first lets look at the clients side code
- signup, has a  appropriate title in browser and heading at the right level. The style of showing placeholder text helps navigation. The required fields are indicated, and as per spec, the required fields not only have colout - but if press submit the browser side 'requried' flag in the input field will show the required fields
- This and natural flow of tab order helps with intercation with voice input for accesibility (press tab to go around all the fields, maybe press the check box with space to show it works). 
- All input feilds also have a label as per accessibility guidlines and if you click on the label the cursor goes to the input field making the selectable area larger (in spec)
- Similarly the min max lengths are validated clients side, as is email format required, and password is hidden from view. 
- If you hover over the input field when it is invalud (ie short input) it shows the validation rules.   

- once I start gettign enough data the form will be submitted to the app.py signup route and servier validation will implement these rules again - as good security not to trust the browser validation - brwoser validation helps speed up entry but server side must validate all data.  
- so to start testing - if I use spaces in name and occuptation, it will pass client browser validation, but will be picked up and show the server side validation in the wtform (userform.py), you can also see the rest of the data is not lost when the error is returned except the pwd as per normal pwd behavior, ie never store pwd in plain text even when accepting in a form
- if I use different matching passwords it will show custom server side validation in the wtform (userform.py)
- if I click real-estate but dont enter data it will show custom server side validation in the wtform (userform.py)
- lastly if you a use an email of an existing user, it will go the to custom validation in the signup route and suggest forgot password
- now the validation is tested, a successful signup takes you back to the login as per common security pattern
--- at this stage you could show he userform.py by switching between browser and code if you want?

Demo login
- enter email and pwd, the clients side validation checks its an email, and length. Press enter with no data. 
- The server side will load the user for the email and check the pwd. Note the pwd is hashed when stored so it is not readable in the database. The user provided login pwd is hashed then checked against the db stored pwd value. Press enter with incorect password to get an error. The pwd is no resupplied which is correct, but the email could be so with TODO fix this or say, the inputs not returned - ran out of time / or say nothing as its minor. 
- at this point could also so page for forgot password, whcih will then take you back to do the login again. 
- completing the login, if found the Flask Login Manager loads the user into the session. Then on subsequent requests, say to update profile the @Login_Required decorator is used to ensure the current user in the session is logged in. 


Demon browse
- once logged in the user is taken to search, they can also access browse and update, see in top right menu
- then just jump into browse to show what its like, a grid of properties in a common design style
- this could be good for the 'David' persona who wants to learn about the brisbane real-estate
- can explain that all images and descriptions were generated with open.ai chatgpt 4 and Dalle. 
- can show here that hte layout is responsive based on bootstrap five grid
( the descriptions are setup so the tiles should all look the same at a normal size window)
- as reduce the browser window it resizes the grid - responsiev, dynamic. Does also work on mobile

Search
- jumping back to search, both 'Brad' who wants to be close to school  and 'Helen' persona looking for close to school and commuting links. The search could be extended for many criteria or with a map, but to meet the primary requirements of REIQ the search allows the user to select a suburb then how far away they prefer schools and bus stops. 
- This search uses the lat long from the gov school, bus stops to compare to the lat long of the properties in the suburb and find the direct distance over the earth using the python library. The datapolicy page describes this also for the user. 
- selecting sandgate and distance 2km, bus stop 1km, search returns the two properties in sandgate - allowing a comparison for the user. The form also returns the data so its there if the user wants to refine the search
- the search returns properties and also shows via a hover the schools and bus stops. The bus stops is a lot so perhaps change to a shorter distance of 500 meters

Profile
- now that I have some properties, the user perhaps realizes they may have put in an incorrect occupation and needs to update it, jump over to profile page where I empower the user to maintain their personal data
- here a majority of the validation is using the same code via the wtfrom userform.py UserForm object. But in this case I dont allow password update here, that has to be done via email to provide an additional fator in the authenticaiton chance, so the route code manages that difference

Admin
- moving on, lets run a scenario where the QLD gov has updated the latest school data. In an extended version you could link to their api, but in the specs of this version for REIQ I need to upload a new version of the data via csv
-  You can see that there is no admin option to udpate the bus an school data as the current user is not an admin. 
- creating an admin user expereince was out of scope so I have used a script to set the is_admin to true on the user John.smith - see the detail in the madeadmin.py script
- so if I log off, and then login with the john.smith user, I cna now see an admin option in the menu. Our flask app both checks the admin in the base.html teamplate that contains the common nav bar, and also checks it in the admin routes. So client and server side validation. 
- selecting admin I can press upload and if no file, it provides an error. 
- if I upload a busfile by mistake it will the validation rules will determine it has the wrong headers in the csv and provide a helpful error
- if I do eventually upload the correct file name I will see that 1774 schools were updated successfull. so this has now successfully run algorthims to check the data has the correct headers and updated schools data base table. I can now do a search on sandgate as I did before and notice that the sacred heart school now has an s on the name which is the only differnece in my new test file. 
(serach for sandgate - 1km schools and verify that the Sacret heart sandgate school is subtly different with an extra s in heart -> hearts)



Data Policy
- Now admin is complete, the last of the required functionality is a page to describe the definition of terms, the source of the data and how I use it so users understand  

Logout
- with that I am done and now will logout, I can use the top right logout and then that takes us back to login if they wish to keep the page open. you can see the profile, admin links are now gone, and using those browse and search require us to login. I did consider hiding those but saw other sites with good design to keep them so people understnad the common feel and where the functionality is. 



















