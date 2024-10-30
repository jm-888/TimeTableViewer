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
    conn = sqlite3.connect('TimeTable.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db


@app.route('/add_timetable', methods=('POST', 'GET'))
def add_timetable():
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM day').fetchone()

    if request.method == 'POST':
        task = request.form['intitle']
        time = request.form['inauthour']
        location = request.form['ingenre']
        description = request.form['incategory']

        if not task or not time or not location or not description:
            flash('All fields are required!')
        else:
            conn.execute('INSERT INTO day (task, time, location, description) VALUES ( ?, ?, ?, ?)', 
                         ( task, time, location, description))
            conn.commit()
            conn.close()
            return render_template('add_timetable.html')
            
    return render_template('add_timetable.html')

@app.route('/edit_timetable', methods=('POST', 'GET'))
def edit_timetable(id):
    conn = get_db_connection()
    day1 = conn.execute('SELECT * FROM DayOne WHERE id=?', (id,)).fetchone()

    if request.method == 'POST':
        task = request.form['']
        time = request.form['']
        location = request.form['']
        description = request.form['']

        if not d1p1 or not password: 
            flash('All fields are required!')
        else:
            conn.execute('UPDATE users SET username = ?, password = ? WHERE id = ?', 
                (user_name, password, id))
            conn.commit()
            conn.close()
            return redirect(url_for('edit_timetable'))
            
    return render_template('edit_timetable.html')

    

# main driver function #MAKE SURE THIS STAYS AT THE BOTTOM AT ALL TIMES
if __name__ == '__main__':
    app.run(debug=True,port=5448)