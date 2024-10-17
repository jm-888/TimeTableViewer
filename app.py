# Importing flask module in the project is mandatory
#Render template is used to load in HTML files
from flask import Flask, render_template,request, redirect, url_for, flash
import random
#Render template is used to load in HTML files
import sqlite3
import random

# We use this to set up our flask sever
app = Flask(__name__)

# The route( tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with index() function.
def index():
    return render_template("index.html")

@app.route('/count')
def count():
    numbers = list(range(1, 11))  # List of numbers from 1 to 10
    return render_template('count.html', numbers=numbers)

@app.route('/names')
def names():
    names = ["Liam", "Hanah", "Lauren", "Owen", "Harrison", "David"]
    return render_template('names.html',names=names)

@app.route('/random')
def random_num():
    num = random.randint(1,100)
    return render_template('random.html',num=num)



@app.route('/guess',methods=('GET','POST'))

def guess():
    try:
        num = -1
        if request.method == 'POST':
            num = request.form['number']
            print(num)
        if int(num) <= -1:
            return render_template('number.html')
        else:
            print(num)
            if int(num) == 10:
                ans = "You got it!"
                return render_template('number.html', ans=ans)
            else:
                ans = "Incorrect!"
                return render_template('number.html',ans=ans)
    except:
        ans = "Please only type in interger values"
        return render_template('number.html',ans=ans)

        # Database connection function
def get_db_connection():
    conn = sqlite3.connect('login.db')
    conn.row_factory = sqlite3.Row
    return conn
    
# Initialize the database with a games table
def init_db():
    conn = get_db_connection() 
    with app.open_resource('schema.sql') as f:
        conn.executescript (f.read().decode('utf8'))
    conn.close()

@app.route('/login', methods=('POST', 'GET'))
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
    return render_template("login.html")

@app.route('/admin')
def admin():
    conn = get_db_connection()
    sql = "SELECT * FROM users"
    users = conn.execute(sql).fetchall()
    conn.close()
    return render_template('view_users.html', users=users)
# Route to edit a game
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_user(id):
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users WHERE id=?', (id,)).fetchone()

    if request.method == 'POST':
        user_name = request.form['userName']
        password = request.form['password']

        if not user_name or not password: 
            flash('All fields are required!')
        else:
            conn.execute('UPDATE users SET username = ?, password = ? WHERE id = ?', 
                (user_name, password, id))
            conn.commit()
            conn.close()
            return redirect(url_for('admin'))
            
    return render_template('edit_user.html', users=users)

    #Route to delete a game
@app.route('/delete/<int:id>', methods=('POST',))
def delete_user(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('User deleted successfully!')
    return redirect(url_for('admin'))

@app.route('/join', methods=['GET', 'POST']) 
def join(): 
    if request.method == 'POST': 
        name = request.form['name'] 
        email = request.form['email'] 
        city = request.form['city'] 
        country = request.form['country'] 
        phone = request.form['phone'] 
  
        with sqlite3.connect("database.db") as users: 
            cursor = users.cursor() 
            cursor.execute("INSERT INTO PARTICIPANTS \
            (name,email,city,country,phone) VALUES (?,?,?,?,?)", 
                           (name, email, city, country, phone)) 
            users.commit() 
        return render_template("index.html") 
    else: 
        return render_template('join.html') 
  
  
@app.route('/participants') 
def participants(): 
    connect = sqlite3.connect('database.db') 
    cursor = connect.cursor() 
    cursor.execute('SELECT * FROM PARTICIPANTS') 
  
    data = cursor.fetchall() 
    return render_template("participants.html", data=data) 

  

# main driver function #MAKE SURE THIS STAYS AT THE BOTTOM AT ALL TIMES
if __name__ == '__main__':
    app.run(debug=True,port=5448)


