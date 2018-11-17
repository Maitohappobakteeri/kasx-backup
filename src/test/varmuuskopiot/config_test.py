
from varmuuskopiot.environment import Environment
from varmuuskopiot.config import Config

import unittest
import os


dir_ = os.path.dirname(os.path.realpath(__file__))


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.environment = Environment()
        self.environment.hostname = "machineB"

    def test_simple_config(self):
        with open(os.path.join(dir_, "test1.config")) as f:
            conf = Config(self.environment, f.read())

        self.assertEqual({"somefile", "anotherone"}, set(conf.fullCopyList))

        self.assertEqual(
            {"Documents", "Music", "projects"},
            set(conf.oneCopyList)
        )

    def test_config_with_optional(self):
        with open(os.path.join(dir_, "test2.config")) as f:
            conf = Config(self.environment, f.read())

        self.assertEqual(
            {"somefile", "anotherone", "/big/whoop/magazine/0.mp3", "skripti"},
            set(conf.fullCopyList)
        )

        self.assertEqual(
            {"Documents", "Music", "projects", "cell.txt"},
            set(conf.oneCopyList)
        )


if __name__ == '__main__':
    unittest.main()
