 # Importing flask module in the project is mandatory
#Render template is used to load in HTML files
from flask import Flask, render_template,request, redirect, url_for, flash
import random
#Render template is used to load in HTML files
import sqlite3
import random

# We use this to set up our flask sever
app = Flask(__name__)
# the associated function.
@app.route('/')
# ‘/’ URL is bound with index() function.
def index():
    return render_template("index.html")
#start
###
#


def get_db_connection():
    conn = sqlite3.connect('login.db')
    conn.row_factory = sqlite3.Row
    return conn


    




@app.route('/add_timetable', methods=('POST', 'GET'))
def add_timetable():
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM library').fetchone()

    if request.method == 'POST':
        title = request.form['intitle']
        authour = request.form['inauthour']
        genre = request.form['ingenre']
        category = request.form['incategory']
        dp = request.form['indop']
        rating = request.form['inrating']
        description = request.form['indescription']
#        image = request.form['img']


        if not title or not authour or not genre or not category or not dp or not rating or not description:
            flash('All fields are required!')
        else:
            conn.execute('INSERT INTO library (title, authour, genre, category, published, rating, description) VALUES ( ?, ?, ?, ?, ?, ?, ?)', 
                         ( title, authour, genre, category, dp, rating, description))
            conn.commit()
            conn.close()
            return render_template('newbook.html')
            
    return render_template('newbook.html')

@app.route('/edit_timetable', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        user_name = request.form['userName']
        password = request.form['password']

        if not user_name or not password: 
            flash('All Fields required')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, password) VALUES (?,?)', (user_name, password))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template("index.html")

def edit_timetable(id):
    conn = get_db_connection()
    day1 = conn.execute('SELECT * FROM DayOne WHERE id=?', (id,)).fetchone()

    if request.method == 'POST':
        d1p1 = request.form['']
        d1p2 = request.form['']
        d1p3 = request.form['']
        d1p4 = request.form['']
        d1p5 = request.form['']
        d1p6 = request.form['']
        d1p7 = request.form['']

        if not user_name or not password: 
            flash('All fields are required!')
        else:
            conn.execute('UPDATE users SET username = ?, password = ? WHERE id = ?', 
                (user_name, password, id))
            conn.commit()
            conn.close()
            return redirect(url_for('edit_timetable'))
            
    return render_template('edit_timetable.html', day1=day1)

    

# main driver function #MAKE SURE THIS STAYS AT THE BOTTOM AT ALL TIMES
if __name__ == '__main__':
    app.run(debug=True,port=5448)