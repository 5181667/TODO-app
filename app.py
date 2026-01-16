import os
from flask import Flask, render_template, request, jsonify
from models import db, Todo

app = Flask(__name__)

# 数据库配置 - 支持 SQLite (开发) 和 PostgreSQL (生产)
database_url = os.environ.get('DATABASE_URL', 'sqlite:///todos.db')
# 兼容 Heroku/Railway 的 postgres:// URL
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 创建数据库表
with app.app_context():
    db.create_all()

# 页面路由
@app.route('/')
def index():
    return render_template('index.html')

# API 路由
@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': '标题不能为空'}), 400
    
    todo = Todo(title=data['title'].strip())
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json()
    
    if 'completed' in data:
        todo.completed = data['completed']
    if 'title' in data:
        todo.title = data['title'].strip()
    
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': '删除成功'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
