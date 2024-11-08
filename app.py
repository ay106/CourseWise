from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)


import cs304dbi as dbi

import secrets

app.secret_key = secrets.token_hex()

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def home():
    # hardcode user values since draft version does not have sign-up/login functionality
    session['uid'] = 1
    session['email'] = 'jc103@wellesley.edu'
    session['name'] = 'Vaishu Chintam'
    return render_template('main.html', page_title='Home')

@app.route('/department/')
def select_department():
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    department = request.args.get('department')

    if department == "All Department":
        # get all courses
        curs.execute('''select cid, course_code, name from course order by course_code''')
    else:
        curs.execute('''select cid, course_code, course.name as name
                     from course inner join department using (did) 
                     where department.name = %s
                     order by course_code''',
                     [department])
    data = curs.fetchall()

    if len(data) == 0:
        # let user know that no matches were found 
        flash('No courses found for this department.')

    return render_template('department_courses.html', 
                           page_title='Department Courses', 
                           data = data, 
                           department = department)

@app.route('/courses/<cid>')
def display_course(cid):
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    sql_reviews = '''SELECT review.*, u.name AS user_name
                        FROM review
                        INNER JOIN course c ON review.course_id = c.cid
                        INNER JOIN user u ON review.user_id = u.uid
                        WHERE review.course_id = %s'''
    curs.execute(sql_reviews, cid)
    info_review = curs.fetchall()

    ## below will capture course_code and name from cid
    sql_course = ('''select c.cid, c.course_code, c.name from course c 
                where cid = %s''')
    curs.execute(sql_course, cid)
    info_course = curs.fetchone()

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
                               length = len(info_review))

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

        conn = dbi.connect()
        curs = dbi.dict_cursor(conn)

        # insert professor into professor table if prof_name not already in the table
        curs.execute('''select * from professor where name=%s''',[prof_name])
        prof_data = curs.fetchone()
        if not prof_data:
            # get department id for the course
            cid_int = int(cid)
            curs.execute('''select did from course where cid=%s''', [cid_int])
            course = curs.fetchone()
            dept_id = course['did']

            curs.execute('''insert into professor(name, department_id) 
                         values (%s, %s)''',[prof_name, dept_id])
            conn.commit()

        # get professor id 
        curs.execute('''select pid from professor where name=%s''',[prof_name])
        prof = curs.fetchone()
        prof_id = prof['pid']

        # insert review
        curs.execute('''
            insert into review (course_id, user_id, prof_name, prof_rating, prof_id,
                                difficulty, credit, sem, year, take_again, 
                                load_heavy, office_hours, helped_learn, 
                                stim_interest, description, last_updated)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            ''', (cid, user_id, prof_name, prof_rating, prof_id, difficulty, credit,
                  sem, year, take_again, load_heavy, office_hours, 
                  helped_learn, stim_interest, description))
        conn.commit()

        flash("Review added successfully!")
        return redirect(url_for('display_course', cid=cid))
    else:
        return render_template('add_review.html', 
                               page_title='Add Review', 
                               course_code=course_code,
                               cid = cid)

@app.route('/profile/')
def profile():
    session['uid'] = 1
    session['email'] = 'jc103@wellesley.edu'
    session['name'] = 'Vaishu Chintam'

    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT *
                    FROM review r
                    INNER JOIN course c on r.course_id = c.cid
                    INNER JOIN user u ON r.user_id = u.uid
                    WHERE r.user_id=%s''', [session['uid']])
    info_review = curs.fetchall()

    if len(info_review) == 0:
        flash('No reviews found for this course.')

    return render_template('profile.html', page_title='Profile', 
                                           uid=session['uid'], 
                                           email=session['email'], 
                                           name=session['name'],
                                           reviews=info_review)


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
