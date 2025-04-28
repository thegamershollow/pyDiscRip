#!/usr/bin/env python3

# ISO9660 conversion module for pyDiscRip.

# Python System
import subprocess
import os
import glob
import json

# Internal Modules
from handler.data.data_handler import DataHandler, Data


class DataHandlerISO9660(DataHandler):
    """Handler for BINCUE data types

    Extracts files using 7zip
    """

    def __init__(self):
        """Constructor to setup basic data and config defaults

        """
        # Call parent constructor
        super().__init__()
        # Set data type to handle
        self.data_id=Data.ISO9660
        # Data types output
        self.data_outputs=[Data.Z_FILES]


    def convertISO9660(self,data):
        """Use 7-zip to extract files out of ISO

        """

        # Go through all ISOs
        for iso in data["data_files"]["ISO"]:

            # Build data output files
            data_files = {
                "data_id": Data.Z_FILES,
                "processed_by": [],
                "data_dir": self.ensureDir(f"{data["data_dir"]}/{iso.replace(".iso","")}"),
                "data_files": {
                    "Z_FILES": f"{iso.replace(".iso","")}"
                }
            }

            print(f"Working on: {iso}")

            # Build 7z command to extract files
            cmd = f"7z -y x {data["data_dir"]}/{iso} -o{data_files["data_dir"]}"

            try:
                # Run 7z command
                result = subprocess.run([cmd], shell=True)
                # Returns data if there was no error
                return data_files

            except subprocess.CalledProcessError as exc:
                print("Status : FAIL", exc.returncode, exc.output)

        # Only returned if an error happens
        return None


    def convert(self, media_sample):
        """Take in ISO and convert to files

        """

        # Setup rip output path
        self.setProjectDir(media_sample["Name"])

        # Go through all data in media sample
        for data in media_sample["data"]:
            # Check handler can work on data
            if data["data_id"] == self.data_id:
                # Check if handler has already worked on data
                if self.data_id not in data["processed_by"]:
                    # Convert data
                    print("Extract files from ISO9660 image")
                    data_output = self.convertISO9660(data)

                    if data_output is not None:
                        # Mark data as processed
                        data["processed_by"].append(self.data_id)
                        # Add new data to media sample
                        media_sample["data"].append(data_output)

        # Return media sample with new data
        return media_sample
