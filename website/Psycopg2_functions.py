from flask import request
import psycopg2
import datetime
import pandas as pd

password = "Kj&hL8+#Sj*f@g1mz"
database = "website_database"
host = "db"
port = 5432
user = "postgres"
conn = False
delete_index = 'name'


def pgconnect(database=database,port=port,host=host,user=user,password=password):
    conn = psycopg2.connect(database=database, port=port, host=host, user=user, password=password)
    return conn

def disconnect(conn=pgconnect()):
    "Disconnects from database"
    conn.close()
    return True

def list_posts(conn=pgconnect()):
    posts=[]
    cur=conn.cursor()
    cur.execute("""
    SELECT id,author, title, content, DATE_TRUNC('minute', date_posted) from blog_posts
    ORDER BY date_posted DESC;
    """)
    post_list = cur.fetchall()
    for post in post_list:
        postdict = dict()
        postdict["id"] = post[0]
        postdict["author"] = post[1]
        postdict["title"]  = post[2]
        postdict["content"] = post[3]
        postdict["date_posted"] = str(post[4])[:-3]
        cur.execute(f"""
        SELECT COUNT(bp.id) FROM blog_posts bp
        JOIN blog_post_comments bpc ON bp.id = bpc.post_id
        WHERE bp.id = {post[0]};
        """)
        comment_count = cur.fetchall()
        postdict["comment_count"] = comment_count[0]

        posts.append(postdict)
        
    cur.close()
    conn.close()
    return posts

def list_post_comments(conn=pgconnect()):
    posts=[]
    cur=conn.cursor()
    cur.execute("""
    SELECT id, post_id,author, content, DATE_TRUNC('minute', date_posted) from blog_post_comments
    ORDER BY date_posted DESC;
    """)
    post_list = cur.fetchall()
    for post in post_list:
        postdict = dict()
        postdict["id"] = post[0]
        postdict["post_id"] = post[1]
        postdict["author"] = post[2]
        postdict["content"] = post[3]
        postdict["date_posted"] = str(post[4])[:-3]
        posts.append(postdict)
    cur.close()
    conn.close()
    return posts

def getdate():
    now = datetime.datetime.now().date()
    return now

def format_content(content, method = "IN"):
    newcontent = content.replace('\n', '<br>')
    return newcontent

def add_post(author, title, content, email, conn=pgconnect()):
    try:
        cur = conn.cursor()
        content=format_content(content)
        cur.execute(f"""
        INSERT INTO blog_posts (author, title, content, date_posted, email) VALUES
        ($${author}$$, $${title}$$, $${content}$$, '{getdate()}', $${email}$$);
        """)
        cur.execute("COMMIT;")
        cur.close()
        conn.close()
        return "success"
    except:
        return "uniqueerror"


def add_comment(post_id, author, content, email, conn=pgconnect()):
    cur = conn.cursor()
    cur.execute(f"""
    INSERT INTO blog_post_comments (post_id, author, content, date_posted, email) VALUES
    ({post_id}, $${author}$$, $${content}$$, '{getdate()}', $${email}$$);
    """)
    cur.execute("COMMIT;")
    cur.close()
    conn.close()


def psdelete_post(title,conn=pgconnect()):
    try:
        cur = conn.cursor()
        print(f"function psdelete_post running on {title}")
        cur.execute(f"""
    DELETE FROM blog_posts
    WHERE title = $${title}$$;
    """)
        cur.execute("COMMIT;")
        cur.close()
        conn.close()
        return "success"
    except:
        return "danger"
    

def get_count(table, conn=pgconnect()):
    cur = conn.cursor()
    cur.execute(f"""
SELECT COUNT(id) FROM {table};
""")
    count=cur.fetchone()
    cur.close()
    conn.close()
    return count


