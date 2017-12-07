# source this file after a test to reset the env vars.

# remove temp files, before erasing the CGIBASHOPTS_DIR var
[ -n "$CGIBASHOPTS_DIR" ] && [ -d "$CGIBASHOPTS_DIR" ] && rm -rf "$CGIBASHOPTS_DIR"
# no need for the trap anymore
trap 0

# clean env vars
unset CGIBASHOPTS_VERSION FORMS FORMFILES FORMQUERY CGIBASHOPTS_DIR FORMQUERY
unset ${!FORM_*} ${!FORMFILE_*}

# clean CGI vars
unset REQUEST_METHOD CONTENT_TYPE QUERY_STRING
