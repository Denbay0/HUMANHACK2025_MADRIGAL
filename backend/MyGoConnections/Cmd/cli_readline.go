// Cmd/cli_readline.go
package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"

	"github.com/Denbay0/HUMANHACK2025_MADRIGAL/MyGoConnections/connections"
	"github.com/chzyer/readline"
)

func main() {
	rl, err := readline.NewEx(&readline.Config{
		Prompt:          "",                  // изначально пустой prompt
		HistoryFile:     "/tmp/readline.tmp", // можно задать файл истории
		InterruptPrompt: "^C",
		EOFPrompt:       "exit",
	})
	if err != nil {
		log.Fatalf("Ошибка при инициализации readline: %v", err)
	}
	defer rl.Close()

	sessionManager := connections.NewSessionManager()

	// Запрос типа подключения
	fmt.Println("Выберите тип подключения:")
	fmt.Println("1. SSH")
	fmt.Println("2. FTP")
	fmt.Println("3. SFTP")
	rl.SetPrompt("Введите номер (1/2/3): ")
	choiceLine, err := rl.Readline()
	if err != nil {
		log.Fatalf("Ошибка ввода: %v", err)
	}
	choice := strings.TrimSpace(choiceLine)
	var connType string
	switch choice {
	case "1":
		connType = "ssh"
	case "2":
		connType = "ftp"
	case "3":
		connType = "sftp"
	default:
		fmt.Println("Неверный выбор")
		os.Exit(1)
	}

	// Запрос адреса сервера
	rl.SetPrompt("Введите адрес сервера: ")
	hostname, err := rl.Readline()
	if err != nil {
		log.Fatalf("Ошибка ввода: %v", err)
	}
	hostname = strings.TrimSpace(hostname)

	// Запрос порта
	rl.SetPrompt("Введите порт (по умолчанию): ")
	portStr, err := rl.Readline()
	if err != nil {
		log.Fatalf("Ошибка ввода: %v", err)
	}
	portStr = strings.TrimSpace(portStr)
	port := 0
	if portStr != "" {
		p, err := strconv.Atoi(portStr)
		if err != nil {
			log.Fatalf("Неверное значение порта: %v", err)
		}
		port = p
	} else {
		if connType == "ftp" {
			port = 21
		} else {
			port = 22
		}
	}

	// Запрос логина
	rl.SetPrompt("Введите логин: ")
	username, err := rl.Readline()
	if err != nil {
		log.Fatalf("Ошибка ввода: %v", err)
	}
	username = strings.TrimSpace(username)

	// Запрос пароля
	rl.SetPrompt("Введите пароль: ")
	password, err := rl.Readline()
	if err != nil {
		log.Fatalf("Ошибка ввода: %v", err)
	}
	password = strings.TrimSpace(password)

	// Запрос пути к ключевому файлу, если требуется
	var keyFile string
	if connType == "ssh" || connType == "sftp" {
		rl.SetPrompt("Введите путь к ключевому файлу (или оставьте пустым): ")
		keyFile, err = rl.Readline()
		if err != nil {
			log.Fatalf("Ошибка ввода: %v", err)
		}
		keyFile = strings.TrimSpace(keyFile)
	}

	// Создание сессии
	sessionID, err := sessionManager.CreateSession(connType, hostname, port, username, password, keyFile, 10)
	if err != nil {
		fmt.Printf("Ошибка при создании сессии: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Сессия создана с ID: %s\n", sessionID)

	fmt.Println("Введите команду для выполнения (например, для FTP: LIST; для SFTP: ls /):")
	fmt.Println("Введите 'exit' для завершения работы с сессией.")

	// Цикл ввода команд с новым приглашением по каждому разу
	for {
		rl.SetPrompt("Команда: ")
		line, err := rl.Readline()
		if err != nil {
			log.Fatalf("Ошибка ввода: %v", err)
		}
		command := strings.TrimSpace(line)
		if strings.ToLower(command) == "exit" {
			break
		}
		stdout, stderr, err := sessionManager.ExecuteCommand(sessionID, command)
		if err != nil {
			fmt.Printf("Ошибка выполнения команды: %v\n", err)
			continue
		}
		fmt.Println("=== STDOUT ===")
		fmt.Println(stdout)
		if stderr != "" {
			fmt.Println("=== STDERR ===")
			fmt.Println(stderr)
		}
	}

	err = sessionManager.CloseSession(sessionID)
	if err != nil {
		fmt.Printf("Ошибка при закрытии сессии: %v\n", err)
	} else {
		fmt.Println("Сессия закрыта.")
	}
}
