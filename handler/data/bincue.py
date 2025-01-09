#!/usr/bin/env python3

import subprocess
import os
import glob
import json

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
            "processed_by": [],
            "data_dir": f"{self.project_dir}/{Data.WAV.value}/{data_in["data_files"]["BIN"].replace(".bin","")}",
            "data_files": {
                "WAV": []
            }
        }

        data_iso = {
            "data_id": Data.ISO9660,
            "processed_by": [],
            "data_dir": f"{self.project_dir}/{Data.ISO9660.value}/{data_in["data_files"]["BIN"].replace(".bin","")}",
            "data_files": {
                "ISO": []
            }
        }

        # Make data_dir if not there
        if not os.path.exists(data_wav["data_dir"]):
            os.makedirs(data_wav["data_dir"])
        # Make data_dir if not there
        if not os.path.exists(data_iso["data_dir"]):
            os.makedirs(data_iso["data_dir"])

        # Don't re-convert CUE
        wavs = glob.glob(f"{data_wav["data_dir"]}/*.wav")
        isos = glob.glob(f"{data_iso["data_dir"]}/*.iso")


        if len(wavs) == 0 and len(isos) == 0 :
            # Build toc2cue command to generate CUE
            cmd = f"bchunk -w {data_in["data_dir"]}/{data_in["data_files"]["BIN"]} {data_in["data_dir"]}/{data_in["data_files"]["CUE"]} {data_wav["data_dir"]}/track"

            try:
                result = subprocess.run([cmd], shell=True)

            except subprocess.CalledProcessError as exc:
                print("Status : FAIL", exc.returncode, exc.output)


        wavs = glob.glob(f"{data_wav["data_dir"]}/*.wav")
        if len(wavs) > 0:

            for wav in wavs:
                data_wav["data_files"]["WAV"].append(f"{wav.replace(data_wav["data_dir"],"")}")

        isos = glob.glob(f"{data_wav["data_dir"]}/*.iso") + glob.glob(f"{data_iso["data_dir"]}/*.iso")
        if len(isos) > 0:

            for iso in isos:
                print(f"Working on: {iso}")
                data_iso["data_files"]["ISO"].append(f"{iso.replace(data_wav["data_dir"],"")}")
                if "WAV" in iso:
                    os.rename(
                        iso,
                        f"{data_iso["data_dir"]}/{iso.replace(data_wav["data_dir"],"")}")

        return [data_wav,data_iso]


    def convert(self, media_sample):

        self.setProjectDir(media_sample["Name"])

        # check if resulting ISO is UDF or ISO9660
        for data in media_sample["data"]:
            if data["data_id"] == self.data_id:
                if self.data_id not in data["processed_by"]:
                    print("Converting BINCUE to FLAC and ISO9660")
                    data_outputs = self.convertBINCUE(data)

                    if data_outputs is not None:
                        data["processed_by"].append(self.data_id)
                        for data_new in data_outputs:
                            media_sample["data"].append(data_new)

        return media_sample
