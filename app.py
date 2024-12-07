# Authors: Vaishu, Ashley, Kathy, and Mukhlisa

from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, send_file, jsonify)
from werkzeug.utils import secure_filename
from PIL import Image
app = Flask(__name__)

import os
import pymysql
import cs304dbi as dbi
import queries as db

import secrets

app.secret_key = secrets.token_hex()

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

# new for file upload
app.config['UPLOADS'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1*1024*1024 # 1 MB

departments = None

@app.route('/')
def home():
    conn = dbi.connect()
    # hardcode user values since draft version does not have sign-up/login functionality
    # session['uid'] = 1
    # session['email'] = 'jc103@wellesley.edu'
    # session['name'] = 'Vaishu Chintam'

    # get all department names and cache it
    global departments 
    if departments is None:
        departments = db.get_departments(conn)

    return render_template('base.html', page_title='Home', departments=departments)

@app.route('/signup/', methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        passwd1 = request.form.get('password1')
        passwd2 = request.form.get('password2')

        incorrect_info = False
        if not email.endswith('@wellesley.edu'):
            flash('Email must be a valid Wellesley College email (@wellesley.edu)')
            incorrect_info = True
        if passwd1 != passwd2:
            flash('passwords do not match')
            incorrect_info = True
        if incorrect_info:
            return redirect( url_for('signup'))
        
        conn = dbi.connect()
        (uid, is_dup, other_err) = db.insert_user(conn, email, name, passwd1)
        if other_err:
            raise other_err
        elif is_dup:
            flash('Sorry; that username is taken')
            return redirect( url_for('signup'))
        else:
            ## success
            session['email'] = email
            session['uid'] = uid
            session['name'] = name
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('signup.html', page_title='Signup')

@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        passwd = request.form.get('password')
        conn = dbi.connect()
        (ok, uid, name) = db.login_user(conn, email, passwd)
        if ok:
            ## success
            print('LOGIN', email)
            flash('successfully logged in as '+email)
            session['email'] = email
            session['uid'] = uid
            session['name'] = name
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Login incorrect, please try again or sign up')
    return render_template('login.html', page_title='Login')

@app.route('/logout/')
def logout():
    if 'email' in session:
        session.pop('email')
        session.pop('uid')
        session.pop('name')
        session.pop('logged_in')
        flash('You are logged out')
        return redirect(url_for('home'))
    else:
        flash('you are not logged in. Please login or join')
        return redirect( url_for('home') )

@app.route('/department/')
def select_department():
    conn = dbi.connect()
    department = request.args.get('department')

    data = db.get_courses_by_department(conn, department)

    if len(data) == 0:
        # let user know that no matches were found 
        flash('No courses found for this department.')

    return render_template('department_courses.html', 
                           page_title='Department Courses', 
                           data = data, 
                           department = department,
                           departments=departments)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    conn = dbi.connect()
    departments = db.get_departments(conn)
    if request.method == 'POST':
        course_code = request.form.get('course_code')
        course_name = request.form.get('course_name')
        department = request.form.get('department')
        # check if course code is correct format
        try:
            parts = course_code.split()
            if len(parts) != 2 or not parts[0].isalpha() or not parts[1].isdigit():
                raise ValueError  # Raise an error if the format is invalid
            
             # Capitalize the letter part
            parts[0] = parts[0].upper() 
            course_code = ' '.join(parts)
        except ValueError:
            flash('Invalid course code format. Format must be course department letter then course number (e.g., "CS 101").')
            return redirect(url_for('add_course'))

        #check if course already exists
        existing_course = db.get_course_by_course_code(conn, course_code)
        if existing_course:
            flash('This course already exists in the database.')
            return redirect(url_for('add_course'))

        #if successful and course does not exist then insert course
        dept_id = db.get_department_id(conn, department) 
        # make thread-safe
        try:
            db.insert_course(conn, course_code, course_name, dept_id)
            flash('Course added successfully!')
        except pymysql.IntegrityError as err:
                print('Unable to insert {} due to {}'.format(course_code,repr(err))) 
        
        return redirect(url_for('select_department', department=department))  # Redirect back to the department page
    else:
        return render_template('add_courses.html', page_title='Add Course', departments=departments) 

@app.route('/courses/<cid>')
def display_course(cid):
    conn = dbi.connect()
    # get all reviews for course
    int_cid = int(cid)
    info_review = db.get_course_reviews(conn, int_cid)

    ## below will capture course_code and name from cid
    info_course = db.get_course_info_by_cid(conn, int_cid)

    if not info_course:
        # If no course is found with the given cid, redirect to home page
        flash('Course not found.')
        return redirect(url_for('home'))

    if len(info_review) == 0:
        flash('No reviews found for this course.')

    return render_template('course_reviews.html', 
                           page_title='Course Reviews',
                           reviews = info_review,
                           course = info_course,
                           length = len(info_review),
                           departments=departments)

@app.route('/add_review/<course_code>/<cid>', methods=['GET', 'POST'])
def add_review(course_code, cid):
    # course_code is the department abbrev. and course num (ex. CS 111)
    # cid is the course id number as stored in the course table
    if request.method == 'POST':
        conn = dbi.connect()

        review_data = {
            'prof_name': request.form.get('prof_name'),
            'prof_rating': request.form.get('prof_rating'),
            'difficulty': request.form.get('difficulty'),
            'credit': request.form.get('credit'),
            'sem': request.form.get('sem'),
            'year': request.form.get('year'),
            'take_again': request.form.get('take_again'),
            'load_heavy': request.form.get('load_heavy'),
            'office_hours': request.form.get('office_hours'),
            'helped_learn': request.form.get('helped_learn'),
            'stim_interest': request.form.get('stim_interest'),
            'description': request.form.get('description')
        }

        user_id = session.get('uid') # get user id from session 
        int_cid = int(cid)

        # insert professor into professor table if prof_name not already in the table
        prof_data = db.get_prof_by_name(conn, review_data['prof_name'])
        if not prof_data:
            # get department id for the course
            course_data = db.get_course_info_by_cid(conn, int_cid)
            dept_id = course_data['did']

            # make thread-safe 
            try: 
                db.insert_professor(conn, review_data['prof_name'], dept_id)
            except pymysql.IntegrityError as err:
                print('Unable to insert {} due to {}'.format(review_data['prof_name'],repr(err)))

        # get professor id 
        prof = db.get_prof_by_name(conn, review_data['prof_name'])
        prof_id = prof['pid']

        # add user id, prof id, and course id to review_data 
        review_data.update({
            'cid': int_cid,
            'user_id': user_id,
            'prof_id': prof_id
        }) 

        # insert review
        db.insert_review(conn, review_data)

        flash("Review added successfully!")
        return redirect(url_for('display_course', cid=cid))
    else:
        return render_template('add_review.html', 
                               page_title='Add Review', 
                               course_code=course_code,
                               cid = cid,
                               departments=departments)
    
@app.route('/edit_review/<course_code>/<rid>', methods=['GET', 'POST'])
def edit_review(course_code, rid):
    conn = dbi.connect()
    # fetch existing review data
    rid = int(rid)
    review = db.get_review_by_id(conn, rid)
    if not review:
        flash("Review not found.")
        return redirect(url_for('profile')) 
    
    # check if the current user logged in is authorized to edit the review
    user_id = session.get('uid')
    if review['user_id'] != user_id:
        flash("You are not authorized to edit this review.")
        return redirect(url_for('profile'))

    if request.method == 'POST':
        # get updated data from form submission
        updated_data = {
            'prof_name': request.form.get('prof_name'),
            'prof_rating': request.form.get('prof_rating'),
            'difficulty': request.form.get('difficulty'),
            'credit': request.form.get('credit'),
            'sem': request.form.get('sem'),
            'year': request.form.get('year'),
            'take_again': request.form.get('take_again'),
            'load_heavy': request.form.get('load_heavy'),
            'office_hours': request.form.get('office_hours'),
            'helped_learn': request.form.get('helped_learn'),
            'stim_interest': request.form.get('stim_interest'),
            'description': request.form.get('description')
        }

        updated_data.update({
            'rid': rid
        }) 

        # update the review in the database
        db.update_review(conn, updated_data)
        flash("Review updated successfully!", "success")
        return redirect(url_for('profile'))
    else:
        return render_template('edit_review.html', course = course_code, review=review)

@app.route('/delete_review/<rid>')
def delete_review(rid):
    conn = dbi.connect()
    db.delete_review(conn, int(rid))
    flash('Review deleted successfully!')
    return redirect(url_for('profile'))

@app.route('/profile/')
def profile():
    conn = dbi.connect()

    uid = session.get('uid')
    email = session.get('email')
    name = session.get('name')


    info_review = db.get_profile_reviews(conn, uid)
    if len(info_review) == 0:
        flash('No reviews found for this user.')
    

    return render_template('profile.html', page_title='Profile', 
                                           uid=uid, 
                                           src=url_for('pic',uid=uid),
                                           email=email, 
                                           name=name,
                                           reviews=info_review,
                                           departments=departments)

@app.route('/pic/<uid>')
def pic(uid):
    conn = dbi.connect()
    picfile = db.get_pic(conn, uid)

    if picfile == None:
        flash('No picture uploaded')
        return send_from_directory(app.config['UPLOADS'], 'default.jpg')
        # return redirect(url_for('profile'))
    
    return send_from_directory(app.config['UPLOADS'],picfile['filename'])


@app.route('/profile/upload', methods=["GET", "POST"])
def file_upload():
    conn = dbi.connect()
    uid = session.get('uid')

    if request.method == 'GET':
        return render_template('add_profile_pic.html',src='',uid='')
    else:
        try:
            f = request.files['pic']
            user_filename = f.filename
            ext = user_filename.split('.')[-1]
            filename = secure_filename('{}.{}'.format(uid,ext))
            pathname = os.path.join(app.config['UPLOADS'],filename)

            # Check if file with the same uid exists
            existing_files = [file for file in os.listdir(app.config['UPLOADS']) if file.startswith(f"{uid}.")]
            for existing_file in existing_files:
                os.remove(os.path.join(app.config['UPLOADS'], existing_file))

            # resize image
            try:
                img = Image.open(f)
                target_width = 200
                w_percent = target_width / float(img.size[0])
                target_height = int(float(img.size[1]) * w_percent)
                img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                img.save(pathname)
            except Exception as e:
                flash(f'Image processing failed: {e}')
                return redirect(url_for('file_upload'))

            # f.save(pathname)
            db.upload_pic(conn, uid, filename)
            flash('Upload successful')
            return redirect(url_for('profile'))
        except Exception as err:
            flash('Upload failed {why}'.format(why=err))
            return render_template('profile.html')


if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()

    db_to_use = 'cwise_db' 
    print(f'will connect to {db_to_use}')
    dbi.conf(db_to_use)
    app.debug = True
    app.run('0.0.0.0',port)
