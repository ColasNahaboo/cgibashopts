# Local file upload interactive test
To use this test:
- copy cgibashopts-local.cgi and cgibashopts into a place in your local web server where .cgi files are executed as cgi
- place the various files to test the upload of in `/tmp`
- open cgibashopts-local.cgi in your browser, e.g: http://localhost/cgi-bin/cgibashopts-local.cgi
- upload them via the web page: On each upload of a file, the script will compare the uploaded copy to its source in /tmp and display the result

This is a (semi-)manual test, but exercising a real web server and browser.