package main

import (
	"fmt"
	"os"

	"github.com/{{OWNER}}/{{PROJECT_SLUG}}/internal/app"
)

func main() {
	name := "world"
	if len(os.Args) > 1 {
		name = os.Args[1]
	}
	message, err := app.Greet(name)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
	fmt.Println(message)
}
