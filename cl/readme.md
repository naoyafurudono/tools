# easy-cp

```
cl src/deep/path/to/original-file new-file-name

Usage: easy-cp <FROM_PATH> <BASE_NAME>

Arguments:
  <FROM_PATH>  
  <BASE_NAME>  

Options:
  -h, --help  Print help
```

## example

Use with `fzf` in fish.

```fish
$ function cl
    set pathname (fzf --print0)
    and set newname $argv[1]
    and easy-cp $pathname $newname
end

$ cl new.rs
```

