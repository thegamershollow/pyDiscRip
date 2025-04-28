#!/usr/bin/env python3

# DVD ripping module for pyDiscRip. Can be used to rip a DVD

# Python System
import os
import subprocess
import json
from pathlib import Path

# Internal Modules
from handler.media.media_handler import MediaHandler, Media
from handler.data.data_handler import Data


class MediaHandlerDVD(MediaHandler):
    """Handler for DVD media types

    rips using a subprocess command to run `ddrescue` to create an ISO file
    """

    def __init__(self):
        """Constructor to setup basic data and config defaults

        """
        # Call parent constructor
        super().__init__()
        # Set media type to handle
        self.type_id=Media.DVD
        # Data types output
        self.data_outputs=[Data.ISO9660]
        # DVD info to be collected
        self.dvd_partition_filesystem=""


    def ripDVD(self, media_sample):
        """Use ddrescue to rip DVD with multiple passes and mapfile

        """
        # TODO - Data is not always ISO9660, support for UDF is needed still
        data = {
            "type_id": Data.ISO9660,
            "processed_by": [],
            "data_dir":  self.ensureDir(f"{self.project_dir}/{Data.ISO9660.value}/{media_sample["Name"]}"),
            "data_files": {
                "ISO": [f"{media_sample["Name"]}.iso"]
            }
        }

        # Don't re-rip ISO
        if not os.path.exists(f"{data["data_dir"]}/{data["data_files"]["ISO"][0]}"):

            # ddrescue is a multi step process that is run three times
            cmd1 = f"ddrescue -b 2048 -n -v \"{media_sample["Drive"]}\" \"{data["data_dir"]}/{data["data_files"]["ISO"][0]}\" \"{data["data_dir"]}/mapfile\"  | tee -a ../$logs/dvd-ddrescue.log"
            cmd2 = f"ddrescue -b 2048 -d -r 3 -v \"{media_sample["Drive"]}\" \"{data["data_dir"]}/{data["data_files"]["ISO"][0]}\" \"{data["data_dir"]}/mapfile\"  | tee -a ../$logs/dvd-ddrescue.log"
            cmd3 = f"ddrescue -b 2048 -d -R -r 3 -v \"{media_sample["Drive"]}\" \"{data["data_dir"]}/{data["data_files"]["ISO"][0]}\" \"{data["data_dir"]}/mapfile\"  | tee -a ../$logs/dvd-ddrescue.log"

            try:
                # Run all ddrescue passes
                result = subprocess.run([cmd1], shell=True)
                result = subprocess.run([cmd2], shell=True)
                result = subprocess.run([cmd3], shell=True)

            except subprocess.CalledProcessError as exc:
                print("Status : FAIL", exc.returncode, exc.output)

        # Return all generated data
        return data


    def rip(self, media_sample):
        """Rip DVD with ddrescue

        """
        print("Ripping as DVD")
        print("WARNING: This software does not yet distinguish between ISO9660 and UDF filesystems")
        # Setup rip output path
        self.setProjectDir(media_sample["Name"])

        # Rip and return data
        return [self.ripDVD(media_sample)]

