# Cgibashopts: CGI BASH options parsing
Cgibashopts is a small and fast pure BASH library to parse web forms parameters for bash shell web CGI scripts, even with binary file uploads. It is free to use with no restrictions (MIT License).
(c) [Colas Nahaboo](http://colas.nahaboo.net) 2017

## Quickstart
- Copy the file `cgibashopts` somewhere on your server.
  E.g. as `/usr/local/bin/cgibashopts`
- Just source this file at the beginning of your CGI bash scripts.
  E.g: `source /usr/local/bin/cgibashopts` or 
  `. /usr/local/bin/cgibashopts`
- The value of a web form parameter `foo` (E.g. in the HTML page: `<input type=text name=foo>`) can then be found as the value of the shell environment variable `$FORM_foo`

Troubleshooting: if something goes wrong, run `tests/tewiba -v` in the cgibashopts directory on your server to see if the test suite detects a problem. I have tested cgibashopts only on "mainstream" full GNU+Linux distribs (Debian, Ubuntu...), it may not work on some more specialized linux systems such as busybox.

## Features
- Simple to use: just one file.
- Fast and small.
- Pure [bash](https://linux.die.net/man/1/bash) except for the use of [grep](https://linux.die.net/man/1/grep), [sed](https://linux.die.net/man/1/sed) and [truncate](https://linux.die.net/man/1/truncate).
- Handles GET and POST requests, with all the methods of encoding the parameters:    application/x-www-form-urlencoded,     multipart/form-data,     text/plain.
- Handles also the legacy index search query strings
- Handles upload of binary files, and text files with unix or DOS newlines. I did not find any existing library providing this functionality for CGI shell programming
- Uses only "classic" features of bash, and should work with old bash versions, I guess 4.1+

## Documentation
- When used, the cgibashopts library decodes the parameters sent by the browser that the web server provides to the scripts as various environment variables and optionally its standard input, as per the [CGI](https://en.wikipedia.org/wiki/Common_Gateway_Interface) standard. Cgibashopts makes them available to the including script in an easy to use form: variables, functions, and files.
- To use the library, source it at the start of your script, as early as possible to avoid conflicts with variables you could use later in your script.
- The library decodes the parameters of GET and POST requests, with all possible ways of encoding the parameters (via "enctype"). 
- The list of parameter names is listed in `$FORMS` as a space-separated string of names. E.g: `echo "$FORMS" ==> foo bar gee`. The parameter names are the one speciified by the `name` attribute in the various HTML elements in an HTML form, or sent via commands like `wget` or `curl`. Parameter names must be legal variable names for bash: alphanumeric characters and underscores, and not starting by a digit.
- Invalid parameter names (e.g: 0to60, a-b, a:b, ...) are silently ignored, as well as their values
- Each parameter value is copied as the value of a FORM_ - prefixed environment variable. E.g: `$FORM_foo` for an HTML form element named `foo`.
- Multi-line parameter values are converted to unix end of lines (a newline instead of carriage return and newline)
- **Files uploads:** When files are uploaded, via form elements like `<input type=file name=file1>`, cgibashopts places the parameter name (here `file1`) into the variable $FORMFILES, which is a space-separated list of all file parameter names received. The actual name of the uploaded file can be found in the variable value (here `$FORM_file1`), while the contents of the file can be found in a local file named by the variable in the `$CGIBASHOPTS_DIR` directory, (here `$CGIBASHOPTS_DIR/file1`)
  - Only actually uploaded files are created and listed this way. If the user does not select any file in the form, the shell variable will not be defined nor any file created.
  - Empty uploaded files will be created, however. They will be empty, of course.
  - Binary and text files received will **not** be converted in the unix text format (lines end with a newline), even if the client uploaded them in a DOS format (lines end with a carriage return and a newline). So you must be ready to handle dos lines in the uploaded text files.
  - **Warning:** A bash cleanup function `cgibashopts_clean` **must** be called at the end of your script to remove the temporary directory `$CGIBASHOPTS_DIR` storing the uploaded files, if the `-n` option (see below) is not used. Cgibashopts does a `trap cgibashopts_clean 0` so that this function will be called automatically at the end of your script, so you do not have to do anything, unless you use a `trap 0` yourself, and thus must ensure that your code handling the exit signal explicitely calls `cgibashopts_clean`.
    - sourcing cgibashopts will erase any `trap 0` that was done previously. So, set your trap 0 after sourcing cgibashopts
    - calling cgibashopts_clean is actually needed only if your html form use input elements of type `file`
    - as soon as you have process the uploaded files, you can explicitely call the `cgibashopts_clean` function yourself, so that it is not needed anymore and you are free to use traps as you wish afterwards
    - if you do not expect to have files uploaded, you can use the -n option (see below)
- **Command line options:**
  - **-n** can be given to ignore and discard any requests to upload files. This is recommended if you do not expect files to be uploaded, as it can save some computing load if some attacker try to upload fake files, but not mandatory. It also does not defines the variable `$CGIBASHOPTS_DIR` nor the function `cgibashopts_clean`, and do not use trap. **Note:** This is only available in versions 3 and above. Example of use : `. cgibashopts -n`
  - **-d directory** specifies where cgibashoptions will manage its temporary files in case of file uploads. It defaults to `/tmp`. cgibashoptions will create in it a `cgibashopts-files.$$` subdirectory (where `$$` is the bash process number, unique per instance), shown in the `$CGIBASHOPTS_DIR` variable.
- The variable `CGIBASHOPTS_RELEASE` holds the release version, uses [semantic versioning](https://semver.org/) (e.g. 4.0.1, 4.4.3) of the cgibashopts libray used, versions being listed at the end of this page in *History of changes*...
  - The variable `CGIBASHOPTS_VERSION` holds the major version number (the first integer of `CGIBASHOPTS_RELEASE`  above, for backwards compatibility.
- Misc goodies:
  - Two handy bash functions are provided: 
    - `urldecode` that takes a string in parameter and outputs its decoded version, transforming `+` in spaces and `%XX` in the character of hexadecimal ascii code XX (e.g %41 becomes A), and removing carriage returns. 
    - `urlencode` that performs the reverse operation. Both are faster than the binary linux commands.
  - two variables `$nl` and `$cr` hold a newline and a carriage return character
  - An alternate way to get the variables values is via the `param` function. This is just a convenience function compatible with [bashlib](http://bashlib.sourceforge.net/) for people (or scripts) used to it.
    - `param` without argument outputs the value of `FORMS` 
    - `param foo` outputs the value of `FORM_foo`
    - `param foo a string...` sets the value of `FORM_foo` to `"a string..."`
    - `param -f` prints `$FORMFILES`
    - `param -f foo` prints `$FORMFILE_foo`
    - `param -f foo a string...` sets the value of `FORMFILE_foo` to `"a string..."`

## Test suite
A test suite is provided, it can be run by `./tests/RUN-ALL-TESTS`, for more details see the README.md in directory `tests`

## Feedback
Feel welcome to copy and enhance this project, as well as providing bug reports, feedback, suggestions via:
- Creating [issues](https://gitreports.com/issue/ColasNahaboo/cgibashopts), if you have a GitHub account.
- Use the provided [Git Report Form](https://gitreports.com/issue/ColasNahaboo/cgibashopts) to create an issue if you do not have a GitHib account.
- Create or participate in a [Discussion](https://github.com/ColasNahaboo/cgibashopts/discussions) on this project
- Or just email me: colas@nahaboo.net

## History of changes
- 2021-12-23 v4.1.0
  - switched to semantic versioning, with new var `CGIBASHOPTS_RELEASE`
  - new -d option to specify the temporary directory (suggestion of "Aufschlauer")
  - move to GitHub: moved most files out of the main view, in tests/, tewiba upgraded to 1.5.0, code cleanup up to pass shellcheck
- 2020-04-16 Version 4: urlencode goodie function added
- 2020-04-04 Some cosmetic changes in this doc and the tests (test-suite dir renamed as tests), but no changes to cgibashopts code itself, so no version number increase.
- 2020-03-27 Version 3: -n option added to disable file uploads
- 2018-10-09 Version 2: fix, spaces in parameter values could be seen as +
- 2017-12-13 Version 1: fixes for upload of files with various mime-types, library can now be used in scripts using set -u and set -e.
- 2017-12-07 Creation of the project
