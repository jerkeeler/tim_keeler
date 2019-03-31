import os
import stat
from logging import handlers


class GroupWriteRotatingFileHandler(handlers.RotatingFileHandler):
    def doRollover(self):
        """
        Override base class method to make the new log file group writable.
        """
        # Rotate the file first.
        super().doRollover()

        # Add group write to the current permissions.
        cur_mode = os.stat(self.baseFilename).st_mode
        os.chmod(self.baseFilename, cur_mode | stat.S_IWGRP)
