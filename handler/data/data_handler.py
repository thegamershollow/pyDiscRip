#!/usr/bin/env python3

import sys, os
import json
from enum import Enum
from datetime import datetime

from handler.handler import Handler

class Data(Enum):
    BINCUE="BINCUE"
    MUSICBRAINZ="MUSICBRAINZ"
    WAV="WAV"
    FLAC="FLAC"
    ISO9660="ISO9660"
    Z_FILES="Z_FILES" # Special type for indeterminate files

class DataHandler(Handler):
    """Base class for Media Types to handle identification and ripping

    Data dict structure example:
{
    data_id: Data.BINCUE,
    data_dir: "some-folder",
    data_processed: False,
    data_files: {
        "BIN": name.bin,
        "cue": name.cue,
        "toc": name.toc
    }
}

    """

    def __init__(self):
        """Init"""

        super().__init__()
        self.data_id=None
        self.project_dir="."
        self.project_timestamp=str(datetime.now().isoformat()).replace(":","-")
        self.data_outputs=[]


    def dataMatch(self, data_sample=None):
        """Check if the data sample should be handled by this type"""
        return data_sample["data_id"] == self.data_id