def list_temps(lat,lon):
    conn= pgconnect()
    cursor = conn.cursor()
    query = f"""SELECT s.station_id From Station s Join
    Temperature t On t.Station_Id = s.Station_Id
    Where t.Quality = 'G'
    order by abs((s.longitude-{lon})*(s.longitude-{lon})+ (s.latitude-{lat})*(s.latitude-{lat})) ASC limit 1;"""
    cursor.execute(query)
    station_id = cursor.fetchone()[0]
    query = f"""SELECT s.Station_Name, t.Value, t.Timestamp From Station s Join
    Temperature t On t.Station_Id = s.Station_Id
    where s.station_id = {station_id}
    Order By t.Timestamp Desc"""
    cursor.execute(query)
    Templist = cursor.fetchall()
    xyList = Templist
    temperatures = [row[1] for row in xyList]
    timestamps = [row[2] for row in xyList]
    print(xyList)
    timestamps = timestamps[::-1]
    print(timestamps)
    for i in range(len(timestamps)):
        print(timestamps[i])
        timestamps[i] = datetime.datetime.fromtimestamp(int(timestamps[i])/1000).strftime('%Y-%m-%d %H')
    station_name = xyList[0][0]
    return temperatures,timestamps,station_name


def add_exercise(exercise):
    conn=pgconnect()
    cursor = conn.cursor()
    query = f"""INSERT INTO exercise (exercise_name) VALUES
    ('{exercise}');

    """
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()


def psadd_workout(workout):
    """This will take in a list of dictionaries with the values exercise name,
    repetitions and sets and weight.
    Format:
    item = {
        "exercise_name": "squats",
        "repetitions": 8,
        "sets": 1,
        "weight": 150
    }

    """
    query1 = f"""
    INSERT INTO workout (workout_date)
    VALUES ('{getdate()}');"""
    query2 = """
    SELECT workout_id from workout
    ORDER BY workout_id DESC LIMIT 1;
    """
    conn = pgconnect()
    cursor = conn.cursor()
    cursor.execute(query1)
    conn.commit()
    cursor.execute(query2)
    workout_id = cursor.fetchone()[0]
    for item in workout:
        query3 = f"""
        SELECT exercise_id from exercise where exercise_name = '{item["exercise_name"]}';"""
        cursor.execute(query3)
        exercise_id = cursor.fetchone()[0]
        query3 = f"""
        INSERT INTO workoutexercises (workout_id, exercise_id, repetitions, sets, weight)
        VALUES 
        ('{workout_id}', '{exercise_id}', '{item["repetitions"]}', '{item["sets"]}', '{item["weight"]}');
        
        """
        cursor.execute(query3)
    conn.commit()
    cursor.close()
    conn.close()
    return True
    

def pgadd_exercise(exercise_name):
    conn=pgconnect()
    cursor = conn.cursor()
    query = f"""
    Insert into exercise (exercise_name) VALUES
    ('{exercise_name}')
    """
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
    return "Success"


def select_exercises():
    conn=pgconnect()
    cursor=conn.cursor()
    query=f"""
    SELECT exercise_name from exercise;"""
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result



