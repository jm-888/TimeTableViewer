# Importing flask module in the project is mandatory
#Render template is used to load in HTML files
from flask import Flask, render_template,request, redirect, url_for, flash
import random
#Render template is used to load in HTML files
import sqlite3

# We use this to set up our flask sever
app = Flask(__name__)

# The route( tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with index() function.
def index():
    return render_template("index.html")



@app.route('/edit_timetable', methods=['GET', 'POST']) 
def edit(): 
    if request.method == 'POST': 
        name = request.form['name'] 
        email = request.form['email'] 
        city = request.form['city'] 
        country = request.form['country'] 
        phone = request.form['phone'] 
  
        with sqlite3.connect("TimeTable.db") as users: 
            cursor = users.cursor() 
            cursor.execute("INSERT INTO timetable (name,email,city,country,phone) VALUES (?,?,?,?,?)",(name, email, city, country, phone)) 
            users.commit() 
        return render_template("index.html") 
    else: 
        return render_template('edit_timetable.html') 
  
  
@app.route('/timetable') 
def timetable_display(): 
    connect = sqlite3.connect('TimeTable.db') 
    cursor = connect.cursor() 
    cursor.execute('SELECT * FROM sqlite_master;') 
    data = cursor.fetchall() 
    return render_template("timetable.html", data=data) 

  

# main driver function #MAKE SURE THIS STAYS AT THE BOTTOM AT ALL TIMES
if __name__ == '__main__':
    app.run(debug=True,port=5448)


