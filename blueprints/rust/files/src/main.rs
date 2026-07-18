use std::env;
use std::process::ExitCode;

fn main() -> ExitCode {
    let name = env::args().nth(1).unwrap_or_else(|| "world".to_owned());
    match {{PACKAGE_NAME}}::greet(&name) {
        Ok(message) => {
            println!("{message}");
            ExitCode::SUCCESS
        }
        Err(message) => {
            eprintln!("{message}");
            ExitCode::from(2)
        }
    }
}
