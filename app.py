 # Importing flask module in the project is mandatory
#Render template is used to load in HTML files
from flask import Flask, render_template,request, redirect, url_for, flash
import random
#Render template is used to load in HTML files
import sqlite3
import random

# We use this to set up our flask sever
app = Flask(__name__)
app.secret_key = "kylebvenjaminuy"  


# the associated function.
@app.route('/')
def index():
    conn = get_db_connection()
    
    # Fetch all tasks from the 'day' table
    day_tasks = conn.execute('SELECT * FROM day').fetchall()
    
    # Close the connection
    conn.close()
    
    # Check if the request method is POST (for adding new tasks)
    if request.method == 'POST':
        task = request.form['task']
        time = request.form['time']
        location = request.form['location']
        description = request.form['description']
        
        # Add logic to insert the new task into the database here
        # Example: 
        conn = get_db_connection()
        conn.execute('INSERT INTO day (task, time, location, description) VALUES (?, ?, ?, ?)', 
                     (task, time, location, description))
        conn.commit()
        conn.close()

        # Redirect to the same page to display updated tasks
        return redirect(url_for('index'))

    # Render the template and pass the tasks to it
    return render_template("index.html", day=day_tasks)



def get_db_connection():
    conn = sqlite3.connect('TimeTable.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection() 
    with app.open_resource('schema.sql') as f:
        conn.executescript (f.read().decode('utf8'))
    conn.close()

@app.route('/view_timetable', methods=('POST', 'GET'))
def view_timetable ():
    conn = get_db_connection()
    sql = "SELECT * FROM day"
    day = conn.execute(sql).fetchall()
    conn.close()
    return render_template('view_timetable.html', day=day)

@app.route('/add_timetable', methods=('POST', 'GET'))
def add_timetable():
    conn = get_db_connection()
    day = conn.execute('SELECT * FROM day').fetchone()

    if request.method == 'POST':
        task = request.form['task']
        time = request.form['time']
        location = request.form['location']
        description = request.form['description']

        if not task or not time or not location or not description:
            flash('All fields are required!')
        else:
            conn.execute('INSERT INTO day (task, time, location, description) VALUES ( ?, ?, ?, ?)', 
                         ( task, time, location, description))
            conn.commit()
            conn.close()
            return render_template('add_timetable.html')
            
    return render_template('add_timetable.html')

@app.route('/edit_timetable/<int:id>', methods=('POST', 'GET'))
def edit_timetable(id):
    conn = get_db_connection()
    day = conn.execute('SELECT * FROM day WHERE id=?', (id,)).fetchone()

    if request.method == 'POST':
        task = request.form['task']
        time = request.form['time']
        location = request.form['location']
        description = request.form['description']

        if not task or not time or not location or not description:
            flash('All fields are required!')
        else:
            conn.execute('UPDATE day SET task = ?, time = ?, location = ?, description = ? WHERE id = ?', 
                (task, time, location, description, id))
            conn.commit()
            conn.close()
            return redirect(url_for('view_timetable'))
            
    return render_template('edit_timetable.html')

@app.route('/delete/<int:id>', methods=('POST',))
def delete_timetable(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM day WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Task deleted successfully!')
    return redirect(url_for('index'))


# main driver function #MAKE SURE THIS STAYS AT THE BOTTOM AT ALL TIMES
if __name__ == '__main__':
    app.run(debug=True,port=5448)