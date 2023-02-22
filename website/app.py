from flask import Flask, render_template, request, redirect, url_for, flash, Response, make_response, json
from Psycopg2_functions import *
from Web_projects import geocode
from Web_projects import getgroup
from dashapp import create_dash_app
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/", methods=['GET', 'POST'])
def Home():
    return render_template('home.html')

@app.route("/help")
def help():
    return "<h1>GNU</h1>"
@app.route("/dash")
def dashh():
    dash_app = create_dash_app(app)
    dash_app_html = dash_app.index()
    return render_template("dashapp.html", dash_app=dash_app_html)

@app.route("/projects")
def projects():
    return render_template('projects.html', posts=list_posts(pgconnect()))
@app.route("/links")
def links():
    return render_template('links.html', posts=list_posts(pgconnect()))

@app.route("/blog", methods=['GET','POST'])
def blog():
    return render_template('blog.html', posts=list_posts(pgconnect()), post_comments=list_post_comments(pgconnect()))


@app.route("/add_new_post", methods=['GET','POST'])
def add_new_post():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        author = request.form.get("author")
        title = request.form.get("title")
        email = request.form.get("email")
        content = request.form.get("content")
        post_status = add_post(author,title, content, email, pgconnect())
        if post_status == "uniqueerror":
            flash("danger")
        elif post_status == "success":
            flash("success")

    return redirect(url_for("blog"))


@app.route("/add_new_comment", methods=['GET','POST'])
def add_new_comment():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        author = request.form.get("author")
        email = request.form.get("email")
        content = request.form.get("comment_content")
        print("Added comment")
        post_id = request.form.get("post_id")
        print("Added comment")
        add_comment(post_id, author, content, email, pgconnect())

        return redirect(url_for("blog"))
    
    


@app.route("/delete", methods=['GET','POST'])
def delete_post():
    title = request.args.get("title")
    post_status = psdelete_post(title, pgconnect())
    if post_status == "danger":
        flash("deletedanger")
    elif post_status == "success":
        flash("deletesuccess")
    return redirect(url_for("blog"))


@app.route("/edit", methods=['GET','POST'])
def edit_post():
    if request.method == 'GET':
        title = request.args.get("title")

        return redirect(f'{url_for("blog")}#{title}')
    elif request.method == 'POST':
        return redirect(f'{url_for("blog")}')


@app.route('/teamscramble', methods=['GET','POST'])
def teamscramble():
    return render_template('teamscramble.html')


@app.route("/calculate_groups", methods=['GET','POST'])
def calculate_groups():
    if request.method == 'POST':
        groupstring = request.form.get("people")
        groupnumber = int(request.form.get("groupnumber"))
        groups = getgroup.getgroups(groupstring,groupnumber)
        return render_template('teamscramble.html', groups=groups)


# Here follow temperature data items.
@app.route("/temperature", methods=['GET','POST'])
def temperature():
    return render_template('temperature.html')


@app.route("/get_temperature", methods=['GET','POST'])
def get_temperature():
    if request.method == 'POST':
        location = request.form.get("location")
        x = geocode.getlocation(location)
        
        
        temperatures, timestamps,station_name = list_temps(*x)
        print('\n', temperatures, '\n', timestamps,'\n')
        return render_template('temperature.html', temperatures = temperatures, timestamps = timestamps, station_name = station_name)
    else:
        return render_template('temperature.html')


@app.route("/workout", methods=["GET","POST"])
def workout():
    if request.method == 'POST':
        return render_template("workout.html")
    elif request.method =='GET':
        selected_exercise = request.args.get("exercise")
        selexname = selected_exercise
        if selected_exercise: selected_exercise = select_single_exercise(selected_exercise)
        return render_template('workout.html', exercise_name=selexname, selected_exercise=selected_exercise, exercises=select_exercises(),workouts=select_workouts(), sessions = list_sessions())

@app.route("/add_workout",methods=["GET","POST"])
def add_workout():
    if request.method == "POST":
        weights = request.form.getlist("weight")
        reps = request.form.getlist("reps")
        exercises = request.form.getlist("exercise")
        sets = request.form.getlist("sets")
        workout=[]
        for i in range(len(weights)):
            exercise = {
        "exercise_name": f"{exercises[i]}",
        "repetitions": reps[i],
        "sets": sets[i],
        "weight": weights[i]
    }
            workout.append(exercise)
        print(workout)
        psadd_workout(workout)
        return redirect(url_for('workout'))
    elif request.method =="GET":
        name=request.args.get("name")
        exercises = get_session(name)
        return render_template("workout.html",sessionexercises=exercises,  sessions = list_sessions(), name=name)


@app.route("/add_session", methods=["POST","GET"])
def add_session():
    if request.method =="POST":
        session_name = request.form.get("session_name")
        exercise_list = request.form.getlist("exercise")
        if not session_name or not exercise_list: return render_template("workout.html")
        psadd_session(session_name,exercise_list)
        return redirect(url_for("workout"))
    elif request.method =="GET":
        return render_template("workout.html", exercises =select_exercises(), sessions = list_sessions(), add_session=True)

@app.route("/add_exercise", methods=["POST"])
def add_exercise():
    if request.method=="POST":
            exercise = request.form.get("addexercise")
            print(exercise)
            pgadd_exercise(exercise)
    return redirect(url_for("add_session"))

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if len(username)>3 or len(password)>3:
            try:
                mylogin = pglogin(username,password)
                resp = make_response(redirect(url_for('Home')))
                print(mylogin[0],mylogin[1])
                resp.set_cookie('userID', str(mylogin[0]))
                resp.set_cookie('username', mylogin[1])
                flash('success')
                return resp
            except:
                flash('danger')
                return redirect(url_for('login'))
        else:
            flash('Username and password need to be more than 3 characters.')
    elif request.method=="GET":
        if not request.cookies.get("userID"):
            return render_template("login.html")
        else:
            return redirect(url_for('Home'))


@app.route("/register", methods=["POST","GET"])
def register():
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        success_status = pgregister(username,password)
        return render_template("login.html")
    elif request.method=="GET":
        
        return redirect(url_for('Home'))


@app.route("/logout", methods=["POST","GET"])
def logout():
    if request.method=="POST":
        resp = make_response(render_template("home.html"))
        resp.set_cookie('userID', '', expires=0)
        return resp
    elif request.method == "GET":
        resp = make_response(render_template("home.html"))
        resp.set_cookie('userID', '', expires=0)
        resp.set_cookie('username','', expires=0)
        return resp


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