def select_single_exercise(exercise):
    conn=pgconnect()
    cursor=conn.cursor()
    query=f"""
    SELECT we.sets, we.repetitions, we.weight, wo.workout_date from exercise e
    JOIN workoutexercises we on we.exercise_id = e.exercise_id
    JOIN workout wo ON we.workout_id = wo.workout_id
     where e.exercise_name = '{exercise}'
     ORDER BY wo.workout_date DESC;"""
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def list_sessions():

    query = f"""
    SELECT name from session_name;
    """
    conn=pgconnect()
    cursor = conn.cursor()
    cursor.execute(query)   
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def get_session(session_name):
    query=f"""
    SELECT e.exercise_id, e.exercise_name from exercise e
    JOIN session s on s.exercise_id = e.exercise_id
    JOIN session_name sn ON sn.session_id = s.session_id
    WHERE sn.name = '{session_name}';
    """

    conn=pgconnect()
    cursor = conn.cursor()
    cursor.execute(query)
    exercises = cursor.fetchall()
    exercise_list = list()
    for item in exercises:
        exercise_list.append(item[1])
    exercise_tuple = tuple(exercise_list)
    print(exercises, '\n\n\n', exercise_tuple)
    query2 = f"""
    with sub as 
    (SELECT e.exercise_id, e.exercise_name, we.repetitions, we.weight, 
    we.weight * (1 + 0.0333 * we.repetitions ) AS onerm from workoutexercises we
    join exercise e on e.exercise_id = we.exercise_id),
sub2 as 
(select sub.exercise_name, max(sub.onerm) from sub group by exercise_name),
sub3 as
(SELECT s.id,s.exercise_id, e.exercise_name from exercise e
    JOIN session s on s.exercise_id = e.exercise_id
    JOIN session_name sn ON sn.session_id = s.session_id
    WHERE sn.name = '{session_name}')

SELECT sub3.exercise_name, sub.repetitions, sub.weight from exercise e
JOIN sub2 ON sub2.exercise_name = e.exercise_name 
left JOIN sub on sub2.max = sub.onerm AND sub2.exercise_name = sub.exercise_name
JOIN sub3 ON sub3. exercise_id = e.exercise_id 
WHERE e.exercise_name IN {exercise_tuple}
order by sub3.id;"""

    cursor.execute(query2)
    bestworkout = cursor.fetchall()
    print(bestworkout)
    cursor.close()
    conn.close()
    if any(bestworkout):
        df = pd.DataFrame(bestworkout)
        for item in exercise_tuple:
            if item not in df.iloc[:,0].values:
                bestworkout.append((item,0,0))
    else:
        for item in exercise_tuple:
            bestworkout.append((item,0,0))
    return (bestworkout)


def select_workouts():
    """item = {
        "exercise_name": "squats",
        "repetitions": 8,
        "sets": 1,
        "weight": 150
    }"""
    conn = pgconnect()
    cursor = conn.cursor()
    query = f"""
    SELECT e.exercise_name,we.sets, we.repetitions,we.weight,w.workout_date,w.workout_id FROM workout w JOIN
    workoutexercises we ON we.workout_id = w.workout_id JOIN
    exercise e on e.exercise_id = we.exercise_id 
    ORDER BY
    w.workout_id;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    if not result: result = ('Deadlift', 0, 0, 0, 0)
    cursor.close()
    conn.close()
    return result


def psadd_session(session_name, exercises):
    conn=pgconnect()
    cur = conn.cursor()
    cur.execute(f"""
    Insert into session_name (name) Values
    ('{session_name}');
    """)
    cur.execute("COMMIT;")
    cur.execute(f"""
    SELECT session_id from session_name ORDER BY session_id desc limit 1;""")
    session_id = cur.fetchone()[0]
    for item in exercises:
        cur.execute(f"SELECT exercise_id from exercise where exercise_name='{item}';")
        ex_id = cur.fetchone()[0]
        cur.execute(f"""
        Insert into session (session_id, exercise_id) Values
        ({session_id},{ex_id})
        """)
        conn.commit()
    cur.close()
    conn.close()
    return "success"
    


def pgregister(username, password):
    now = datetime.datetime.now()
    conn=pgconnect()
    cur = conn.cursor()
    cur.execute(f"""
    INSERT INTO login (username, password, register_date) VALUES
    ('{username}', '{password}', '{now}');
    """)
    conn.commit()
    cur.close()
    conn.close()
    return "Success"

def pglogin(username,password):
    print(username,password)
    conn=pgconnect()
    cur=conn.cursor()
    cur.execute(f"""
    select username, password, userid from login
    where username = '{username}' and password = '{password}';
    
    """)
    logininfo = cur.fetchall()
    print(logininfo)
    cur.close()
    conn.close()
    if any(logininfo):
        return logininfo[0][2],logininfo[0][0]

def cookiecheck(userID,username):
    conn = pgconnect()
    cur = conn.cursor()
    cur.execute(f"""
    select username from login where userID = {userID};
    """)
    
    if any(cur.fetchall()):
        return True
    else: return False


if __name__ == '__main__':
    print(select_workouts())
