
from varmuuskopiot.config import Config

import unittest
import os


dir_ = os.path.dirname(os.path.realpath(__file__))


class ConfigTest(unittest.TestCase):

    def test_simple_config(self):
        with open(os.path.join(dir_, "test1.config")) as f:
            conf = Config(f.read())

        self.assertEqual({"somefile", "anotherone"}, set(conf.fullCopyList))

        self.assertEqual(
            {"Documents", "Music", "projects"},
            set(conf.oneCopyList)
        )

    def test_config_with_optional(self):
        def test_simple_config(self):
            with open(os.path.join(dir_, "test2.config")) as f:
                conf = Config(f.read())

            self.assertEqual(
                {"somefile", "anotherone"},
                set(conf.fullCopyList)
            )

            self.assertEqual(
                {"Documents", "Music", "projects"},
                set(conf.oneCopyList)
            )


if __name__ == '__main__':
    unittest.main()
