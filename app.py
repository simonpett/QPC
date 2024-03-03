from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')                                                                 #use the route() decorator to tell Flask what URL should trigger our functions
def index():                                                                    # createa a route for the landing / home page  
    return render_template('index.html')    

if __name__ == '__main__':
    app.run()