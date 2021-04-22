from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ghuanying1115'
app.config['MYSQL_DB'] = 'rfid'

mysql = MySQL(app)


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM attendance")
    data = cur.fetchall()
    cur.close()

    return render_template('index2.html', attendance=data)


@app.route('/insert', methods=['POST', 'GET'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        id = request.form['id']
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO attendance (id, name, date, time, status) VALUES (%s, %s, %s, %s, %s)", (id, name, date, time, status))
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>/<string:name>/<string:date>/<string:time>/<string:status>', methods=['GET'])
def delete(id, name, date, time, status):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM attendance WHERE id=%s and name=%s and date=%s and time=%s and status=%s",
                (id, name, date, time, status))
    mysql.connection.commit()
    return redirect(url_for('Index'))


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        old_id = request.form['old_id']
        old_name = request.form['old_name']
        old_date = request.form['old_date']
        old_time = request.form['old_time']
        old_status = request.form['old_status']
        new_id = request.form['id']
        new_name = request.form['name']
        new_date = request.form['date']
        new_time = request.form['time']
        new_status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE attendance
               SET id=%s, name=%s, date=%s, time=%s, status=%s
               WHERE id=%s and name=%s and date=%s and time=%s and status=%s
            """, (new_id, new_name, new_date, new_time, new_status, old_id, old_name, old_date, old_time, old_status))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(host='192.168.0.166')
