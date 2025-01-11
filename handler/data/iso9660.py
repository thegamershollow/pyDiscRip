#!/usr/bin/env python3

import subprocess
import os
import glob
import json

from handler.data.data_handler import DataHandler, Data


class DataHandlerISO9660(DataHandler):
    """API Base for signal emitters

    Manages loading API keys, logging, and registering signal recievers
    """

    def __init__(self):
        """Init with file path"""
        super().__init__()
        self.data_id=Data.ISO9660
        self.data_outputs=[Data.Z_FILES]

    def convertISO9660(self,data):
        # 7z -y x ../"$isoname".iso
        for iso in data["data_files"]["ISO"]:

            data_files = {
                "data_id": Data.Z_FILES,
                "processed_by": [],
                "data_dir": f"{data["data_dir"]}/{iso.replace(".iso","")}",
                "data_files": {
                    "Z_FILES": f"{iso.replace(".iso","")}"
                }
            }

            # Make data_dir if not there
            if not os.path.exists(data_files["data_dir"]):
                os.makedirs(data_files["data_dir"])

            print(f"Working on: {iso}")

            # Build 7z command to extract files
            cmd = f"7z -y x {data["data_dir"]}/{iso} -o{data_files["data_dir"]}"

            try:
                result = subprocess.run([cmd], shell=True)
                return data_files

            except subprocess.CalledProcessError as exc:
                print("Status : FAIL", exc.returncode, exc.output)


        return None

    def convert(self, media_sample):

        self.setProjectDir(media_sample["Name"])

        # check if resulting ISO is UDF or ISO9660
        for data in media_sample["data"]:
            if data["data_id"] == self.data_id:
                if self.data_id not in data["processed_by"]:
                    print("Extract files from ISO9660 image")
                    data_output = self.convertISO9660(data)

                    if data_output is not None:
                        data["processed_by"].append(self.data_id)
                        media_sample["data"].append(data_output)

        return media_sample
