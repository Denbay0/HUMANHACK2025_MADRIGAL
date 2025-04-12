import React, { useEffect, useRef } from 'react';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';

export default function TerminalTest() {
  const terminalRef = useRef(null);

  useEffect(() => {
    // Создаем терминал
    const term = new Terminal({
      cursorBlink: true,
      rows: 24,
      cols: 80,
      theme: {
        background: '#202B33', // более заметный фон, если вдруг сайт темный
        foreground: '#F5F8FA', // светлый текст
      },
    });
    const fitAddon = new FitAddon();
    term.loadAddon(fitAddon);

    // Монтируем терминал в DOM
    term.open(terminalRef.current);
    fitAddon.fit();

    // Пишем тестовое сообщение
    term.write('Hello from xterm!\r\n');
    term.write('Если вы видите этот текст, xterm.js работает.\r\n');
    term.write('Попробуйте ввести что-нибудь...\r\n');

    // Для демонстрации, при вводе данных печатаем их в терминал
    term.onData(data => {
      term.write(data);
    });

    // По желанию, можно установить фокус, чтобы сразу можно было вводить
    term.focus();

    // Очистка при размонтировании
    return () => {
      term.dispose();
    };
  }, []);

  return (
    <div
      style={{
        width: '100%',
        height: '100vh',
        background: '#2E2644',
        display: 'flex',
        flexDirection: 'column',
        margin: 0,
        padding: 0
      }}
    >
      <div
        ref={terminalRef}
        style={{
          flex: '1',            // занимаем всё доступное пространство родителя
          border: '2px solid red', // для наглядности красная рамка
        }}
      />
    </div>
  );
}
