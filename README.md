# pydupes

## Overview

[pydupes](https://github.com/clarkcb/pydupes) is a command-line file duplicates finder that is
based on / inspired by [fdupes](https://github.com/adrianlopezroche/fdupes), but with a number of
key differences. It uses the python version of [xfind](https://github.com/clarkcb/xfind)
as a dependency for the file finding functionality.

For the features that `pydupes` and `fdupes` have in common, the results should be the same,
except that `pydupes` will order the output from smallest to largest file sizes. Also, `pydupes`
will not display a progress bar during the file duplicates searching.

At the time of this writing, no benchmarking has been done to compare performance of `pydupes`
and `fdupes`. It does seem that `fdupes` is faster than `pydupes`, though not dramatically so,
and the ability to filter files by extension, path and filename can limit the files being
compared, which should give `pydupes` a performance advantage.

## Features

Currently, `pydupes` has the following features in common with `fdupes`:

* find (optionally recursively) and group duplicate files found under one or more given directories
* specify a mix of directories to recurse into and not recurse into
* include only files greater than minsize and/or less than maxsize
* include or exclude empty files
* include or exclude hidden files
* show file sizes
* show file modification times
* summarize file duplicate info
* order duplicate file sets by mtime, ctime or name
* reverse file order
* display version info

Here are `fdupes` features that `pydupes` does *not* currently support:

* show/hide progress bar during duplicates searching
* delete and related functionality
  * plain
  * noprompt
  * immediate
  * log
* exclude duplicates with different owner/group or permissions

Finally, here are features that are unique to `pydupes`:

* order file duplicate sets by size ascending
* provide extensions of files to include and/or exclude
* provide regexes of directory paths of files to include and/or exclude
* provide regexes of names of files to include and/or exclude
* provide types of files to include and/or exclude (archive, binary, code, text, xml)

One other thing to mention is that the help output and some of the error
messages differ between `pydupes` and `fdupes`.

## Installation

The following requirements are necessary to install and run `pydupes`:

* Python 3.9.x
* git clone of [xfind](https://github.com/clarkcb/xfind)
* git clone of [pydupes](https://github.com/clarkcb/pydupes)

The clone of `xfind` is necessary because `pydupes` has `pyfind` (the python version of `xfind`)
as a dependency for the file-finding functionality, and as of this writing `pyfind` has not
yet been published to PyPI. These instructions will be revised once that has happened.

Once you have satisfied the requirements, change into the _pydupes_ directory and install the
project's dependencies. It is recommended to use a virtual environment (skip if you want to
install to the system _site-packages_ directory for the Python 3.9.x version):

```sh
$ python3.9 -m venv venv
$ . ./venv/bin/activate
```

Next, install the dependencies listed in the _requirements.txt_ file:

```sh
$ (venv) pip3.9 install -r requirements.txt
```

Finally, install the `pyfind` dependency (`$XFIND_PATH` indicates the root directory to where
`xfind` has been cloned):

```sh
$ (venv) pip3.9 install $XFIND_PATH/python/pyfind
```

You should now be able to run `pydupes`. The executable is in the _bin_ directory. Try this
command to verify:

```sh
$ (venv) ./bin/pydupes -h
```

You should get the help message.

## Usage

As mentioned before, for the features that `pydupes` and `fdupes` have in common, the results
should match. No deletion options are (currently) available in `pydupes`, and filtering
files by extension, path and filename are unique to `pydupes`.

The following example looks for duplicate files under two directories using the following
criteria:

* search all directories recursively (`-r`)
* show the file size of each duplicate file set in resulting output (`-S`)
* show the modification time of each file in the duplicate sets (`-t`)
* include only files that have the `py` file extension
* exclude paths that contain `vendor`
* search under `$PYDUPES_PATH` (the root directory where `pydupes` was cloned)
* also search under `$XFIND_PATH` (the root directory where `xfind` was cloned)

The full command with partial sample output:

```sh
$ pydupes -rSt -x py -D vendor $PYDUPES_PATH $XFIND_PATH/python/pyfind
. . .
7779 bytes each:
2021-05-06 10:43 $PYDUPES_PATH/venv/lib/python3.9/site-packages/pyfind/finder.py
2021-05-06 10:43 $XFIND_PATH/python/pyfind/pyfind/finder.py
. . .
```

To get only summary information for the found duplicates from the previous command,
try this:

```sh
$ pydupes -rm -x py -D vendor $PYDUPES_PATH $XFIND_PATH/python/pyfind
189 duplicate files (in 179 sets), occupying 1.9 megabytes
```

To see what other options are available, use the help option:

```sh
$ pydupes -h
```

## License

This project is licensed under the MIT license. See the [LICENSE](LICENSE) file for more info.
