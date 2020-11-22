from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
from timeloop import Timeloop
from datetime import date, datetime, timedelta
from rejson import Client, Path
import time
import os

app = Flask(__name__)
CORS(app)
tl = Timeloop()

REDIS_URL = os.getenv('REDIS_URL')
rj = Client(host=REDIS_URL, port=6379, decode_responses=True)

# Helper function for adding, editing and deleting from database
def databaseExecute(query, parameters):
    try:
        con = sqlite3.connect('database/database.db')
        cur = con.cursor()
        cur.execute(query, parameters)
        con.commit()
        con.close()
        return True
    except:
        return False

def getAutoID(task):
    con = sqlite3.connect('database/database.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM tasks WHERE description = ?", (task,))
    ids = cur.fetchall()
    con.commit()
    con.close()
    if (ids):
        return max(ids)[0]
    return 0


@app.route('/getTasks', methods=['GET'])
def getTasks():
    tasks = []
    for key in rj.keys('*'):
        tasks.append(rj.jsonget(key, Path.rootPath()))
    # # Connect to the database
    # con = sqlite3.connect('database/database.db')
    # cur = con.cursor()
    # # Extract all tasks
    # cur.execute("SELECT * FROM tasks")
    # listOfTuples = cur.fetchall()
    # con.close()
    # tasks = []
    # for tup in listOfTuples:
    #     tasks.append({'id': tup[0],
    #                   'checked': tup[1],
    #                   'name': tup[2],
    #                   'description': tup[3],
    #                 })
    return jsonify({'tasks': tasks})


@app.route('/addTask', methods=['POST'])
def addTask():
    # Collect the description
    name = request.get_json()['name']
    description = request.get_json()['description']

    # # Add new task to database
    # query = "INSERT INTO tasks (checked, name, description) VALUES (?, ?, ?)"
    # result = databaseExecute(query, (False, name, description))
    # newID = getAutoID(description)
    newID = len(rj.keys('*'))
    obj = {
        'id': newID,
        'checked': 0,
        'name': name,
        'description': description
    }
    rj.jsonset(newID, Path.rootPath(), obj)
    return jsonify({'id': newID})

@app.route('/editTask', methods=['PUT'])
def editTask():
    # Collect the id and description of current task
    id = request.get_json()['id']
    name = request.get_json()['name']
    description = request.get_json()['description']
    # Change the specified task's description
    # query = "UPDATE tasks SET name = ?, description = ? WHERE id = ?"
    # result = databaseExecute(query, (name, description, id))
    try:
        rj.jsonset(id, Path('.name'), name)
        rj.jsonset(id, Path('.description'), description)
        return jsonify(success=True)
    except:
        return jsonify(success=False)

@app.route('/checkTask', methods=['PUT'])
def checkTask():
    # Collect the id of a current task
    id = request.get_json()['id']
    # checked = request.get_json()['checked']
    # Set the specified task to completed or not completed
    # query = "UPDATE tasks SET checked = ? WHERE id = ?"
    # result = databaseExecute(query, (checked, id))
    # return jsonify(success=result)
    try:
        rj.jsonset(id, Path('.checked'), request.get_json()['checked'])
        return jsonify(success=True)
    except:
        return jsonify(success=False)

@app.route('/deleteTask', methods=['DELETE'])
def deleteTask():
    # Collect the id of a current task
    taskID = request.get_json()['id']
    # Delete task
    try:
        rj.jsondel(taskID, Path.rootPath())
        return jsonify(success=True)
    except:
        return jsonify(success=False)
    # query = "DELETE FROM tasks WHERE id = ?"
    # result = databaseExecute(query, (taskID,))
    # return jsonify(success=result)

@tl.job(interval=timedelta(seconds=20))
def addToSql():
    query_ = "DELETE FROM tasks"
    query = "INSERT INTO tasks (checked, name, description) VALUES (?, ?, ?)"
    try:
        con = sqlite3.connect('database/database.db')
        cur = con.cursor()
        cur.execute(query_)
        con.commit()
        con.close()
        print("success delete all data")
    except:
        print("fail to delete all data")

    try:
        for key in rj.keys('*'):
            task = rj.jsonget(key, Path.rootPath())
            result = databaseExecute(query, (task['checked'], task['name'], task['description']))
        print("success update data")
    except:
        print("fail to update data")


if __name__== "__main__":
    tl.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            tl.stop()
        break
    app.run(host="0.0.0.0", port=5000)
