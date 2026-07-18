package app

import "testing"

func TestGreet(t *testing.T) {
	t.Parallel()

	got, err := Greet(" Ada ")
	if err != nil {
		t.Fatalf("Greet returned an error: %v", err)
	}
	if want := "Hello, Ada!"; got != want {
		t.Fatalf("Greet() = %q, want %q", got, want)
	}
}

func TestGreetRejectsEmptyName(t *testing.T) {
	t.Parallel()

	if _, err := Greet("   "); err == nil {
		t.Fatal("Greet accepted an empty name")
	}
}
