from flask import Flask, jsonify, request
from todoTableClient import TodoTableClient
import os

app = Flask(__name__)

todoTableClient = TodoTableClient()

@app.route('/todos', methods=['GET'])
def get_todos():
    filter_status = request.args.get('status')
    filter_priority = request.args.get('priority')
    
    todos = todoTableClient.getAllTodos(filter_status, filter_priority)
    return jsonify(todos)

@app.route('/todos/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = todoTableClient.getTodo(todo_id)
    return jsonify(todo)

@app.route('/todos/<todo_id>/complete', methods=['POST'])
def complete_todo(todo_id):
    response = todoTableClient.completeTodo(todo_id)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80) 