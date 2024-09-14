import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [todos, setTodos] = useState([]);
  const [newTask, setNewTask] = useState('');

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const response = await axios.get('http://localhost:5000/todos');
      setTodos(response.data.list);
    } catch (error) {
      console.error('Error fetching todos:', error);
    }
  };

  const addTodo = async () => {
    if (!newTask.trim()) return;

    try {
      await axios.post('http://localhost:5000/add_todos', { task: newTask });
      setNewTask('');
      fetchTodos();
    } catch (error) {
      console.error('Error adding todo:', error);
    }
  };

  const deleteTodo = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/todos/${id}`);
      fetchTodos();
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  };

  const clearAllTodos = async () => {
    try {
      await axios.delete('http://localhost:5000/todos/clear');
      fetchTodos();
    } catch (error) {
      console.error('Error clearing todos:', error);
    }
  };

  return (
    <div className="container">
      <div className="todo-app">
        <h1>Todo App</h1>
        <div className="input-container">
          <input
            type="text"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            placeholder="Add your new todo"
          />
          <button className="add-btn" onClick={addTodo}></button>
        </div>
        <ul>
          {todos.map(todo => (
            <li key={todo.id}>
              {todo.title}
              <button className="dustbin-btn" onClick={() => deleteTodo(todo.id)}></button>
            </li>
          ))}
        </ul>
        <div className="footer">
          <p>You have {todos.length} pending tasks</p>
          <button onClick={clearAllTodos}>Clear All</button>
        </div>
      </div>
    </div>
  );
}

export default App;

