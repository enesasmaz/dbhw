from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

def create_app():
    app = Flask(__name__)

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '15963214'
    app.config['MYSQL_DB'] = 'calendar'
    app.config['MYSQL_CURSORCLASS'] = "DictCursor"

    mysql = MySQL(app)
    app.config.from_object("settings")
    
    @app.route('/')
    def home_page():
        return render_template("home.html")

    @app.route('/s_sign', methods=['GET', 'POST'])
    def s_sign_page():
        return render_template('s_sign.html')
    
    @app.route('/t_sign')
    def t_sign_page():
        return render_template('t_sign.html')

    @app.route('/c_sign')
    def c_sign_page():
        return render_template('c_sign.html')

    @app.route('/s_calendar', methods=['GET', 'POST'])
    def s_calendar():
        if 's_id'  in request.args:
            s_id = request.args.get('s_id')
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT calendar_id FROM calendar WHERE s_id=%s",(s_id))
            calid = cursor.fetchone()
            mysql.connection.commit()
            cursor.execute("SELECT * FROM calendar_days WHERE calendar_id=%s", ([calid['calendar_id']]))
            caldays=cursor.fetchall()
            return render_template('s_calendar.html',s_id=s_id, caldays=caldays)
        else:    
            return render_template('s_calendar.html')

    @app.route('/s_login', methods=['GET', 'POST'])
    def s_login():
        return render_template('s_login.html')

    @app.route('/t_login', methods=['GET', 'POST'])
    def t_login():
        return render_template('t_login.html')

    @app.route('/c_login', methods=['GET', 'POST'])
    def c_login():
        return render_template('c_login.html')    

    @app.route('/day/<int:s_id>/<int:day_id>', methods=["GET","POST"])
    def day(s_id, day_id):
        return render_template('day1.html', s_id=s_id, day_id=day_id)    

    @app.route('/aftersign_s', methods=["GET","POST"])
    def s_aftersign_page():
        if request.method == "POST":

            site_studentid = request.form.get('s_id')
            site_studentname = request.form.get('s_name')
            site_password = request.form.get('s_password')
            site_studentmail = request.form.get('s_mail')

            cursor = mysql.connection.cursor()

            q = "INSERT INTO student VALUES (%s, %s, %s, %s)"
            v = (site_studentid, site_studentname, site_password, site_studentmail)
            cursor.execute(q,v)
            
            q1 = "INSERT INTO calendar VALUES(%s, %s)"
            v1 = (None,site_studentid)
            cursor.execute(q1,v1)

            mysql.connection.commit()

            index = cursor.lastrowid

            for i in range(1,32):
                q_dates = "INSERT INTO calendar_days VALUES (%s, %s, %s, %s)"
                cursor.execute(q_dates,(index, i, None, None))

            mysql.connection.commit()
            cursor.close()
        return render_template('s_login.html')

    @app.route('/days/<int:s_id>/<int:day_id>', methods=["GET","POST"])
    def afterday(s_id, day_id):
        if request.method == "POST":
            event1 = request.form.get('events')
            time1 = request.form.get('time')
            cursor = mysql.connection.cursor()

            cursor.execute("SELECT * FROM calendar WHERE s_id=%s", (s_id,))

            index = cursor.fetchone()

            index=index['calendar_id']

            cursor.execute("SELECT * FROM calendar_days WHERE calendar_id=%s", ([index]))
            caldays=cursor.fetchall()

            q1 = "UPDATE calendar_days SET events=%s, time=%s WHERE calendar_id=%s AND day_id=%s"
            cursor.execute(q1,(event1, time1, index, day_id))
            mysql.connection.commit()
            cursor.close()
        return redirect(url_for('s_calendar', s_id=s_id, caldays=caldays))

    @app.route('/aftersign_t', methods=["GET","POST"])
    def t_aftersign_page():
        if request.method == "POST":

            site_teacherid = request.form.get('t_id')
            site_teachername = request.form.get('t_name')
            site_password = request.form.get('t_password')
            site_teachermail = request.form.get('t_mail')

            cursor = mysql.connection.cursor()

            q = "INSERT INTO teacher(calendar_id, t_id, t_name, t_password, t_mail) VALUES (%s, %s, %s, %s, %s)"

            cursor.execute(q,(1, site_teacherid, site_teachername, site_password, site_teachermail))
            mysql.connection.commit()
            cursor.close()
        return render_template('home.html')

    @app.route('/aftersign_c', methods=['POST'])
    def c_aftersign_page():
        if request.method == "POST":

            site_clubpid = request.form.get('c_id')
            site_clubpname = request.form.get('c_name')
            site_password = request.form.get('c_password')
            site_clubpmail = request.form.get('c_mail')

            cursor = mysql.connection.cursor()

            q = "INSERT INTO student_club_person(calendar_id, c_id, c_name, c_password, c_mail) VALUES (%s, %s, %s, %s, %s)"

            cursor.execute(q,(1, site_clubpid, site_clubpname, site_password, site_clubpmail))
            mysql.connection.commit()
            cursor.close()
        return render_template('home.html')

    @app.route('/afterlogin_s', methods=['GET', 'POST'])
    def s_afterlogin():
        if request.method == "POST" and 's_mail' in request.form and 's_password' in request.form:
            
            s_loginmail = request.form.get('s_mail')
            s_loginpassword = request.form.get('s_password')
            
            cursor = mysql.connection.cursor()
            
            cursor.execute("SELECT* FROM student WHERE s_mail = %s AND s_password = %s", (s_loginmail, s_loginpassword,))
            account = cursor.fetchone()
            mysql.connection.commit()
            cursor.execute("SELECT calendar_id FROM calendar WHERE s_id=%s",([account['s_id']]))
            calid = cursor.fetchone()
            mysql.connection.commit()
            cursor.execute("SELECT * FROM calendar_days WHERE calendar_id=%s", ([calid['calendar_id']]))
            caldays=cursor.fetchall()

            if account:
                s_loginmail= account['s_mail']
                s_loginpassword= account['s_password']
                return render_template('s_calendar.html', s_id=account['s_id'], caldays=caldays)
        return render_template('home.html')
    
    @app.route('/afterlogin_t', methods=['GET', 'POST'])
    def t_afterlogin():
        if request.method == "POST" and 't_mail' in request.form and 't_password' in request.form:
            
            t_loginmail = request.form.get('t_mail')
            t_loginpassword = request.form.get('t_password')
            
            cursor = mysql.connection.cursor()
            
            check = cursor.execute("SELECT* FROM teacher WHERE t_mail = %s AND t_password = %s", (t_loginmail, t_loginpassword,))
            
            if check:
                account = cursor.fetchone()
                t_loginmail= account['t_mail']
                t_loginpassword= account['t_password']
                return 'Logged in successfully!'
        return render_template('home.html')

    @app.route('/afterlogin_c', methods=['GET', 'POST'])
    def c_afterlogin():
        if request.method == "POST" and 'c_mail' in request.form and 'c_password' in request.form:
            
            c_loginmail = request.form.get('c_mail')
            c_loginpassword = request.form.get('c_password')
            
            cursor = mysql.connection.cursor()
            
            check = cursor.execute("SELECT* FROM student_club_person WHERE c_mail = %s AND c_password = %s", (c_loginmail, c_loginpassword,))
            

            if check:
                account = cursor.fetchone()
                c_loginmail= account['c_mail']
                c_loginpassword= account['c_password']
                return 'Logged in successfully!'
        return render_template('home.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="localhost", port=8080, debug=True)