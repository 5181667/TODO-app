// 页面加载时获取所有待办事项
document.addEventListener('DOMContentLoaded', () => {
    loadTodos();

    // 回车键添加待办
    document.getElementById('todoInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTodo();
        }
    });
});

// 加载所有待办事项
async function loadTodos() {
    try {
        const response = await fetch('/api/todos');
        const todos = await response.json();
        renderTodos(todos);
    } catch (error) {
        console.error('加载失败:', error);
    }
}

// 渲染待办事项列表
function renderTodos(todos) {
    const todoList = document.getElementById('todoList');
    const emptyState = document.getElementById('emptyState');

    todoList.innerHTML = '';

    if (todos.length === 0) {
        emptyState.classList.add('show');
    } else {
        emptyState.classList.remove('show');
        todos.forEach(todo => {
            const li = createTodoElement(todo);
            todoList.appendChild(li);
        });
    }

    updateStats(todos);
}

// 创建单个待办事项元素
function createTodoElement(todo) {
    const li = document.createElement('li');
    li.className = `todo-item ${todo.completed ? 'completed' : ''}`;
    li.dataset.id = todo.id;

    li.innerHTML = `
        <div class="checkbox" onclick="toggleTodo(${todo.id}, ${!todo.completed})"></div>
        <span class="todo-text">${escapeHtml(todo.title)}</span>
        <button class="delete-btn" onclick="deleteTodo(${todo.id})" title="删除">
            🗑️
        </button>
    `;

    return li;
}

// HTML 转义防止 XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 添加新待办事项
async function addTodo() {
    const input = document.getElementById('todoInput');
    const title = input.value.trim();

    if (!title) {
        input.focus();
        return;
    }

    try {
        const response = await fetch('/api/todos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title })
        });

        if (response.ok) {
            input.value = '';
            loadTodos();
        }
    } catch (error) {
        console.error('添加失败:', error);
    }
}

// 切换完成状态
async function toggleTodo(id, completed) {
    try {
        await fetch(`/api/todos/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ completed })
        });
        loadTodos();
    } catch (error) {
        console.error('更新失败:', error);
    }
}

// 删除待办事项
async function deleteTodo(id) {
    try {
        await fetch(`/api/todos/${id}`, {
            method: 'DELETE'
        });
        loadTodos();
    } catch (error) {
        console.error('删除失败:', error);
    }
}

// 更新统计信息
function updateStats(todos) {
    const total = todos.length;
    const completed = todos.filter(t => t.completed).length;

    document.getElementById('totalCount').textContent = `共 ${total} 项`;
    document.getElementById('completedCount').textContent = `已完成 ${completed} 项`;
}
