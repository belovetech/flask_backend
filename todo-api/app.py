#!/usr/bin/python3
import json
from flask import Flask, jsonify
from flask import request, Response
from flask import abort
from flask import make_response

app = Flask(__name__)

with open("./dev-data/data/todos.json", "r") as json_file:
    todos = json.load(json_file)


@app.route("/api/v1/todos", methods=["GET"])
def getAllTodos():

    return jsonify({
        "success": True,
        "results": len(todos),
        "data": todos
    })


@app.route("/api/v1/todos/<int:id>", methods=["GET"])
def getTodo(id):

    todo = {"todo": todo for todo in todos if todo["id"] == id}

    print(todos)

    if len(todo) == 0:
        abort(404)

    return jsonify({
        "success": True,
        "todo": todo["todo"]
    })


@app.route("/api/v1/todos", methods=["POST"])
def createTodo():
    todo = request.json

    if not todo or not "title" in todo:
        abort(400)

    #     # todo = {
    #     #     'id': tasks[-1]['id'] + 1,
    #     #     'title': request.json['title'],
    #     #     'description': request.json.get('description', ""),
    #     #     'done': False
    #     # }

    todo["id"] = int(todos[-1]["id"]) + 1
    todos.append(todo)

    with open("./dev-data/data/todos.json", "w", encoding="utf-8") as json_file:
        json_file.write(json.dumps(todos))

    return jsonify({
        "success": True,
        "todo": todo
    }), 201


@app.route("/api/v1/todos/<int:id>", methods=["PUT"])
def updateTodo(id):
    data = request.json
    todo = {"todo": todo for todo in todos if todo["id"] == id}

    if not todo:
        abort(404)

    if "id" not in data:
        abort(400)
    if "description" not in data:
        abort(400)
    if "title" not in data:
        abort(400)
    if "done" not in data and type(json.loads(data['done'].lower())) is not bool:
        abort(400)

    index = todos.index(todo["todo"])
    todos[index] = request.json

    with open("./dev-data/data/todos.json", "w", encoding="utf-8") as json_file:
        json_file.write(json.dumps(todos))

    return jsonify({
        "success": True,
        "todo": data
    }), 201


@app.route('/api/v1/todos/<int:id>', methods=['DELETE'])
def deleteTodo(id):
    try:
        todo = {"todo": todo for todo in todos if todo["id"] == id}

        if not todo:
            abort(404)

        todos.remove(todo['todo'])

        with open("./dev-data/data/todos.json", "w", encoding="utf-8") as json_file:
            json_file.write(json.dumps(todos))

        return jsonify({
            'success': True,
            'status': 204,
            'message': 'No content'
        })
    except:
        abort(500)


# ERRORS HANDLERS
@app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify({
            "success": False,
            "status": 404,
            "message": "Resourcse Not Found"
        }), 404,)


@app.errorhandler(400)
def not_found(error):
    return make_response(
        jsonify({
            "success": False,
            "status": 400,
            "message": "Bad request"
        }), 400)


@app.errorhandler(500)
def not_found(error):
    return make_response(
        jsonify({
            "success": False,
            "status": 500,
            "message": "Internal Server Error"
        }), 500)


if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="127.0.0.1")
