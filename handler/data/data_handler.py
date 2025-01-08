#!/usr/bin/env python3

import sys, os
import json
from enum import Enum
from datetime import datetime

from handler.handler import Handler

class Data(Enum):
    BINCUE="BINCUE"

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


    def log(self,action_name,text,json_output=False):
        """logging output for data"""
        log_path=f"{self.project_dir}/log"

        # Make log dir if not there
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        # Build filename
        if json_output:
            filepath=f"{log_path}/{self.project_timestamp}_{action_name}.json"
        else:
            filepath=f"{log_path}/{self.project_timestamp}_{action_name}.log"

        # Write data
        with open(filepath, 'w', encoding="utf-8") as output:
            if json_output:
                output.write(json.dumps(text, indent=4))
            else:
                output.write(text)

        return

    def rip(self, media_sample):
        print("Converting would happen here")


    def dataMatch(self, media_sample=None):
        """Check if the media sample should be handled by this type"""

        # will need to go through a list of data dicts to check them all
        media_sample

        return False
