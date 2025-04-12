// connections/session_manager.go
package connections

import (
	"fmt"
	"sync"

	"github.com/google/uuid"
)

type SessionManager struct {
	sessions map[string]Connection
	mu       sync.Mutex
}

func NewSessionManager() *SessionManager {
	return &SessionManager{
		sessions: make(map[string]Connection),
	}
}

func (sm *SessionManager) CreateSession(connType, hostname string, port int, username, password, keyFile string, timeout int) (string, error) {
	var conn Connection

	switch connType {
	case "ssh":
		conn = NewSSHConnection(hostname, port, username, password, keyFile, timeout)
	case "sftp":
		conn = NewSFTPConnection(hostname, port, username, password, keyFile, timeout)
	case "ftp":
		conn = NewFTPConnection(hostname, port, username, password, timeout)
	default:
		return "", fmt.Errorf("Неподдерживаемый тип подключения: %s", connType)
	}

	if err := conn.Connect(); err != nil {
		return "", err
	}

	sessionID := uuid.NewString()
	sm.mu.Lock()
	sm.sessions[sessionID] = conn
	sm.mu.Unlock()
	return sessionID, nil
}

func (sm *SessionManager) ExecuteCommand(sessionID, command string) (string, string, error) {
	sm.mu.Lock()
	conn, ok := sm.sessions[sessionID]
	sm.mu.Unlock()
	if !ok {
		return "", "", fmt.Errorf("Сессия не найдена")
	}
	return conn.ExecuteCommand(command)
}

func (sm *SessionManager) CloseSession(sessionID string) error {
	sm.mu.Lock()
	conn, ok := sm.sessions[sessionID]
	if ok {
		delete(sm.sessions, sessionID)
	}
	sm.mu.Unlock()
	if !ok {
		return fmt.Errorf("Сессия не найдена")
	}
	return conn.Close()
}
