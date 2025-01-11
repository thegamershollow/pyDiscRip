#!/usr/bin/env python3

import os
import subprocess
import json
from pathlib import Path

from handler.media.media_handler import MediaHandler, Media
from handler.data.data_handler import Data


class MediaHandlerDVD(MediaHandler):
    """API Base for signal emitters

    Manages loading API keys, logging, and registering signal recievers
    """

    def __init__(self):
        """Init with file path"""
        super().__init__()
        self.media_id=Media.DVD
        self.dvd_partition_filesystem=""
        self.data_outputs=[Data.ISO9660]

    def ripDVD(self, media_sample):
        data = {
            "data_id": Data.ISO9660,
            "processed_by": [],
            "data_dir": f"{self.project_dir}/{Data.ISO9660.value}/{media_sample["Name"]}",
            "data_files": {
                "ISO": [f"{media_sample["Name"]}.iso"]
            }
        }

        if not os.path.exists(f"{data["data_dir"]}/{data["data_files"]["ISO"][0]}"):
            # Make data_dir if not there
            if not os.path.exists(data["data_dir"]):
                os.makedirs(data["data_dir"])

            cmd1 = f"ddrescue -b 2048 -n -v \"{media_sample["Drive"]}\" \"{data["data_dir"]}/{data["data_files"]["ISO"][0]}\" \"{data["data_dir"]}/mapfile\"  | tee -a ../$logs/dvd-ddrescue.log"
            cmd2 = f"ddrescue -b 2048 -d -r 3 -v \"{media_sample["Drive"]}\" \"{data["data_dir"]}/{data["data_files"]["ISO"][0]}\" \"{data["data_dir"]}/mapfile\"  | tee -a ../$logs/dvd-ddrescue.log"
            cmd3 = f"ddrescue -b 2048 -d -R -r 3 -v \"{media_sample["Drive"]}\" \"{data["data_dir"]}/{data["data_files"]["ISO"][0]}\" \"{data["data_dir"]}/mapfile\"  | tee -a ../$logs/dvd-ddrescue.log"

            try:
                result = subprocess.run([cmd1], shell=True)
                result = subprocess.run([cmd2], shell=True)
                result = subprocess.run([cmd3], shell=True)

            except subprocess.CalledProcessError as exc:
                print("Status : FAIL", exc.returncode, exc.output)

        return data


    def rip(self, media_sample):
        print("Ripping as DVD")
        # Wrap ddrescue in subprocess
        self.setProjectDir(media_sample["Name"])

        # check if resulting ISO is UDF or ISO9660
        return [self.ripDVD(media_sample)]



