from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://todo_list_tcca_user:u9tDAjOMAYsdc65Kkvb3bVy86xZ33pHv@dpg-criq3t5umphs73copeg0-a.oregon-postgres.render.com/todo_list_tcca'

db = SQLAlchemy(app)

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<User {self.title}>'
    
    def __init__(self, title):
        self.title = title

@app.route('/', methods=['GET'])
def home():
    todo = Todos.query.all()
    todo_dict = {tod.id: tod.title for tod in todo}
    arr = []
    for to in todo:
        dt = {"id":to.id, "title":to.title}
        arr.append(dt)
    print(arr)
    return jsonify({"list": arr})

@app.route('/add_todos', methods=['POST'])
def add_task():
    title = request.json['task']
    todo = Todos(title)
    db.session.add(todo)
    db.session.commit()
    return{"Msg": "Task added"}

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todos.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({"message": "Todo deleted successfully!"})
    return jsonify({"message": "Todo not found!"}), 404

@app.route('/todos/clear', methods=['DELETE'])
def clear_all():
    try:
        db.session.query(Todos).delete()
        db.session.commit()
        return jsonify({"message": "All todos cleared!"})
    except Exception as e:
        return jsonify({"message": "Failed to clear todos", "error": str(e)})

if __name__ == "__main__":
    app.run()
