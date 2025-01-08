#!/usr/bin/env python3

import sys, os
import json
from enum import Enum
from datetime import datetime

from handler.handler import Handler

class Media(Enum):
    CD="CD"
    DVD="DVD"

class MediaHandler(Handler):
    """Base class for Media Types to handle identification and ripping


    """

    def __init__(self):
        """Init"""

        super().__init__()
        self.media_id=None
        self.project_dir="./"
        self.project_timestamp=str(datetime.now().isoformat()).replace(":","-")
        self.data_outputs=[]

    def setProjectDir(self,project_dir="./"):
        self.project_dir=project_dir

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
        print("Ripping would happen here")


    def mediaMatch(self, media_sample=None):
        """Check if the media sample should be handled by this type"""

        if media_sample["media_type"] == self.media_id:
            print("Media type Match: "+self.media_id.value)
            return True

        return False
