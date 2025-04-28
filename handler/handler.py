#!/usr/bin/env python3

import sys, os,re
import json
from enum import Enum
from datetime import datetime

import unidecode

class Handler(object):
    """Base class for Media and Data Types to handle identification data
    manipulation


    """

    def __init__(self):
        """Init"""

        self.media_id=None
        self.project_dir="./"
        self.project_timestamp=str(datetime.now().isoformat()).replace(":","-")
        self.data_outputs=[]
        self.config_data=None

    def cleanFilename(self, filename_raw):
        return re.sub("[\\/\\\\\\&:\\\"<>\?\*|]","-", unidecode.unidecode(filename_raw))

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

    def config(self, config_data):
        """Receive configutation data for the rip"""

        if self.media_id in config_data:
            print(config_data[self.media_id])
            for key, value in config_data[self.media_id].items():
                print(f"{key}: {value}")
                self.config_data[key] = value


    def configOptions(self):
        """Return all configutation options"""

        return self.config_data





