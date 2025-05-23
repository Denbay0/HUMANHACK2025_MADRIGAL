// App_terminal.jsx
import React, { useState, useEffect } from 'react';
import './App_ssh.css';

const ConnectionTabs = () => {
  const [activeTab, setActiveTab] = useState('ssh');
  const [server, setServer] = useState(null);
  const [sshCommand, setSshCommand] = useState('');
  const [rdpFile, setRdpFile] = useState({
    ip: '',
    port: 3389,
    username: ''
  });
  const [error, setError] = useState(null);

  useEffect(() => {
    // Если у вас есть рабочий API, раскомментируйте код ниже и замените URL.
    /*
    const fetchServerData = async () => {
      try {
        const response = await fetch('https://api.example.com/servers');
        if (!response.ok) {
          throw new Error('Не удалось загрузить данные о серверах');
        }
        const data = await response.json();
        
        if (data && data.length > 0) {
          setServer(data[0]);
        } else {
          throw new Error('Серверы не найдены');
        }
      } catch (error) {
        setError(error.message);
      }
    };
    fetchServerData();
    */
    
    // Заглушка (dummy data) для тестирования:
    setTimeout(() => {
      const dummyServer = {
        id: 1,
        name: "Test Server",
        ip: "192.168.1.100",
        user: "testuser"
      };
      setServer(dummyServer);
    }, 1000);
  }, []);

  useEffect(() => {
    if (server) {
      setSshCommand(`ssh ${server.user}@${server.ip}`);
      setRdpFile({
        ip: server.ip,
        port: 3389,
        username: server.user,
      });
    }
  }, [server]);

  if (error) {
    return <div className="error">Ошибка: {error}</div>;
  }

  if (!server) {
    return <div>Загрузка...</div>;
  }

  const copyToClipboard = (text) => {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text);
      alert('Скопировано в буфер обмена!');
    } else {
      alert('Ошибка! Буфер обмена недоступен.');
    }
  };

  const downloadRdpFile = () => {
    const content = [
      `full address:s:${rdpFile.ip}:${rdpFile.port}`,
      `username:s:${rdpFile.username}`,
      'session bpp:i:32',
      'autoreconnection enabled:i:1',
    ].join('\n');

    const blob = new Blob([content], { type: 'application/rdp' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${server.name}.rdp`;
    a.click();
  };

  return (
    <main className="body">
      <div className="container">
        <div className="cub"></div>
        <h1 className="name">ServerLink</h1>
        <hr className="line" />

        <div className="connection-tabs">
          <div className="tab-header">
            <button
              className={activeTab === 'ssh' ? 'active' : ''}
              onClick={() => setActiveTab('ssh')}
            >
              SSH
            </button>
            <button
              className={activeTab === 'rdp' ? 'active' : ''}
              onClick={() => setActiveTab('rdp')}
            >
              RDP
            </button>
            <button
              className={activeTab === 'sftp' ? 'active' : ''}
              onClick={() => setActiveTab('sftp')}
            >
              SFTP
            </button>
          </div>

          <div className="tab-content">
            {activeTab === 'ssh' && (
              <div className="ssh-tab">
                <h3>SSH подключение</h3>
                <div className="connection-info">
                  <div className="input-group">
                    <label>Команда для подключения:</label>
                    <div className="command-box">
                      <code>{sshCommand}</code>
                      <button onClick={() => copyToClipboard(sshCommand)}>
                        📋 Скопировать
                      </button>
                    </div>
                  </div>
                  <button
                    className="connect-button"
                    onClick={() =>
                      window.open(`ssh://${server.user}@${server.ip}`)
                    }
                  >
                    Подключиться
                  </button>
                </div>
              </div>
            )}

            {activeTab === 'rdp' && (
              <div className="rdp-tab">
                <h3>RDP подключение</h3>
                <div className="connection-info">
                  <div className="input-group">
                    <label>Адрес сервера:</label>
                    <input type="text" value={rdpFile.ip} readOnly />
                  </div>
                  <div className="input-group">
                    <label>Порт:</label>
                    <input
                      type="number"
                      value={rdpFile.port}
                      onChange={(e) =>
                        setRdpFile({ ...rdpFile, port: e.target.value })
                      }
                    />
                  </div>
                  <div className="input-group">
                    <label>Имя пользователя:</label>
                    <input
                      type="text"
                      value={rdpFile.username}
                      onChange={(e) =>
                        setRdpFile({ ...rdpFile, username: e.target.value })
                      }
                    />
                  </div>
                  <button className="connect-button" onClick={downloadRdpFile}>
                    Скачать RDP файл
                  </button>
                  <p className="hint">
                    Используйте Remote Desktop (Windows) или Remmina (Linux)
                  </p>
                </div>
              </div>
            )}

            {activeTab === 'sftp' && (
              <div className="sftp-tab">
                <h3>SFTP подключение</h3>
                <div className="connection-info">
                  <div className="input-group">
                    <label>Хост:</label>
                    <input type="text" value={server.ip} readOnly />
                  </div>
                  <div className="input-group">
                    <label>Порт:</label>
                    <input type="number" value="22" readOnly />
                  </div>
                  <div className="input-group">
                    <label>Имя пользователя:</label>
                    <input type="text" value={server.user} readOnly />
                  </div>
                  <div className="input-group">
                    <label>Пароль:</label>
                    <input type="password" value="********" readOnly />
                  </div>
                  <button
                    className="connect-button"
                    onClick={() => window.open(`sftp://${server.user}@${server.ip}`)}
                  >
                    Открыть в FileZilla
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
};

export default ConnectionTabs;
