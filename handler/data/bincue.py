#!/usr/bin/env python3

import subprocess
import os

from handler.data.data_handler import DataHandler, Data


class DataHandlerBINCUE(DataHandler):
    """API Base for signal emitters

    Manages loading API keys, logging, and registering signal recievers
    """

    def __init__(self):
        """Init with file path"""
        super().__init__()
        self.data_id=Data.BINCUE
        self.data_outputs=[Data.WAV,Data.ISO9660]


    def convertBINCUE(self,data_in):
        data_wav = {
            "data_id": Data.WAV,
            "data_dir": f"{self.project_dir}/{Data.WAV.value}/{data_in["data_files"]["BIN"].replace(".bin","")}",
            "data_files": {
                "WAV": "track01.wav"
            }
        }

        data_iso = {
            "data_id": Data.ISO9660,
            "data_dir": f"{self.project_dir}/{Data.ISO9660.value}/{data_in["data_files"]["BIN"].replace(".bin","")}",
            "data_files": {
                "ISO": "track01.iso"
            }
        }

        # Make data_dir if not there
        if not os.path.exists(data_wav["data_dir"]):
            os.makedirs(data_wav["data_dir"])

        # Don't re-convert CUE
        if not (
            os.path.exists(f"{data_wav["data_dir"]}/{data_wav["data_files"]["WAV"]}") or
            os.path.exists(f"{data_iso["data_dir"]}/{data_iso["data_files"]["ISO"]}")
            ):
            # Build toc2cue command to generate CUE
            cmd = f"bchunk -w {data_in["data_dir"]}/{data_in["data_files"]["BIN"]} {data_in["data_dir"]}/{data_in["data_files"]["CUE"]} {data_wav["data_dir"]}/track"

            try:
                result = subprocess.run([cmd], shell=True)
                if os.path.exists(f"{data_wav["data_dir"]}/{data_iso["data_files"]["ISO"]}"):
                    # Make data_dir if not there
                    if not os.path.exists(data_iso["data_dir"]):
                        os.makedirs(data_iso["data_dir"])
                    os.rename(
                        f"{data_wav["data_dir"]}/{data_iso["data_files"]["ISO"]}",
                        f"{data_iso["data_dir"]}/{data_iso["data_files"]["ISO"]}")


            except subprocess.CalledProcessError as exc:
                print("Status : FAIL", exc.returncode, exc.output)


    def convert(self, media_sample):
        print("Converting BINCUE to FLAC and ISO9660")

        self.setProjectDir(media_sample["Name"])

        # check if resulting ISO is UDF or ISO9660
        for data in media_sample["data"]:
            if data["data_id"] == self.data_id:
                print(f"Checking: {data["data_dir"]}/{data["data_files"]["BIN"]}")
                self.convertBINCUE(data)

        return media_sample
