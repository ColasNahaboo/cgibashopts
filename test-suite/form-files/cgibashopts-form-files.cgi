#!/bin/bash
export LANG=C
export nl=$'\n'
set -u

title="CGI BASH opts form file upload test"
header="Content-Type: text/html$nl$nl<html><head><title>$title</title>
</head><body>"
footer=""

################################# Options
export data=/tmp/cgibashopts-formfiletest.data
err() { echo "***ERROR: $*" >&2; exit -1; }

################################# Code
main() {
    local name
    cat >$data
    set >${data%.*}.vars
    name=$(head -40 $data|grep -A2 'Content-Disposition: form-data; name="testname"'|tail -1|sed -e 's/[^-._[:alnum:]]//g')
    [ -n "$name" ] && {
	cp $data /tmp/CBOgenf-$name.data
	cp ${data%.*}.vars /tmp/CBOgenf-$name.vars
    }
    main_page
}

main_page() {
    echo "$header$nl<h1>$title</h1><h2>Generate test data in $data</h2>
<form method=POST enctype='multipart/form-data'>
<ul>
<li><b>Save as name: <input type=text size=64 name=testname></b>
<li>Text: <input type=text size=64 name=text value='A sample string!'>
<li>Empty: <input type=text size=64 name=empty>
<li>Area: <textarea name=ta rows=3 cols=50>ta1
ta2
ta3</textarea>
<li>Select: <select name=sel>
  <option value=sel1>sel1</option>
  <option value=sel2>sel2</option>
  <option value=sel3 selected>sel3</option>
  <option value=sel4>sel4</option>
  </select>
<li>File1: <input type=file name=file1 size=32>
<li>File2: <input type=file name=file2 size=32>
<li>File3: <input type=file name=file3 size=32>
<li>File4: <input type=file name=file4 size=32>
<li>File5: <input type=file name=file5 size=32>
<li>Check: <input type=checkbox name=check checked>
</ul>
<input type=submit value=Submit> 
</form>"    
    echo "$footer"
}

main
