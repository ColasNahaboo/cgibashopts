# Cgibashopts test suite
This is a test suite of the cgibashopts library, using [tewiba](http://colas.nahaboo.net/Software/Tewiba) (included)

Just run `RUN-ALL-TESTS.sh` to run all the tests silently. No output means everything is OK. Use `RUN-ALL-TESTS.sh -v` for verbose mode. Each set of tests is in a `*.test` file, that can be also run individually:

- `query-string.test` tests the GET mode, using a query string for arguments
- `form.test` replays saved data for test in POST mode
- `form-files.test` replays saved data for testing file uploads

`clearenv.sh` is a script to source before (or after) each test to clean all the results of an invocation of cgibashopts, to enable performing multiple tests in the same file.

## Manual tests
- **form-local/** tests manually the uploads of files through a real browser and web server on your local machine