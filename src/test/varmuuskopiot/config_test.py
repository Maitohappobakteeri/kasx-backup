
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

        self.assertEqual(
            {
                ("somefile", "somefile", False),
                ("anotherone/withDeep/", "anotherone/withDeep/", True)
            },
            set(conf.fullCopyList)
        )

        self.assertEqual(
            {
                ("Documents", "Documents", False),
                ("Music", "Music", False),
                ("projects", "projects", False)
            },
            set(conf.oneCopyList)
        )

    def test_config_with_optional(self):
        with open(os.path.join(dir_, "test2.config")) as f:
            conf = Config(self.environment, f.read())

        self.assertEqual(
            {
                ("somefile", "somefile", False),
                ("anotherone", "anotherone", False),
                ("/big/whoop/magazine/0.mp3", "a/0.mp3", False),
                ("skripti", "xxx", False)
            },
            set(conf.fullCopyList)
        )

        self.assertEqual(
            {
                ("Documents", "Documents", False),
                ("Music", "Music", False),
                ("projects", "projects", False),
                ("cell.txt", "megacell", False)
            },
            set(conf.oneCopyList)
        )

    def test_config_abs_not_allowed_without_backup_name(self):
        def openConfig():
            with open(os.path.join(dir_, "test5.config")) as f:
                Config(self.environment, f.read())
        self.assertRaises(RuntimeError, openConfig)


if __name__ == '__main__':
    unittest.main()
