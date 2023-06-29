# easy-cp

```sh
easy-cp path/to/deep/dir/file newname
// equiv to `cp path/to/deep/file path/to/deep/dir/newname`
```

## example

Use with `fzf` in fish.

```fish
$ function cl
    set pathname (fzf --print0)
    set newname $argv[1]
    and easy-cp $pathname $newname
end

$ cl new.rs
```

