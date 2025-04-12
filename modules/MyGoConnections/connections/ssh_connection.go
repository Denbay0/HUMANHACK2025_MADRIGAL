// connections/ssh_connection.go
package connections

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"sync"
	"time"

	"golang.org/x/crypto/ssh"
	"golang.org/x/term"
)

type SSHConnection struct {
	Hostname string
	Port     int
	Username string
	Password string
	KeyFile  string
	Timeout  time.Duration
	Client   *ssh.Client
	clientMu sync.Mutex
}

func NewSSHConnection(hostname string, port int, username, password, keyFile string, timeout int) *SSHConnection {
	return &SSHConnection{
		Hostname: hostname,
		Port:     port,
		Username: username,
		Password: password,
		KeyFile:  keyFile,
		Timeout:  time.Duration(timeout) * time.Second,
	}
}

func (s *SSHConnection) Connect() error {
	var authMethods []ssh.AuthMethod
	if s.KeyFile != "" && s.KeyFile != "string" {
		key, err := ioutil.ReadFile(s.KeyFile)
		if err != nil {
			return fmt.Errorf("[SSH] Не удалось прочитать ключевой файл: %v", err)
		}
		signer, err := ssh.ParsePrivateKey(key)
		if err != nil {
			return fmt.Errorf("[SSH] Не удалось распарсить ключ: %v", err)
		}
		authMethods = append(authMethods, ssh.PublicKeys(signer))
	} else if s.Password != "" {
		authMethods = append(authMethods, ssh.Password(s.Password))
	} else {
		return fmt.Errorf("[SSH] Не предоставлен пароль или ключевой файл")
	}

	config := &ssh.ClientConfig{
		User:            s.Username,
		Auth:            authMethods,
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
		Timeout:         s.Timeout,
	}

	addr := fmt.Sprintf("%s:%d", s.Hostname, s.Port)
	client, err := ssh.Dial("tcp", addr, config)
	if err != nil {
		log.Printf("[SSH] Ошибка подключения к %s: %v", addr, err)
		return err
	}
	s.clientMu.Lock()
	s.Client = client
	s.clientMu.Unlock()
	log.Printf("[SSH] Подключение установлено к %s", addr)
	return nil
}

func (s *SSHConnection) ExecuteCommand(command string) (string, string, error) {
	s.clientMu.Lock()
	defer s.clientMu.Unlock()
	if s.Client == nil {
		return "", "", fmt.Errorf("[SSH] Соединение не установлено – вызовите Connect()")
	}
	session, err := s.Client.NewSession()
	if err != nil {
		return "", "", fmt.Errorf("[SSH] Не удалось создать сессию: %v", err)
	}
	defer session.Close()

	var stdoutBuf, stderrBuf bytes.Buffer
	session.Stdout = &stdoutBuf
	session.Stderr = &stderrBuf

	if err := session.Run(command); err != nil {
		return stdoutBuf.String(), stderrBuf.String(), fmt.Errorf("[SSH] Ошибка выполнения команды: %v", err)
	}
	return stdoutBuf.String(), stderrBuf.String(), nil
}

// Новый метод для интерактивного выполнения команд (например, vim)
func (s *SSHConnection) ExecuteInteractiveCommand(command string) error {
	s.clientMu.Lock()
	defer s.clientMu.Unlock()
	if s.Client == nil {
		return fmt.Errorf("[SSH] Соединение не установлено – вызовите Connect()")
	}
	session, err := s.Client.NewSession()
	if err != nil {
		return fmt.Errorf("[SSH] Не удалось создать сессию: %v", err)
	}
	defer session.Close()

	// Получаем размеры терминала
	width, height, err := term.GetSize(int(os.Stdin.Fd()))
	if err != nil {
		width, height = 80, 24
	}
	// Определяем терминальные режимы
	modes := ssh.TerminalModes{
		ssh.ECHO:          1,
		ssh.TTY_OP_ISPEED: 14400,
		ssh.TTY_OP_OSPEED: 14400,
	}
	if err := session.RequestPty("xterm", height, width, modes); err != nil {
		return fmt.Errorf("[SSH] Не удалось запросить pty: %v", err)
	}

	// Переводим терминал в raw-режим, чтобы обеспечить корректную работу интерактивных приложений
	oldState, err := term.MakeRaw(int(os.Stdin.Fd()))
	if err != nil {
		return fmt.Errorf("[SSH] Не удалось установить raw режим: %v", err)
	}
	defer term.Restore(int(os.Stdin.Fd()), oldState)

	session.Stdin = os.Stdin
	session.Stdout = os.Stdout
	session.Stderr = os.Stderr

	if err := session.Start(command); err != nil {
		return fmt.Errorf("[SSH] Ошибка запуска интерактивной команды: %v", err)
	}
	if err := session.Wait(); err != nil {
		return fmt.Errorf("[SSH] Ошибка ожидания завершения интерактивной команды: %v", err)
	}
	return nil
}

func (s *SSHConnection) Close() error {
	s.clientMu.Lock()
	defer s.clientMu.Unlock()
	if s.Client != nil {
		err := s.Client.Close()
		if err != nil {
			log.Printf("[SSH] Ошибка закрытия соединения: %v", err)
			return err
		}
		log.Printf("[SSH] Соединение с %s:%d закрыто", s.Hostname, s.Port)
		s.Client = nil
	}
	return nil
}
