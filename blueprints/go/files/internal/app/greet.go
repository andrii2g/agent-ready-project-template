package app

import (
	"errors"
	"fmt"
	"strings"
)

// Greet returns a deterministic greeting for name.
func Greet(name string) (string, error) {
	normalized := strings.TrimSpace(name)
	if normalized == "" {
		return "", errors.New("name must not be empty")
	}
	return fmt.Sprintf("Hello, %s!", normalized), nil
}
