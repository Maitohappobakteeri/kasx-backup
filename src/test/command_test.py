
from varmuuskopiot.environment import Environment
from varmuuskopiot.config import Config
from varmuuskopiot.backup import dateFormat as dateFormat
from varmuuskopiot import backup
import komento as command

import unittest
import os
import datetime


dir_ = os.path.dirname(os.path.realpath(__file__))


class MockBackup:
    def __init__(self, path):
        self.path_ = path

    def path(self):
        return self.path_


class CommandTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.environment = Environment()
        self.environment.hostname = "machineB"
        self.environment.date = datetime.datetime.strptime(
            "2011_11_12_21_20_00",
            dateFormat
        )

    def test_backup_commands(self):
        with open(os.path.join(dir_, "test3.config")) as f:
            conf = Config(self.environment, f.read())

        commands = command.create_backup_commands(
            self.environment,
            conf,
            MockBackup("/home/someone"),
            MockBackup("/mnt/somedev/kasx/"),
            False
        )

        with open(os.path.join(dir_, "test3-backup.txt")) as f:
            expectedCommands = f.read().rstrip()

        self.assertEqual(expectedCommands, "\n".join(commands))

    def test_sync_commands(self):
        with open(os.path.join(dir_, "test3.config")) as f:
            conf = Config(self.environment, f.read())

        commands = command.create_sync_commands(
            self.environment,
            conf,
            MockBackup("/home/someone"),
            MockBackup("/mnt/somedev/kasx/"),
            self.environment.date.strftime(backup.dateFormat),
            False
        )

        with open(os.path.join(dir_, "test3-sync.txt")) as f:
            expectedCommands = f.read().rstrip()

        self.assertEqual(expectedCommands, "\n".join(commands))


if __name__ == '__main__':
    unittest.main()
