from flask import Flask, request, jsonify,redirect, Response
import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient('mongodb://localhost:27017/')

db = client['InfoSys']
courses = db['Courses']
students = db['Students']

app = Flask(__name__)

@app.route('/insert-course', methods=['POST'])
def insert_course():
    data = None
    try:   
        data = json.loads(request.data)
    except Exception as e:
        return Response('bad json content',status = 500)    
    if data == None:
        return Response("bad request",status=500)
    if not "courseid" in data or not "name" in data or not "ects" in data:
        return Response("Information incompleted.Must contain courseid,name,ects", status=500)        

    if courses.find({"courseid":data["courseid"]}).count() == 0:
        course = {"courseid" : data['courseid'], "name" : data['name'], "ects": data['ects']}
        courses.insert_one(course)
        return Response(data['name']+"was added to the MongoDB",status=200)
    else:
        return Response("A course with the given id already exists", status=200)    
    

@app.route('/get-course' , methods=['GET'])
def get_course():
    cid = request.args.get('courseid')
    if cid == None:
        return Response("Bad request", status=500)
    course = courses.find_one({"courseid": cid})    
    if course != None:
        course = {"courseid":course['courseid'],"name":course['name'],"ects":course["ects"]}
        return jsonify(course)
    else:
        return Response('No course found',status=500)    


"""@app.route('/add-course/<string:student_email>', methods=['PUT'])
def add_course(student_email):
    
    if student_email == None:
        return Response('Bad request', status=500)
    student = students.find_one({"email":student_email})
    if student ==None:
        return Response("No student found with this email", status=500)    

    try:
        student=students.update_one({"email":student_email},
        {"$set":
            {
                "course":request.form["courseid"]

            }
        })"""
        
@app.route('/delete-student', methods=['DELETE'])
def delete_student():
    email = request.args.get('email')
    if email == None:
        return Response("Bad request", status=500)
    students.delete_one({"email":email})
    return Response("Student deleted successfully", status=200)            


@app.route('/insert-course-description', methods=['POST'])
def insert_course_description():
    courseid = request.args.get('courseid')
    if request.data:
        data = json.loads(request.data)
    for i, course in enumerate(courses):
        if course['courseid'] == courseid:
            courses[i] = data
            return Response('course was updated', status=200)

        return Response('people was not updated',status=500)
    else:
        return Response('people was not updated',status=500)    


@app.route('/update-course',methods=['PUT'])
def update_course():
    courseid = request.args.get('courseid')
    if courseid == None:
        return Response('Bad request',status=500)
    course = courses.find_one({"courseid":courseid})
    if course == None:
        return Response('No course found', status=500)
    try :
        course = courses.update_one({"courseid":courseid},
        {"$set":
            {
                "courseid":request.form['courseid'],
                "name": request.form['name'],
                "ects": request.form['ects'],
                "description": request.form['description']

            }
        
        })
        course = courses.find_one({"courseid":courseid})
        course = {'courseid':course['courseid'],'name':course['name'],'ects':course['ects'],'description':course['description']}
        return jsonify(course)
    except Exception as e:
        return Response('Course could not be updated',staus=500)    
        
        
        






if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)
