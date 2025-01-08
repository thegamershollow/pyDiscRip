#!/usr/bin/env python3

import subprocess

from handler.media.media_handler import MediaHandler


class MediaHandlerDVD(MediaHandler):
    """API Base for signal emitters

    Manages loading API keys, logging, and registering signal recievers
    """

    def __init__(self):
        """Init with file path"""
        super().__init__()
        self.media_id="DVD"
        self.dvd_partition_filesystem=""

    def rip(self, media_sample):
        print("Ripping as DVD")
        # Wrap ddrescue in subprocess

        # check if resulting ISO is UDF or ISO9660
