import unittest

try:
    # Python 2
    from StringIO import StringIO
except ImportError:
    # Python 3
    from io import StringIO

from asynchronousfilereader import AsynchronousFileReader


class AsynchronousFileReaderTest(unittest.TestCase):
    def test_simple(self):
        file = StringIO('line1\nline2\n')
        reader = AsynchronousFileReader(file)
        lines = []
        while not reader.eof():
            for line in reader.readlines():
                lines.append(line)
        reader.join()

        self.assertEqual(['line1\n', 'line2\n'], lines)


if __name__ == '__main__':
    unittest.main()
