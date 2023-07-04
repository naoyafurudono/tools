# easy-cp

[![crates.io](https://img.shields.io/crates/v/easy-cp.svg)](https://crates.io/crates/easy-cp)

```
a rich cp

Usage: easy-cp [OPTIONS] <FROM_PATH> <BASE_NAME>

Arguments:
  <FROM_PATH>  
  <BASE_NAME>  

Options:
  -f, --force  
  -h, --help   Print help
```

## example

Use with `fzf` in fish.

```fish
$ function cl
    set pathname (fzf --print0)
    and set newname [1]
    and easy-cp  
end

$ cl new.rs
```

