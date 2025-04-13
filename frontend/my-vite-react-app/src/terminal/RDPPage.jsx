import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './rdp.css';

const RDPPage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Необходимо авторизоваться. Пожалуйста, войдите.");
      navigate("/login");
    }
  }, [navigate]);

  // Параметры для RDP-подключения
  const [connParams, setConnParams] = useState({
    server_name: '',
    hostname: '',
    port: 3389,
    username: '',
    password: '',
    domain: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setConnParams(prev => ({ ...prev, [name]: value }));
  };

  const createRDPConnection = async (e) => {
    e.preventDefault();
    try {
      console.log("Создаем RDP-подключение:", connParams);
      const token = localStorage.getItem("token");
      const response = await fetch('http://localhost:8000/rdp-connection/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          jwt_token: token,
          server_name: connParams.server_name,
          hostname: connParams.hostname,
          port: parseInt(connParams.port, 10),
          username: connParams.username,
          password: connParams.password,
          domain: connParams.domain
        }),
      });
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Ошибка создания RDP-подключения");
      }
      const data = await response.json();
      console.log("RDP-подключение создано, join_url:", data.join_url);
      // Перебрасываем пользователя на полученный URL
      window.open(data.join_url, "_blank");
    } catch (error) {
      console.error("Ошибка RDP-подключения:", error);
      alert("Ошибка: " + error.message);
    }
  };

  return (
    <div className="rdp-page">
      {/* Кнопка "Назад" */}
      <button className="back-button" onClick={() => navigate('/profile')}>
        Назад
      </button>

      <div className="rdp-connection-container">
        <h2>Подключиться по RDP</h2>
        <form onSubmit={createRDPConnection}>
          <div className="rdp-form-group">
            <label>Server Name:</label>
            <input
              type="text"
              name="server_name"
              value={connParams.server_name}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="rdp-form-group">
            <label>Hostname:</label>
            <input
              type="text"
              name="hostname"
              value={connParams.hostname}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="rdp-form-group">
            <label>Port:</label>
            <input
              type="number"
              name="port"
              value={connParams.port}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="rdp-form-group">
            <label>Username:</label>
            <input
              type="text"
              name="username"
              value={connParams.username}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="rdp-form-group">
            <label>Password:</label>
            <input
              type="password"
              name="password"
              value={connParams.password}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="rdp-form-group">
            <label>Domain (необязательно):</label>
            <input
              type="text"
              name="domain"
              value={connParams.domain}
              onChange={handleInputChange}
            />
          </div>
          <button type="submit">Подключиться</button>
        </form>
      </div>
    </div>
  );
};

export default RDPPage;
