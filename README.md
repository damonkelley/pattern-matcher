# pattern-matching-paths
Warby Parker Programming Test

### Requirements

Python 3.x

### Usage

The script will read from stdin and write to stdout. If it encounters an error, a message will be written to stderr.

There are 2 ways to run the script.

#####  Option 1: Install the package and expose the `entry_point` command.

```sh
$ python[3] setup.py install

$ cat foo.txt | pattern-matcher > bar.txt
```

##### Option 2: Use the shell script.

```sh
$ cat foo.txt | ./bin/pattern-matcher > bar.txt
```

**Note**: The script will look for the `python3` binary in the current environment.


### Running the Tests

```sh
$ python[3] setup.py test
```



