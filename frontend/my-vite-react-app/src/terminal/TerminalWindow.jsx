import React, { useEffect, useRef, useState } from 'react';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';
import './TerminalPage.css';
import { useParams } from 'react-router-dom';

const TerminalWindow = () => {
  const terminalRef = useRef(null);
  // Получаем sessionId из параметров URL
  const { sessionId } = useParams();
  const [term, setTerm] = useState(null);
  const [fitAddon, setFitAddon] = useState(null);
  const [ws, setWs] = useState(null);

  // Инициализация xterm.js
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

  // Устанавливаем WebSocket-соединение для текущей сессии
  useEffect(() => {
    if (!sessionId) return;
    const socket = new WebSocket(`ws://localhost:8000/ws/ssh/${sessionId}`);
    socket.onopen = () => {
      console.log("WebSocket: onopen");
      setWs(socket);
    };
    socket.onerror = (err) => {
      console.error("WebSocket error:", err);
      if (term) {
        term.write("Ошибка WebSocket-соединения\r\n");
      }
    };
    socket.onmessage = (event) => {
      console.log("WebSocket: onmessage", event.data);
      if (term) {
        term.write(event.data);
      }
    };
    socket.onclose = (e) => {
      console.log("WebSocket: onclose", e);
    };
    return () => {
      socket.close();
    };
  }, [sessionId, term]);

  // Передача ввода терминала через WebSocket
  useEffect(() => {
    if (!ws || !term) return;
    term.onData((data) => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(data);
      }
    });
  }, [ws, term]);

  return (
    <div className="terminal-page">
      <div className="terminal-container" ref={terminalRef}></div>
    </div>
  );
};

export default TerminalWindow;
