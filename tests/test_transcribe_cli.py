import os
import tempfile
import unittest
from unittest import mock


class TestCLI(unittest.TestCase):
    def test_output_file_written(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            outfile = os.path.join(tmpdir, "out.txt")
            with mock.patch("transcribe.transcribe_audio", return_value="hello"):
                from transcribe import main

                self.assertEqual(
                    main(["dummy.wav", "-o", outfile]),
                    0,
                )
            with open(outfile, "r", encoding="utf-8") as fh:
                self.assertEqual(fh.read(), "hello")


if __name__ == "__main__":
    unittest.main()
