import cs304dbi as dbi

dbi.conf('cwise_db')

def get_departments():
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute('''select name from department''')
    return curs.fetchall()

def get_courses_by_department(department):
    conn = dbi.connect()
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

def get_course_reviews(cid):
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    sql_reviews = '''SELECT review.*, u.name AS user_name
                        FROM review
                        INNER JOIN course c ON review.course_id = c.cid
                        INNER JOIN user u ON review.user_id = u.uid
                        WHERE review.course_id = %s'''
    curs.execute(sql_reviews, [cid])
    return curs.fetchall()

def get_course_info_by_cid(cid):
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    sql_course = ('''select c.cid, c.did, c.course_code, c.name from course c 
                where cid = %s''')
    curs.execute(sql_course, [cid])
    return curs.fetchone()

def insert_professor(prof_name, dept_id):
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute('''insert into professor(name, department_id) 
                         values (%s, %s)''',[prof_name, dept_id])
    conn.commit()

def get_prof_by_name(prof_name):
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute('''select * from professor where name=%s''',[prof_name])
    return curs.fetchone()

def insert_review(cid, user_id, prof_name, prof_rating, prof_id, difficulty, credit, sem, year, take_again, load_heavy, office_hours, helped_learn, stim_interest, description):
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
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

def get_reviews_by_uid(uid):
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT *
                    FROM review r
                    INNER JOIN user u ON r.user_id = u.uid
                    WHERE r.user_id=%s''', [uid])
    return curs.fetchall()