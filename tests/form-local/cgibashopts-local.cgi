#!/bin/bash
set -u
set -e
. cgibashopts

title="CGI BASH opts upload test on a local host"
header="Content-Type: text/html$nl$nl<html><head><title>$title</title>
</head><body><h1>$title</h1>"
footer=""

################################# Options
export data=/tmp/cgibashopts-formfiletest.data
err() { echo "***ERROR: $*" >&2; exit -1; }

################################# Code
main() {
    echo "$header"
    if [ -n "${FORM_file:-}" ]; then
	src="/tmp/${FORM_file##*/}"
	[ "$FORMFILES" = file ] || echo "<p>***Error, FORMFILES=$FORMFILES</p>"
	if [ -e "$CGIBASHOPTS_DIR/file" ]; then
	    if [ -s "$CGIBASHOPTS_DIR/file" ]; then
		if [ -s "$src" ]; then
		    if cmp -s "$src" "$CGIBASHOPTS_DIR/file"; then
			echo "<p>Upload of $src successful</p>"
		    else
			echo "<p>***Error, file uploaded differ</p>"
		    fi
		else
		    echo "<p>***Error, src file empty</p>"
		fi
	    else
		echo "<p>***Error, file uploaded empty</p>"
	    fi
	else
	    echo "<p>***Error no uploaded file!</p>"
	fi
    fi
    form_page
}

form_page() {
    echo "<form method=POST enctype='multipart/form-data'>
<br>File: <input type=file name=file size=32>
<br><input type=submit value=Upload> 
</form>"    
    echo "$footer"
}

main
