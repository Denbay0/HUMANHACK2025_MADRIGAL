// connections/ftp_connection.go
package connections

import (
	"fmt"
	"log"
	"strings"
	"time"

	"github.com/jlaffaye/ftp"
)

type FTPConnection struct {
	Hostname string
	Port     int
	Username string
	Password string
	Timeout  time.Duration
	client   *ftp.ServerConn
}

func NewFTPConnection(hostname string, port int, username, password string, timeout int) *FTPConnection {
	return &FTPConnection{
		Hostname: hostname,
		Port:     port,
		Username: username,
		Password: password,
		Timeout:  time.Duration(timeout) * time.Second,
	}
}

func (f *FTPConnection) Connect() error {
	addr := fmt.Sprintf("%s:%d", f.Hostname, f.Port)
	conn, err := ftp.Dial(addr, ftp.DialWithTimeout(f.Timeout))
	if err != nil {
		log.Printf("[FTP] Ошибка подключения к %s: %v", addr, err)
		return err
	}
	err = conn.Login(f.Username, f.Password)
	if err != nil {
		return fmt.Errorf("[FTP] Не удалось выполнить вход: %v", err)
	}
	f.client = conn
	log.Printf("[FTP] Подключение установлено к %s", addr)
	return nil
}

func (f *FTPConnection) ExecuteCommand(command string) (string, string, error) {
	upperCmd := strings.ToUpper(strings.TrimSpace(command))
	if upperCmd == "LIST" {
		entries, err := f.client.List("")
		if err != nil {
			return "", fmt.Sprintf("[FTP] Ошибка выполнения LIST: %v", err), err
		}
		var output strings.Builder
		for _, entry := range entries {
			output.WriteString(entry.Name)
			output.WriteRune('\n')
		}
		return output.String(), "", nil
	}
	return "", "", fmt.Errorf("[FTP] Команда '%s' не поддерживается. Поддерживается только команда LIST.", command)
}

func (f *FTPConnection) Close() error {
	if f.client != nil {
		if err := f.client.Quit(); err != nil {
			log.Printf("[FTP] Ошибка при закрытии соединения: %v", err)
			return err
		}
		log.Printf("[FTP] Соединение с %s:%d закрыто", f.Hostname, f.Port)
	}
	return nil
}
