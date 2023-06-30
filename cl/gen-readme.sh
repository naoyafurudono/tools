#!/bin/bash

export HELP=`cargo run -- -h`
envsubst < readme.md.template > readme.md

