// Main.go
package main

import (
	"net/http"

	"github.com/Denbay0/HUMANHACK2025_MADRIGAL/MyGoConnections/connections"

	"github.com/gin-gonic/gin"
)

func Main() {
	router := gin.Default()
	sessionManager := connections.NewSessionManager()

	// SSH эндпоинт
	router.POST("/connections/ssh", func(c *gin.Context) {
		var req struct {
			Hostname string `json:"hostname" binding:"required"`
			Port     int    `json:"port" binding:"omitempty"`
			Username string `json:"username" binding:"required"`
			Password string `json:"password"`
			KeyFile  string `json:"key_filename"`
			Timeout  int    `json:"timeout" binding:"omitempty"`
		}
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		if req.Port == 0 {
			req.Port = 22
		}
		if req.Timeout == 0 {
			req.Timeout = 10
		}

		sessionID, err := sessionManager.CreateSession("ssh", req.Hostname, req.Port, req.Username, req.Password, req.KeyFile, req.Timeout)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"session_id": sessionID})
	})

	// SFTP эндпоинт
	router.POST("/connections/sftp", func(c *gin.Context) {
		var req struct {
			Hostname string `json:"hostname" binding:"required"`
			Port     int    `json:"port" binding:"omitempty"`
			Username string `json:"username" binding:"required"`
			Password string `json:"password"`
			KeyFile  string `json:"key_filename"`
			Timeout  int    `json:"timeout" binding:"omitempty"`
		}
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		if req.Port == 0 {
			req.Port = 22
		}
		if req.Timeout == 0 {
			req.Timeout = 10
		}

		sessionID, err := sessionManager.CreateSession("sftp", req.Hostname, req.Port, req.Username, req.Password, req.KeyFile, req.Timeout)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"session_id": sessionID})
	})

	// FTP эндпоинт
	router.POST("/connections/ftp", func(c *gin.Context) {
		var req struct {
			Hostname string `json:"hostname" binding:"required"`
			Port     int    `json:"port" binding:"omitempty"`
			Username string `json:"username" binding:"required"`
			Password string `json:"password" binding:"required"`
			Timeout  int    `json:"timeout" binding:"omitempty"`
		}
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		if req.Port == 0 {
			req.Port = 21
		}
		if req.Timeout == 0 {
			req.Timeout = 10
		}

		sessionID, err := sessionManager.CreateSession("ftp", req.Hostname, req.Port, req.Username, req.Password, "", req.Timeout)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"session_id": sessionID})
	})

	// Пример эндпоинта для выполнения команды
	router.POST("/session/:id/execute", func(c *gin.Context) {
		sessionID := c.Param("id")
		command := c.Query("command")
		if command == "" {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Не задана команда"})
			return
		}
		stdout, stderr, err := sessionManager.ExecuteCommand(sessionID, command)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{
			"stdout": stdout,
			"stderr": stderr,
		})
	})

	// Эндпоинт для закрытия сессии
	router.DELETE("/session/:id", func(c *gin.Context) {
		sessionID := c.Param("id")
		err := sessionManager.CloseSession(sessionID)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"message": "Сессия закрыта"})
	})

	// Запуск сервера на порту 8080
	router.Run(":8080")
}
