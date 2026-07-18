use {{PACKAGE_NAME}}::greet;

#[test]
fn normalizes_surrounding_whitespace() {
    assert_eq!(greet(" Ada "), Ok("Hello, Ada!".to_owned()));
}

#[test]
fn rejects_empty_name() {
    assert!(greet("   ").is_err());
}
