from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
import mysql.connector
import datetime
from studentdetails import students

app = Flask(__name__)

# Mysql database connection details
app.config['MYSQL_USER'] = 'DELL'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_DB'] = 'mysql'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


# logging date time information before each request for performance analysis and other stats
@app.before_request
def before():
    print("This is executed BEFORE each request. Below request has been executed at "
          + str(datetime.datetime.now()))


# let us display home page with html image with css style
@app.route('/')
def hello():
    return render_template('python.html')


# creating student details table inside mysql database
@app.route('/student/create')
def student():
    cur = mysql.connection.cursor()
    cur.execute(
        '''CREATE TABLE studentDetails (id INTEGER PRIMARY KEY, name VARCHAR(20), subjects VARCHAR(200), Marks INTEGER, ExamResult VARCHAR(20), Classcategorty varchar(80))''')
    return 'Student table created successfully. Please verify in mysql database', 200


# now let us add few more students into details table
@app.route('/student/add', methods=['GET'])
def add_student():
    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO studentDetails VALUES (5, 'valli', 'Maths', 200, 'PASS', 'Distinction')''')
    cur.execute('''INSERT INTO studentDetails VALUES (6, 'laxmi', 'Physics', 150, 'PASS', 'First Class')''')
    cur.execute('''INSERT INTO studentDetails VALUES (7, 'Keerti', 'Science', 45, 'Fail', 'None')''')
    cur.execute('''INSERT INTO studentDetails VALUES (8, 'Keerti', 'Social', 112, 'PASS', 'Second Class')''')
    mysql.connection.commit()
    return 'Student details added successfully. Please verify in mysql database', 200


# let us check all inserted details of students committed in mysql database for future reference
@app.route('/student/view', methods=['GET'])
def view_details():
    cur = mysql.connection.cursor()
    cur.execute('''select * from studentDetails''')
    results = cur.fetchall()
    print(results)
    if results is ():
        print('Data is not available in database')
        results = 'Data is not available in database'
    return jsonify(results)


# view details of specific student name
@app.route('/student/display/<string:param>', methods=['GET'])
def get_student_details(param):
    cur = mysql.connection.cursor()
    cur.execute("select * from studentDetails where name = %s", [param])
    results = cur.fetchall()
    print(results)
    if results is ():
        print('student details for %s is not available in database', [param])
        results = 'student details for ' + str(param) + ' is not available in database'
    return jsonify(results)


# add 100 bonus marks for specific student id who excelled both in studies and sports
@app.route('/student/change/<int:index>', methods=['GET'])
def update_details(index):
    try:
        cur = mysql.connection.cursor()
        cur.execute("update studentDetails set marks= marks+100 where id = %s", [index])
        mysql.connection.commit()
    except mysql.connection.Error as err:
        print(err)
        output = 'SQL error for index ' + str([index]) + str(err)
    else:
        output = 'marks updated for student with id as ' + str([index])
    return output


# let us see list of students who all passed or failed
@app.route('/student/exam/<string:Exam_Result>', methods=['GET'])
def exam_details(Exam_Result):
    cur = mysql.connection.cursor()
    cur.execute('''select * from student where Exam_Result = %s''', [Exam_Result])
    results = cur.fetchall()
    print(results)
    if results is ():
        print('Data is not available in database')
        results = 'Data is not available in database'
    return str(results)


# let us delete few student details from mysql storage database as they might moved out to different departments!!
@app.route('/student/delete/<int:index>', methods=['GET'])
def del_details(index):
    cur = mysql.connection.cursor()
    cur.execute('''delete from student where id = %s''', [index])
    mysql.connection.commit()
    return 'Deleted index' + str([index]) + ' successfully', 200


# let us get students additional details
@app.route('/students', methods=['GET'])
def welcome():
    return jsonify(students)


# let us add few more students details to the list from postman!
@app.route('/students/add', methods=['POST'])
def added():
    stud = request.get_json()
    student.append(stud)
    return {"list": student}, 200


# let us update few details based on specific student id
@app.route('/student-update/<int:index>', methods=['PUT'])
def update_student(index):
    stud = request.get_json()
    student[index] = stud
    return jsonify(student[index]), 200


# let us delete few details as they might has passed out this year!!
@app.route('/student-delete/<int:index>', methods=['DELETE'])
def delete_student_id(index):
    student.pop(index)
    return "Deleted Successfully", 200


if __name__ == '__main__':
    app.run(debug=True)
