use std::process;

use clap::Parser;
use cmd::Cmd;

mod cmd;

#[derive(Parser)]
#[command(name = "cl")]
#[command(author = "Naoya Furudono <naoyafurudono@gmail.com>")]
#[command(about = "rich cp", long_about = None)]
pub struct Args {
    from_path: String,
    base_name: String,
    #[clap(short, long)]
    force: bool
}

fn main() {
    let args = Args::parse();
    match Cmd::new(&args).and_then(|c| c.run()) {
        Ok(_) => process::exit(0),
        Err(e) => {
            eprintln!("{}", e);
            process::exit(1)
        }
    }
}
