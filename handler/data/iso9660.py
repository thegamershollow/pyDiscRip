#!/usr/bin/env python3

# ISO9660 conversion module for pyDiscRip.

# Python System
import os
import glob
import json

# Internal Modules
from handler.data.data_handler import DataHandler


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
        self.type_id="ISO9660"
        # Data types output
        self.data_outputs=["Z_FILES"]


    def convertISO9660(self,data):
        """Use 7-zip to extract files out of ISO

        """

        # Go through all ISOs
        for iso in data["data_files"]["ISO"]:

            # Build data output files
            data_files = {
                "type_id": "Z_FILES",
                "processed_by": [],
                "data_dir": self.ensureDir(f"{data["data_dir"]}/{iso.replace(".iso","")}"),
                "data_files": {
                    "Z_FILES": f"{iso.replace(".iso","")}"
                }
            }

            print(f"Working on: {iso}")

            # Build 7z command to extract files
            cmd = f"7z -y x {data["data_dir"]}/{iso} -o{data_files["data_dir"]}"

            # Run command
            self.osRun(cmd)

            return data_files

        # Only returned if an error happens
        return None


    def convert(self, media_sample):
        """Take in ISO and convert to files

        """

        # Setup rip output path
        self.setProjectDir(media_sample["name"])

        # Go through all data in media sample
        for data in media_sample["data"]:
            # Check handler can work on data
            if data["type_id"] == self.type_id:
                # Check if handler has already worked on data
                if self.type_id not in data["processed_by"]:
                    # Convert data
                    print("Extract files from ISO9660 image")
                    data_output = self.convertISO9660(data)

                    if data_output is not None:
                        # Mark data as processed
                        data["processed_by"].append(self.type_id)
                        # Add new data to media sample
                        media_sample["data"].append(data_output)

        # Return media sample with new data
        return media_sample
