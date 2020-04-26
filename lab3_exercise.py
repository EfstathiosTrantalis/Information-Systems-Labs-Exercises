from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json

client = MongoClient('mongodb://localhost:27017/')

db = client['InfoSys']
students = db['Students']

app = Flask(__name__)

@app.route('/getAllStudentAddress', methods=['GET'])
def get_All_Student_Address():
    iterable = students.find({})
    output = []
    for student in iterable:
        if student['address'] !=None : 
            output.append(student)
    return jsonify(output)
    


@app.route('/getStudentAddress/<student_email>', methods=['GET'])
def get_student_by_email(email):
    if email == None:
        return Response("Bad request", status=500, mimetype='application/json')
    student = students.find_one({"email":email})
    if student !=None:
        student = {'address':student["address"]}
        return jsonify(student)
    return Response('no student found',status=500,mimetype='application/json')


@app.route('/getEightiesAddress', methods=['GET'])
def get_eighties_address():
    item = students.find({})
    output = []
    for student in item:
        if student['address'] != None and student['yearOfBirth'] >= 1980 and student['yearOfBirth'] <= 1989:
            output.append(student)
    return  jsonify(output)

@app.route('/countAddress', methods=['GET'])
def count_Address():
    items = students.find({})
    output = []
    for student in items:
        if student['address'] != None:
            output.append(student)
    number_of_students = output.count()            
    return jsonify({"Number of students": number_of_students})

@app.route('/insertstudent', methods=['POST'])
def insert_student():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "name" in data or not "address" in data:
        return Response("Information incompleted",status=500,mimetype="application/json")
    
    if students.find({"name":data["name"]}).count() == 0 :
        student = {"address": data['email'], "name": data['name']}
        
        students.insert_one(student)
        return Response("was added to the MongoDB",status=200,mimetype='application/json') 
    else:
        return Response("A user with the given email already exists",status=200,mimetype='application/json')

@app.route('/countYearofBirth/<yearOfBirth>', methods=['GET'])
def count_Year_Of_Birth(yearOfBirth):
    
    if yearOfBirth == None:
        return Response("Bad request", status=500, mimetype='application/json')
    numberSt = students.find_one({"yearOfBirth":yearOfBirth}).count()
    return jsonify({"Number of students": numberSt})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)




