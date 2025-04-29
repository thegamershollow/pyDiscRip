#!/usr/bin/env python3

# Base handler for pyDiscRip.

# Python System
import sys, os,re
import json
from enum import Enum
from datetime import datetime
import subprocess

# External Modules
import unidecode


class Handler(object):
    """Base handler for media and data samples


    """
    def __init__(self):
        """Constructor to setup basic data and config defaults

        """
        self.type_id=None # TODO - Genericize media and data IDs
        # Set directory to work in
        self.project_dir="./"
        # Get current datetime
        self.project_timestamp=str(datetime.now().isoformat()).replace(":","-")
        # Data types output for later use
        self.data_outputs=[]
        # Default config data
        self.config_data=None


    def cleanFilename(self, filename_raw):
        """Replace characters that are not available for filenames in some filesystems

        """
        return re.sub("[\\/\\\\\\&:\\\"<>\*|]","-", unidecode.unidecode(filename_raw))

    def setProjectDir(self,project_dir="./"):
        """Update project dir path

        """
        self.project_dir=project_dir

    def ensureDir(self,path):
        """Ensured that a path exists by attempting to create it or throwing an error

        """
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except Exception as e:
            print(f"Error making directory: {path}")
            sys.exit(1)
        return path

    def log(self,action_name,text,json_output=False):
        """Log data from processes

        Supports JSON as an output format

        """
        # Set filepath for log
        log_path=self.ensureDir(f"{self.project_dir}/log")

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
        """Set configuration data for handler by matching ID

        """
        # Check for config data for handler
        if self.type_id.value in config_data:
            # Iterate over all top level config values
            for key, value in config_data[self.type_id.value].items():
                # Set all config values
                self.config_data[key] = value


    def configOptions(self):
        """Return all configutation options"""

        return self.config_data

    def osRun(self, cmd):
        """Runs a command at the OS level and returns stdout and stderr"""
        try:
            # Run command and store output
            result = subprocess.run([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            return result

        except subprocess.CalledProcessError as exc:
            print("Status : FAIL", exc.returncode, exc.output)



