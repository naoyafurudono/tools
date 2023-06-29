use std::{fs, path::PathBuf};

use crate::Args;

pub enum Cmd {
    Copy {
        from_path: PathBuf,
        base_name: String,
        overwrite: bool,
    },
}

impl Cmd {
    pub fn new(args: &Args) -> Result<Self, String> {
        let from_path = PathBuf::from(&args.from_path);
        let base_name = args.base_name.clone();
        Ok(Cmd::Copy {
            from_path,
            base_name,
            overwrite: args.force,
        })
    }

    pub fn run(&self) -> Result<(), String> {
        match self {
            Cmd::Copy {
                from_path,
                base_name,
                overwrite,
            } => {
                let mut to = from_path.clone();
                to.set_file_name(base_name);
                let from = PathBuf::from(from_path);
                if !from.exists() {
                    return Err(format!(
                        "{} does not exist",
                        from_path.to_str().ok_or("internal error")?
                    ));
                }
                if !overwrite && to.exists() {
                    return Err(format!("{} already exists", to.to_str().ok_or("internal error")?));
                }
                fs::copy(from, to).map_err(|e| e.to_string())?;
                Ok(())
            }
        }
    }
}
