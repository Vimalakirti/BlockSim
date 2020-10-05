#!/bin/bash

function join_by {
    local IFS="$1"; shift
    echo "$*"
}

function join_by_comma {
    join_by , $@
}
