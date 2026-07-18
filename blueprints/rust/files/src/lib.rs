//! {{PROJECT_DESCRIPTION}}

/// Return a deterministic greeting for `name`.
///
/// # Errors
///
/// Returns an error when `name` contains only whitespace.
pub fn greet(name: &str) -> Result<String, &'static str> {
    let normalized = name.trim();
    if normalized.is_empty() {
        return Err("name must not be empty");
    }
    Ok(format!("Hello, {normalized}!"))
}
