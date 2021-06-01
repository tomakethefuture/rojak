from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import User, Attendance, Profiles
from .auth import check_password_hash, generate_password_hash
import datetime
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    username = current_user.username
    return render_template("home.html", user=current_user, username=username)



@views.route('/attendance', methods = ['GET', 'POST'])
@login_required
def attendance():
    received = request.form
    print(received)
    username = current_user.username
    data = Attendance.query.all()
    if request.method == 'POST':
        add_or_check = request.form.get('add_or_check')
        if add_or_check == 'check':
            input_id = request.form.get('employee_id')
            id_exist = Profiles.query.filter_by(id=input_id).first()
            if id_exist:
                msg = "Employee ID Found"
                now = datetime.now()
                name = id_exist.name
                date = now.strftime("%d-%m-%Y")
                time = now.strftime("%H:%M:%S")
                return render_template('add_attendance.html',user=current_user, employee_found=True, msg=msg, employee_id=input_id, name=name, date=date, time=time)
            else:
                flash("Employee ID NOT Found", category='error')
        elif add_or_check == 'add':
            id = request.form.get('employee_id')
            name = request.form.get('employee_name')
            date = request.form.get('date')
            time = request.form.get('time')
            status = request.form.get('status')
            new_attendance = Attendance(id=id, name=name, date=date, time=time, status=status)
            db.session.add(new_attendance)
            db.session.commit()
            flash('Added New Record of Attendance!', category='success')
            return redirect(url_for('views.attendance'))
        elif add_or_check == 'custom':
            id = request.form.get('employee_id')
            id_exist = Profiles.query.filter_by(id=id).first()
            if id_exist:
                name = id_exist.name
                date = request.form.get('date')
                day = date[8:10]
                month = date[5:7]
                year = date[0:4]
                date = day + "-" + month + "-" + year
                hour = request.form.get('hour')
                if len(hour) == 1:
                    hour = "0" + hour
                minute = request.form.get('minute')
                if len(minute) == 1:
                    minute = "0" + minute
                second = request.form.get('second')
                if len(second) == 1:
                    second = "0" + second
                time = hour + ":" + minute + ":" + second
                status = request.form.get('status')
                new_attendance = Attendance(id=id, name=name, date=date, time=time, status=status)
                db.session.add(new_attendance)
                db.session.commit()
                flash('Updated Attendance', category='success')
                return redirect(url_for('views.attendance'))
            else:
                flash('Employee ID Does NOT Exist', category='error')
                return redirect(url_for('views.attendance'))
        elif add_or_check == 'search':
            id = request.form.get('id')
            if not id:
                id = ""
            name = request.form.get('name')
            if not name:
                name = ""
            date = request.form.get('date')
            date_filter = ""
            if date:
                day = date[8:10]
                print(day)
                month = date[5:7]
                print(month)
                year = date[0:4]
                print(year)
                search_range = request.form.get('search_range')
                if search_range == 'year':
                    date_filter = year
                elif search_range == 'month':
                    date_filter = month + "-" + year
                elif search_range == 'day':
                    date_filter = day + "-" + month + "-" + year
            else:
                date = ""

            search_range = request.form.get('search_range')
            search_query = Attendance.query.filter(
                Attendance.id.like('%' + id + '%'),
                Attendance.name.like('%' + name + '%'),
                Attendance.date.like('%' + date_filter + '%')
            ).all()
            if not search_query:
                no_results = True
            return render_template('attendance.html', attendance=search_query, user=current_user, username=username, no_results=no_results)
    return render_template('attendance.html', attendance=data, user=current_user, username=username)

@views.route('/employee_list', methods =['GET', 'POST'])
@login_required
def employee_list():
    username = current_user.username
    data = Profiles.query.all()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun' ,'Jul','Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    if request.method == 'POST':
        add_or_check = request.form.get('add_or_check')
        if add_or_check == 'search':
            id = request.form.get('id')
            if not id:
                id = ""
            name = request.form.get('name')
            if not name:
                name = ""
            gender = request.form.get('gender')
            if gender == 'Any':
                gender = ""
            date = request.form.get('date')
            date_filter = ""
            if date:
                day = date[8:10]
                print(day)
                month = date[5:7]
                print(month)
                year = date[0:4]
                print(year)
                search_range = request.form.get('search_range')
                if search_range == 'year':
                    date_filter = year
                elif search_range == 'month':
                    date_filter = month + "-" + year
                elif search_range == 'day':
                    date_filter = day + "-" + month + "-" + year
            else:
                date = ""
            age = request.form.get('age')
            if age == 'Any':
                age = ""
            department = request.form.get('department')
            if department == 'Any':
                department = ""
            search_range = request.form.get('search_range')
            search_query = Profiles.query.filter(
                Profiles.id.like('%' + id + '%'),
                Profiles.name.like('%' + name + '%'),
                Profiles.gender.like('%' + gender + '%'),
                Profiles.birthdate.like('%' + date_filter + '%'),
                Profiles.age.like('%' + age + '%'),
                Profiles.department.like('%' + department + '%')
            ).all()
            if not search_query:
                no_results = True
            else:
                no_results = False
            return render_template('employee_list.html', employees=search_query, user=current_user, username=username, no_results=no_results)
        else:
            id = request.form.get('employee_id')
            name = request.form.get('employee_name')
            department = request.form.get('employee_department')
            gender = request.form.get('employee_gender')
            id_exists = Profiles.query.filter_by(id=id).first()
            if id_exists:
                flash('Employee already exist with current ID.', category='error')
            elif len(id) < 14:
                flash('Invalid Format for ID.', category='error')
            else:
                currentyear = datetime.now().strftime("%Y")
                sliced_currentyear = int(currentyear[2:4])
                birthyear = id[0:2]
                if sliced_currentyear - int(birthyear) < 0:
                    birthyear = "19" + str(birthyear)
                else:
                    birthyear = currentyear[0:2] + str(birthyear)
                age = int(currentyear) - int(birthyear)
                birthmonth = months[int(id[2:4])-1]
                birthdate = id[4:6] + "/" + birthmonth + "/" + birthyear
                new_employee = Profiles(id=id, name=name,department=department, gender=gender, age=age, birthdate=birthdate)
                db.session.add(new_employee)
                db.session.commit()
                flash('Successfully Added New Employee.', category='success')
                return redirect(url_for('views.employee_list'))
    return render_template('employee_list.html', employees=data, user=current_user, username=username)

@views.route('/account_settings', methods = ['GET', 'POST'])
@login_required
def account_settings():
    username = current_user.username
    name = current_user.name
    email = current_user.email
    password = current_user.password
    return render_template('account_settings.html', user=current_user, username=username, name=name, email=email, password=password)

@views.route('/change_password', methods = ['GET', 'POST'])
@login_required
def change_password():
    username = current_user.username
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password1 = request.form.get('new_password1')
        new_password2 = request.form.get('new_password2')
        userpasswordhash = current_user.password
        if not check_password_hash(userpasswordhash, current_password):
            flash('Password Incorrect',category='error')
        elif len(new_password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif new_password1 != new_password2:
            flash("New passwords don't match.",category='error')
        else:
            current_user.password = generate_password_hash(new_password1,method='SHA256')
            db.session.commit()
            flash("Successfully changed password.",category='success')
            return redirect(url_for('views.account_settings'))
    return render_template('change_password.html', user=current_user, username=username)

