from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)


import queries as db

import secrets

app.secret_key = secrets.token_hex()

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

departments = None

@app.route('/')
def home():
    # hardcode user values since draft version does not have sign-up/login functionality
    session['uid'] = 1
    session['email'] = 'jc103@wellesley.edu'
    session['name'] = 'Vaishu Chintam'

    global departments 
    if departments is None:
        departments = db.get_departments()

    return render_template('base.html', page_title='Home', departments=departments)


@app.route('/department/')
def select_department():
    department = request.args.get('department')

    data = db.get_courses_by_department(department)

    if len(data) == 0:
        # let user know that no matches were found 
        flash('No courses found for this department.')

    return render_template('department_courses.html', 
                           page_title='Department Courses', 
                           data = data, 
                           department = department,
                           departments=departments)

@app.route('/courses/<cid>')
def display_course(cid):
    # get all reviews for course
    info_review = db.get_course_reviews(int(cid))

    ## below will capture course_code and name from cid
    info_course = db.get_course_info_by_cid(cid)

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
    if request.method == 'POST':
        prof_name = request.form.get('prof_name')
        prof_rating = request.form.get('prof_rating')
        difficulty = request.form.get('difficulty')
        credit = request.form.get('credit')
        sem = request.form.get('sem')
        year = request.form.get('year')
        take_again = request.form.get('take_again')
        load_heavy = request.form.get('load_heavy')
        office_hours = request.form.get('office_hours')
        helped_learn = request.form.get('helped_learn')
        stim_interest = request.form.get('stim_interest')
        description = request.form.get('description')

        user_id = session.get('uid') # get user id from session 

        # insert professor into professor table if prof_name not already in the table
        prof_data = db.get_prof_by_name(prof_name)
        if not prof_data:
            # get department id for the course
            course_data = db.get_course_info_by_cid(int(cid))
            dept_id = course_data['did']

            db.insert_professor(prof_name, dept_id)

        # get professor id 
        prof = db.get_prof_by_name(prof_name)
        prof_id = prof['pid']

        # insert review
        db.insert_review(int(cid), user_id, prof_name, prof_rating, prof_id, difficulty, credit, sem, year, take_again, load_heavy, office_hours, helped_learn, stim_interest, description)

        flash("Review added successfully!")
        return redirect(url_for('display_course', cid=cid))
    else:
        return render_template('add_review.html', 
                               page_title='Add Review', 
                               course_code=course_code,
                               cid = cid,
                               departments=departments)

@app.route('/profile/')
def profile():
    uid = session.get('uid')
    email = session.get('email')
    name = session.get('name')

    # info_review = db.get_reviews_by_uid(uid)
    info_review = db.get_profile_reviews(uid)
    # print(info_review)
    if len(info_review) == 0:
        flash('No reviews found for this course.')
    
    global departments 
    if departments is None:
        departments = db.get_departments()

    return render_template('profile.html', page_title='Profile', 
                                           uid=uid, 
                                           email=email, 
                                           name=name,
                                           reviews=info_review,
                                           departments=departments)


if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()

    app.debug = True
    app.run('0.0.0.0',port)
