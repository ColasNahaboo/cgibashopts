#!/bin/bash
# runs all the tests in this directory
# Options: -v for verbose mode
#          -? for help

# Sanity check: stop immediately if we have a syntax error in the lib
bash -n ../cgibashopts || { 
     echo "***ABRTING: syntax errors in cgibashopts" >&2; exit 1
}

# otherwise, run all the *.test files in this dir in alphabetical order

PATH=$PWD:$PATH

for i in $(grep -ls '^#!/bin/bash' *); do 
    if ! bash -n "$i"; then
        echo "************ Syntax errors in test file $i!" >&2
        exit 1
    fi
done

. clearenv.sh  # clean env

for test in *.test; do
    [ "$test" != "*.test" ] && tewiba $* "$test"
done
