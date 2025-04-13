import React, { useEffect, useRef, useState } from 'react';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';
import './TerminalPage.css'; // Общие стили для терминала
import { useParams } from 'react-router-dom';

const TerminalWindow = () => {
  const terminalRef = useRef(null);
  const { sessionId } = useParams(); // это ID SSH-сессии для терминала
  const [term, setTerm] = useState(null);
  const [fitAddon, setFitAddon] = useState(null);
  const [ws, setWs] = useState(null);

  // Состояния для SFTP-загрузки файлов:
  const [selectedFile, setSelectedFile] = useState(null);
  const [remotePath, setRemotePath] = useState('');
  // Состояние для SFTP-сессии (отдельной)
  const [sftpSessionId, setSftpSessionId] = useState('');
  // Параметры для создания SFTP-сессии (можно редактировать при необходимости)
  const [sftpParams, setSftpParams] = useState({
    hostname: '',
    port: 22,
    username: '',
    password: '',
    key_filename: ''
  });
  const [sftpFormVisible, setSftpFormVisible] = useState(false);

  // Инициализация терминала (SSH-сессии)
  useEffect(() => {
    if (!terminalRef.current) return;
    const xterm = new Terminal({
      cursorBlink: true,
      cols: 80,
      rows: 24,
      theme: {
        background: '#1E172F',
        foreground: '#FFFFFF'
      },
    });
    const fit = new FitAddon();
    xterm.loadAddon(fit);
    xterm.open(terminalRef.current);
    fit.fit();
    setTerm(xterm);
    setFitAddon(fit);
    xterm.focus();

    const handleResize = () => fit.fit();
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      xterm.dispose();
    };
  }, [terminalRef]);

  // Устанавливаем WebSocket-соединение для SSH (терминала)
  useEffect(() => {
    if (!sessionId) return;
    const socket = new WebSocket(`ws://localhost:8000/ws/ssh/${sessionId}`);
    socket.onopen = () => {
      console.log("WebSocket: SSH-соединение открыто");
      setWs(socket);
    };
    socket.onerror = (err) => {
      console.error("WebSocket error:", err);
      if (term) {
        term.write("Ошибка WebSocket-соединения\r\n");
      }
    };
    socket.onmessage = (event) => {
      console.log("WebSocket: SSH-сообщение", event.data);
      if (term) {
        term.write(event.data);
      }
    };
    socket.onclose = (e) => {
      console.log("WebSocket: SSH-соединение закрыто", e);
    };
    return () => {
      socket.close();
    };
  }, [sessionId, term]);

  // Передаем данные из терминала через WebSocket (если используется)
  useEffect(() => {
    if (!ws || !term) return;
    term.onData((data) => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(data);
      }
    });
  }, [ws, term]);

  // Форма создания SFTP-сессии
  const handleSftpParamChange = (e) => {
    const { name, value } = e.target;
    setSftpParams(prev => ({ ...prev, [name]: value }));
  };

  const createSftpSession = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      // Выполняем запрос к эндпоинту создания SFTP-сессии
      const response = await fetch("http://localhost:8000/connections/sftp/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          hostname: sftpParams.hostname,
          port: parseInt(sftpParams.port, 10),
          username: sftpParams.username,
          password: sftpParams.password,
          key_filename: sftpParams.key_filename,
          timeout: 10
        }),
      });
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Ошибка создания SFTP-сессии");
      }
      const data = await response.json();
      console.log("SFTP-сессия создана, session_id:", data.session_id);
      setSftpSessionId(data.session_id);
      alert("SFTP-сессия создана");
      setSftpFormVisible(false);
    } catch (error) {
      console.error("Ошибка создания SFTP-сессии:", error);
      alert("Ошибка: " + error.message);
    }
  };

  // Обработчик выбора файла для загрузки
  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  // Обработчик изменения удалённого пути
  const handleRemotePathChange = (e) => {
    setRemotePath(e.target.value);
  };

  // Функция загрузки файла через SFTP (использует sftpSessionId)
  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile || !remotePath) {
      alert("Выберите файл и укажите удалённый путь");
      return;
    }
    if (!sftpSessionId) {
      alert("Сначала создайте SFTP-сессию");
      return;
    }
    try {
      const formData = new FormData();
      formData.append("session_id", sftpSessionId);
      formData.append("remote_path", remotePath);
      formData.append("file", selectedFile);

      const response = await fetch("http://localhost:8000/sftp-upload/", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Ошибка загрузки файла");
      }
      alert("Файл успешно загружен");
      setSelectedFile(null);
      setRemotePath("");
    } catch (error) {
      console.error("Ошибка загрузки файла:", error);
      alert("Ошибка загрузки файла: " + error.message);
    }
  };

  return (
    <div className="terminal-page">
      {/* Контейнер терминала (SSH) */}
      <div className="terminal-container" ref={terminalRef}></div>
      
      {/* Блок для создания SFTP-сессии */}
      <div className="sftp-upload-container">
        <h3>Файловый менеджер (SFTP)</h3>
        {!sftpSessionId && !sftpFormVisible && (
          <button onClick={() => setSftpFormVisible(true)}>Создать SFTP-сессию</button>
        )}
        {sftpFormVisible && (
          <form onSubmit={createSftpSession}>
            <div className="form-group">
              <label>Hostname:</label>
              <input
                type="text"
                name="hostname"
                value={sftpParams.hostname}
                onChange={handleSftpParamChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Port:</label>
              <input
                type="number"
                name="port"
                value={sftpParams.port}
                onChange={handleSftpParamChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Username:</label>
              <input
                type="text"
                name="username"
                value={sftpParams.username}
                onChange={handleSftpParamChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Password:</label>
              <input
                type="password"
                name="password"
                value={sftpParams.password}
                onChange={handleSftpParamChange}
              />
            </div>
            <div className="form-group">
              <label>Key Filename (если есть):</label>
              <input
                type="text"
                name="key_filename"
                value={sftpParams.key_filename}
                onChange={handleSftpParamChange}
              />
            </div>
            <button type="submit">Создать SFTP-сессию</button>
          </form>
        )}
        {sftpSessionId && (
          <>
            <p>SFTP-сессия активна (ID: {sftpSessionId})</p>
            <form onSubmit={handleFileUpload}>
              <div className="form-group">
                <label>Удалённый путь (например, /home/user/filename.ext):</label>
                <input
                  type="text"
                  name="remotePath"
                  value={remotePath}
                  onChange={handleRemotePathChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Выберите файл:</label>
                <input
                  type="file"
                  name="file"
                  onChange={handleFileChange}
                  required
                />
              </div>
              <button type="submit">Загрузить файл</button>
            </form>
          </>
        )}
      </div>
    </div>
  );
};

export default TerminalWindow;
