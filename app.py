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
    return render_template('department_courses.html', page_title='Department Courses')

@app.route('/course/<course_code>')
def display_course(course_code):
    return render_template('course_reviews.html', page_title='Course Reviews')

@app.route('/profile/')
def display_course():
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
