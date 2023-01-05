#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Arity mismatch. want: 2, actual: $#" 1>&2
  exit 1
fi

git grep -lE "$1" | xargs sed -i -E "s/$1/$2/g"
