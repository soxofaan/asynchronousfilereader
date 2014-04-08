import sys
import subprocess
import random
import time

from asynchronousfilereader import AsynchronousFileReader


def consume(command):
    """
    Example of how to consume standard output and standard error of
    a subprocess asynchronously without risk on deadlocking.
    """

    # Launch the command as subprocess.
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Launch the asynchronous readers of the process' stdout and stderr.
    stdout = AsynchronousFileReader(process.stdout, autostart=True)
    stderr = AsynchronousFileReader(process.stderr, autostart=True)

    # Check the readers if we received some output (until there is nothing more to get).
    while not stdout.eof() or not stderr.eof():
        # Show what we received from standard output.
        for line in stdout.readlines():
            print('Received line on standard output: ' + repr(line))

        # Show what we received from standard error.
        for line in stderr.readlines():
            print('Received line on standard error: ' + repr(line))

        # Sleep a bit before polling the readers again.
        time.sleep(.1)

    # Let's be tidy and join the threads we've started.
    stdout.join()
    stderr.join()

    # Close subprocess' file descriptors.
    process.stdout.close()
    process.stderr.close()


def produce(items=10):
    """
    Dummy function to randomly render a couple of lines
    on standard output and standard error.
    """
    streams = [('stdout', sys.stdout), ('stderr', sys.stderr)]
    for i in range(items):
        name, stream = random.choice(streams)
        stream.write('Line %d on %s\n' % (i, name))
        stream.flush()
        time.sleep(random.uniform(.1, 1))


if __name__ == '__main__':
    # The main flow:
    # if there is a command line argument 'produce', act as a producer
    # otherwise be a consumer (which launches a producer as subprocess).
    if len(sys.argv) == 2 and sys.argv[1] == 'produce':
        produce(10)
    else:
        consume([sys.executable, sys.argv[0], 'produce'])
