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
        flash('No courses found for this department.') # let user know that no matches were found 

    return render_template('department_courses.html', page_title='Department Courses', data = data, department = department)

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

    if len(info_review) == 0:
        flash('No reviews found for this course.')

    else:
        ## below will capture course_code and name from cid
        sql_course = ('''select c.course_code, c.name from course c 
                    where cid = %s''')
        curs.execute(sql_course, cid)
        info_course = curs.fetchone()
        return render_template('course_reviews.html', 
                               page_title='Course Reviews',
                               reviews = info_review,
                               course = info_course,
                               length = len(info_review))

@app.route('/profile/')
def profile():
    return render_template('profile.html', page_title='Profile')


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
