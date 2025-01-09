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
                wavs = glob.glob(f"{data_wav["data_dir"]}/*.wav")
                if len(wavs) > 0:
                    data_wav["data_files"] = wavs

                isos = glob.glob(f"{data_wav["data_dir"]}/*.iso")
                if len(isos) > 0:
                    data_iso["data_files"] = wavs

                    for iso in isos:
                        os.rename(
                            iso,
                            f"{data_iso["data_dir"]}/{iso.replace(data_wav["data_dir"],"")}")

                return [data_wav,data_iso]

            except subprocess.CalledProcessError as exc:
                print("Status : FAIL", exc.returncode, exc.output)


    def convert(self, media_sample):
        print("Converting BINCUE to FLAC and ISO9660")

        self.setProjectDir(media_sample["Name"])

        # check if resulting ISO is UDF or ISO9660
        for data in media_sample["data"]:
            if data["data_id"] == self.data_id:
                data_outputs = self.convertBINCUE(data)

                if data_outputs is not None:
                    for data in data_outputs:
                        media_sample["data"].append(data)

        return media_sample
