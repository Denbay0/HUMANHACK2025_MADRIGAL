// connections/connection.go
package connections

type Connection interface {
	Connect() error
	ExecuteCommand(command string) (string, string, error)
	Close() error
}
