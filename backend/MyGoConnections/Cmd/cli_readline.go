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
	newReadline := func() *readline.Instance {
		rl, err := readline.NewEx(&readline.Config{
			Prompt:          "",
			HistoryFile:     "/tmp/readline.tmp",
			InterruptPrompt: "^C",
			EOFPrompt:       "exit",
		})
		if err != nil {
			log.Fatalf("Ошибка при инициализации readline: %v", err)
		}
		return rl
	}

	rl := newReadline()
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

	// Если SSH или SFTP, запрашиваем путь к ключевому файлу
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

	fmt.Println("Введите команду для выполнения (например, для FTP: LIST; для SFTP: ls /).")
	fmt.Println("Если используете интерактивную команду (например, vim) на SSH, просто введите её (без префиксов).")
	fmt.Println("Введите 'exit' для завершения работы с сессией.")

	// Главный цикл ввода команд
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

		// Если тип подключения SSH и команда начинается с "vim", выполняем интерактивно
		if connType == "ssh" && strings.HasPrefix(command, "vim") {
			err := sessionManager.ExecuteInteractiveCommand(sessionID, command)
			if err != nil {
				fmt.Printf("Ошибка выполнения интерактивной команды: %v\n", err)
			}
			continue
		}

		// Обычное удалённое выполнение команд
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
