import React, { useEffect, useRef, useState } from 'react';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';
import './TerminalPage.css';

const TerminalPage = () => {
  const terminalRef = useRef(null);
  const [term, setTerm] = useState(null);
  const [fitAddon, setFitAddon] = useState(null);
  const [ws, setWs] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [connParams, setConnParams] = useState({
    hostname: '',
    port: 22,
    username: '',
    password: '',
  });
  const [connected, setConnected] = useState(false);

  // Обработчик изменений в форме
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setConnParams((prev) => ({ ...prev, [name]: value }));
  };

  // Создание SSH-сессии через REST и открытие WebSocket-соединения
  const createSession = async (e) => {
    e.preventDefault();
    try {
      console.log("Отправляем запрос на создание сессии:", connParams);
      const response = await fetch('http://localhost:8000/connections/ssh/', {
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
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Ошибка создания соединения');
      }
      const data = await response.json();
      console.log("Сессия создана, session_id:", data.session_id);
      setSessionId(data.session_id);
      // Открываем WebSocket-соединение
      const socket = new WebSocket(`ws://localhost:8000/ws/ssh/${data.session_id}`);
      socket.onopen = () => {
        console.log("WebSocket: onopen");
        setConnected(true);
        setWs(socket);
        if (term) {
          term.focus();
        }
      };
      socket.onerror = (err) => {
        console.error('WebSocket error:', err);
        alert('Ошибка WebSocket-соединения');
      };
      socket.onmessage = (event) => {
        console.log("WebSocket: onmessage", event.data);
        if (term) {
          term.write(event.data);
        }
      };
      socket.onclose = (e) => {
        console.log("WebSocket: onclose", e);
        setConnected(false);
      };
    } catch (error) {
      console.error("Ошибка создания сессии:", error);
      alert(`Ошибка: ${error.message}`);
    }
  };

  // Инициализация терминала xterm.js при монтировании компонента
  useEffect(() => {
    if (!terminalRef.current) return;
    const xterm = new Terminal({
      cursorBlink: true,
      cols: 80,
      rows: 24,
      theme: {
        background: '#1E172F',
        foreground: '#FFFFFF',
      },
    });
    const fit = new FitAddon();
    xterm.loadAddon(fit);
    xterm.open(terminalRef.current);
    fit.fit();
    setTerm(xterm);
    setFitAddon(fit);
    // Устанавливаем фокус, чтобы сразу можно было вводить команды
    xterm.focus();

    const handleResize = () => {
      fit.fit();
    };
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      xterm.dispose();
    };
  }, [terminalRef]);

  // Передача ввода с терминала в WebSocket
  useEffect(() => {
    if (!ws || !term) return;
    term.onData((data) => {
      console.log("Введенные данные:", data);
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(data);
      }
    });
  }, [ws, term]);

  return (
    <div className="terminal-page">
      {/* Форма подключения всегда рендерится */}
      <div className="connection-form-container">
        <h2>Установить SSH-соединение</h2>
        <form onSubmit={createSession}>
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

      {/* Контейнер для терминала всегда присутствует для отладки */}
      <div
        className="terminal-container"
        ref={terminalRef}
        style={{ marginTop: '20px', height: '80vh', border: '2px solid red' }}
      />
    </div>
  );
};

export default TerminalPage;
