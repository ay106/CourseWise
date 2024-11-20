import cs304dbi as dbi

def get_departments(conn):
    curs = dbi.dict_cursor(conn)
    curs.execute('''select name from department''')
    return curs.fetchall()

def get_department_id(conn, department_name):
    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT did FROM department WHERE name = %s''', [department_name])
    dept = curs.fetchone()
    return dept['did'] if dept else None

def get_course_by_code(conn, course_code):
     curs = dbi.dict_cursor(conn)
     curs.execute('''SELECT * FROM course WHERE course_code = %s''', [course_code])
     return curs.fetchone()

def get_courses_by_department(conn, department):
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
    curs = dbi.dict_cursor(conn)
    sql_reviews = '''SELECT review.*, u.name AS user_name
                        FROM review
                        INNER JOIN course c ON review.course_id = c.cid
                        INNER JOIN user u ON review.user_id = u.uid
                        WHERE review.course_id = %s'''
    curs.execute(sql_reviews, [cid])
    return curs.fetchall()

def get_course_info_by_cid(conn, cid):
    curs = dbi.dict_cursor(conn)
    sql_course = ('''select c.cid, c.did, c.course_code, c.name from course c 
                where cid = %s''')
    curs.execute(sql_course, [cid])
    return curs.fetchone()

def insert_professor(conn, prof_name, dept_id):
    curs = dbi.dict_cursor(conn)
    curs.execute('''insert into professor(name, department_id) 
                         values (%s, %s)''',[prof_name, dept_id])
    conn.commit()

def get_prof_by_name(conn, prof_name):
    curs = dbi.dict_cursor(conn)
    curs.execute('''select * from professor where name=%s''',[prof_name])
    return curs.fetchone()

def insert_review(conn, cid, user_id, prof_name, prof_rating, prof_id, difficulty, credit, sem, year, take_again, load_heavy, office_hours, helped_learn, stim_interest, description):
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

def insert_course(conn, course_code, course_name, dept_id):
    curs = dbi.dict_cursor(conn)
    curs.execute("""
        INSERT INTO course (course_code, name, did)
        VALUES (%s, %s, %s)
    """, [course_code, course_name, dept_id])
    conn.commit()

def get_reviews_by_uid(conn, uid):
    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT *
                    FROM review r
                    INNER JOIN user u ON r.user_id = u.uid
                    WHERE r.user_id=%s''', [uid])
    return curs.fetchall()

def get_profile_reviews(conn, uid):
    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT *
                    FROM review r
                    INNER JOIN course c on r.course_id = c.cid
                    INNER JOIN user u ON r.user_id = u.uid
                    WHERE r.user_id=%s''', [uid])
    return curs.fetchall()