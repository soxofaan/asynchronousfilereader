
AsyncFileReader
===============

Simple thread based asynchronous file reader for Python.

Example use case:
you running a longer running child process with the `subprocess` module
and want to monitor its standard output and error along the way.
A tricky issue with this kind of parallel "flows" is the risk on deadlocks
if you are not careful with the order things are done.
For example, you want to read from the subprocess standard output pipe,
but the buffer of the standard error pipe is full
and the operating system wants you to read that first.
Kaboom, deadlock.

If it's ok to get the complete standard output and error content in one fell swoop,
the `communicate()` method, as recommended by the `subprocess.Popen` documentation, is the way to go.
However, if you want to monitor the streams line by line, you need other tricks.
On the web you can find many solutions, with varying degrees of complexity, abstraction and dependencies.

`AsynchronousFileReader` from `asyncfilereader.py` provides a simple solution
with limited code and no dependencies outside the standard library.
It reads the files or pipes line by line in separate threads (so one pipe can't block another)
and allows the main thread to fetch these lines as they become available.


Example/Demo
------------

The script `demo.py` provides an example of how to use it.
The script acts both as "child" process (producer mode) and monitoring process (consume mode).
Just run it without arguments and watch it go.


Features
--------

- supports both Python 2.x and 3.x
- simple, one file implementation
- only depends on standard library (`threading` and `Queue`)

