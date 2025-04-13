import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './TerminalPage.css';

const TerminalPage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Необходимо авторизоваться. Пожалуйста, войдите.");
      navigate('/login');
    }
  }, [navigate]);

  const [connParams, setConnParams] = useState({
    server_name: '',
    hostname: '',
    port: 22,
    username: '',
    password: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setConnParams((prev) => ({ ...prev, [name]: value }));
  };

  const createSession = async (e) => {
    e.preventDefault();
    try {
      console.log("Создаем SSH-сессию:", connParams);
      const sshResp = await fetch('http://localhost:8000/connections/ssh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          hostname: connParams.hostname,
          port: parseInt(connParams.port, 10),
          username: connParams.username,
          password: connParams.password,
          timeout: 10,
        }),
      });
      if (!sshResp.ok) {
        const errData = await sshResp.json();
        throw new Error(errData.detail || 'Ошибка создания SSH-сессии');
      }
      const sshData = await sshResp.json();
      console.log("SSH-сессия создана, session_id:", sshData.session_id);

      const token = localStorage.getItem("token");
      const saveResp = await fetch('http://localhost:8000/ssh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          jwt_token: token,
          server_name: connParams.server_name,
          host: connParams.hostname,
          port: parseInt(connParams.port, 10),
          username: connParams.username,
          password: connParams.password,
          private_key: null,
        }),
      });
      if (!saveResp.ok) {
        const saveErr = await saveResp.json();
        console.error("Ошибка сохранения сервера:", saveErr.detail);
      } else {
        console.log("Информация о сервере сохранена");
      }

      // Открываем терминал в новой вкладке
      window.open(`/terminal/${sshData.session_id}`, '_blank');
    } catch (error) {
      console.error("Ошибка:", error);
      alert("Ошибка: " + error.message);
    }
  };

  return (
    <div className="terminal-page">
      {/* Кнопка "Назад" с отступом */}
      <button className="back-button" onClick={() => navigate('/profile')}>
        Назад
      </button>

      <div className="connection-form-container">
        <h2>Подключиться к серверу</h2>
        <form onSubmit={createSession}>
          <div className="form-group">
            <label>Server Name:</label>
            <input
              type="text"
              name="server_name"
              value={connParams.server_name}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Hostname:</label>
            <input
              type="text"
              name="hostname"
              value={connParams.hostname}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Port:</label>
            <input
              type="number"
              name="port"
              value={connParams.port}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Username:</label>
            <input
              type="text"
              name="username"
              value={connParams.username}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Password:</label>
            <input
              type="password"
              name="password"
              value={connParams.password}
              onChange={handleInputChange}
              required
            />
          </div>
          <button type="submit">Подключиться</button>
        </form>
      </div>
    </div>
  );
};

export default TerminalPage;
