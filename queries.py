import cs304dbi as dbi


def get_departments(conn):
    '''
    Gets all department names from department table.

    param conn: database connection

    return: a list of dictionaries containing department names
    '''    
    curs = dbi.dict_cursor(conn)
    curs.execute('''select name from department''')
    return curs.fetchall()


def get_department_id(conn, department_name):
    '''
    Gets department id for the given department name

    param conn: database connection
    param department_name: name of department

    return: the department id or None if the department does not exist 
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT did FROM department WHERE name = %s''', 
                 [department_name])
    dept = curs.fetchone()
    return dept['did'] if dept else None


def get_course_by_course_code(conn, course_code):
    '''
    Gets course data from the course table for the provided course code.

    param conn: database connection
    param course_code: the course code

    return: a dictionary containing the course data
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''select * from course where course_code = %s''', 
                 [course_code])
    return curs.fetchone()

def get_courses_by_department(conn, department):
    '''
    Gets all courses belonging to the given department. 

    param conn: database connection
    param department: the name of the department

    return: a list of dictionaries containing course data for each course
        under the department 
    '''    
    curs = dbi.dict_cursor(conn)
    if department == "All Department":
        # get all courses
        curs.execute('''select cid, course_code, name from course order by course_code''')
    else:
        curs.execute('''select cid, course_code, course.name as name
                     from course inner join department using (did) 
                     where department.name = %s
                     order by course_code''',
                     [department])
    return curs.fetchall()


def get_course_reviews(conn, cid):
    '''
    Gets all reviews for the given course.

    param conn: databse connection
    param cid: course id

    return: list of dictionaries containing review data for each review
    '''
    curs = dbi.dict_cursor(conn)
    sql_reviews = '''SELECT review.*, u.name AS user_name
                        FROM review
                        INNER JOIN course c ON review.course_id = c.cid
                        INNER JOIN user u ON review.user_id = u.uid
                        WHERE review.course_id = %s'''
    curs.execute(sql_reviews, [cid])
    return curs.fetchall()


def get_course_info_by_cid(conn, cid):
    '''
    Gets course info for the given course id.

    param conn: database connection
    param cid: course id 

    return: a dictionary holding course data
    '''
    curs = dbi.dict_cursor(conn)
    sql_course = ('''select c.cid, c.did, c.course_code, c.name from course c 
                where cid = %s''')
    curs.execute(sql_course, [cid])
    return curs.fetchone()


def insert_professor(conn, prof_name, dept_id):
    '''
    Inserts a new professor into the professor table

    param conn: database connection
    param prof_name: name of professor
    param dept_id: the id of the department the professor belongs to
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''insert into professor(name, department_id) 
                         values (%s, %s)''',[prof_name, dept_id])
    conn.commit()


def get_prof_by_name(conn, prof_name):
    '''
    Gets all data for the given professor. 

    param conn: database connection
    param prof_name: the professor's name

    return: a dictionary holding the professor's data from the professor table
    '''    
    curs = dbi.dict_cursor(conn)
    curs.execute('''select pid, name, department_id from professor where name=%s''',
                 [prof_name])
    return curs.fetchone()


def insert_review(conn, review_data):
    '''
    Inserts a new review into the review table.

    param conn: database connection
    param review_data: dictionary holding the review data 
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
            insert into review (course_id, user_id, prof_name, prof_rating, prof_id,
                                difficulty, credit, sem, year, take_again, 
                                load_heavy, office_hours, helped_learn, 
                                stim_interest, description, last_updated)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            ''', (review_data['cid'], review_data['user_id'], review_data['prof_name'], 
                  review_data['prof_rating'], review_data['prof_id'], review_data['difficulty'], 
                  review_data['credit'], review_data['sem'], review_data['year'], 
                  review_data['take_again'], review_data['load_heavy'], review_data['office_hours'], 
                  review_data['helped_learn'], review_data['stim_interest'], 
                  review_data['description']))
    conn.commit()


def insert_course(conn, course_code, course_name, dept_id):
    '''
    Inserts a new course to the course table.

    param conn: database connection
    param course_code: the course code
    param course_name: the course name
    param dept_id: the department id for the department the course belongs to
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute("""
        INSERT INTO course (course_code, name, did)
        VALUES (%s, %s, %s)
    """, [course_code, course_name, dept_id])
    conn.commit()


def get_profile_reviews(conn, uid):
    '''
    Gets all reviews written by the user. 

    param conn: database connection
    param uid: user id 

    return: a list of dictionaries containing review data for each review the user 
    submitted
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT *
                    FROM review r
                    INNER JOIN course c on r.course_id = c.cid
                    INNER JOIN user u ON r.user_id = u.uid
                    WHERE r.user_id=%s''', [uid])
    return curs.fetchall()


def get_review_by_id(conn, rid):
    '''
    Gets the data for the given review id.

    param conn: database connection
    param rid: review id

    return: a dictionary holding the review data
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''select rid, course_id, user_id, difficulty, credit, 
                 prof_name, prof_id, prof_rating, sem, year, take_again, 
                 load_heavy, office_hours, helped_learn, stim_interest, description, 
                 last_updated from review
                 where rid = %s''', 
                 [rid])
    return curs.fetchone()


def update_review(conn, updated_data):
    '''
    Updates the review with the given review id.

    param conn: database connection
    param updated_data: dictionary containing updated review data
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''update review set 
                 prof_name = %s,
                 prof_rating = %s,
                 difficulty = %s,
                 credit = %s,
                 sem = %s,
                 year = %s,
                 take_again = %s,
                 load_heavy = %s,
                 office_hours = %s,
                 helped_learn = %s,
                 stim_interest = %s,
                 description = %s
                 where rid = %s''', 
                 [updated_data['prof_name'], updated_data['prof_rating'], 
                  updated_data['difficulty'], updated_data['credit'], 
                  updated_data['sem'], updated_data['year'], updated_data['take_again'], 
                  updated_data['load_heavy'], updated_data['office_hours'], 
                  updated_data['helped_learn'], updated_data['stim_interest'], 
                  updated_data['description'], updated_data['rid']])

    conn.commit()


def delete_review(conn, rid):
    '''
    Deletes the review with the given review id.

    param conn: database connection
    param rid: review id
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''delete from review where rid = %s''', 
                 [rid])
    conn.commit()

def upload_pic(conn, uid, filename):
    '''
    Insert uid and picture file name into picfile table.

    param conn: database connection
    param uid: user id
    param filename: picture file name
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute(
        '''insert into picfile(uid,filename) values (%s,%s)
            on duplicate key update filename = %s''',
        [uid, filename, filename])
    conn.commit()