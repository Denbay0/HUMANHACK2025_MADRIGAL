// connections/sftp_connection.go
package connections

import (
	"fmt"
	"io/ioutil"
	"log"
	"time"

	"github.com/pkg/sftp"
	"golang.org/x/crypto/ssh"
)

type SFTPConnection struct {
	Hostname   string
	Port       int
	Username   string
	Password   string
	KeyFile    string
	Timeout    time.Duration
	sshClient  *ssh.Client
	sftpClient *sftp.Client
}

func NewSFTPConnection(hostname string, port int, username, password, keyFile string, timeout int) *SFTPConnection {
	return &SFTPConnection{
		Hostname: hostname,
		Port:     port,
		Username: username,
		Password: password,
		KeyFile:  keyFile,
		Timeout:  time.Duration(timeout) * time.Second,
	}
}

func (s *SFTPConnection) Connect() error {
	var authMethods []ssh.AuthMethod
	if s.KeyFile != "" && s.KeyFile != "string" {
		key, err := ioutil.ReadFile(s.KeyFile)
		if err != nil {
			return fmt.Errorf("[SFTP] Не удалось прочитать ключевой файл: %v", err)
		}
		signer, err := ssh.ParsePrivateKey(key)
		if err != nil {
			return fmt.Errorf("[SFTP] Не удалось распарсить ключ: %v", err)
		}
		authMethods = append(authMethods, ssh.PublicKeys(signer))
	} else if s.Password != "" {
		authMethods = append(authMethods, ssh.Password(s.Password))
	} else {
		return fmt.Errorf("[SFTP] Не предоставлен пароль или ключевой файл")
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
		log.Printf("[SFTP] Ошибка подключения к %s: %v", addr, err)
		return err
	}
	s.sshClient = client

	sftpClient, err := sftp.NewClient(client)
	if err != nil {
		return fmt.Errorf("[SFTP] Не удалось создать SFTP клиент: %v", err)
	}
	s.sftpClient = sftpClient

	log.Printf("[SFTP] Подключение установлено к %s", addr)
	return nil
}

func (s *SFTPConnection) ExecuteCommand(command string) (string, string, error) {
	// Пример: выполнение команд в SFTP не реализовано
	return "", "", fmt.Errorf("[SFTP] Выполнение команд не реализовано")
}

func (s *SFTPConnection) Close() error {
	if s.sftpClient != nil {
		if err := s.sftpClient.Close(); err != nil {
			log.Printf("[SFTP] Ошибка закрытия SFTP клиента: %v", err)
		}
	}
	if s.sshClient != nil {
		if err := s.sshClient.Close(); err != nil {
			log.Printf("[SFTP] Ошибка закрытия SSH соединения: %v", err)
		}
	}
	log.Printf("[SFTP] Соединение с %s:%d закрыто", s.Hostname, s.Port)
	return nil
}
