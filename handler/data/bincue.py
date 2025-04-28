#!/usr/bin/env python3

# BINCUE conversion module for pyDiscRip.

# Python System
import subprocess
import os
import glob
import sys
import json

# Internal Modules
from handler.data.data_handler import DataHandler, Data


class DataHandlerBINCUE(DataHandler):
    """Handler for BINCUE data types

    Extracts files using bchunk
    """

    def __init__(self):
        """Constructor to setup basic data and config defaults

        """
        # Call parent constructor
        super().__init__()
        # Set data type to handle
        self.type_id=Data.BINCUE
        # Data types output
        self.data_outputs=[Data.WAV,Data.ISO9660]


    def convertBINCUE(self,data_in):
        """Use bchunk to extract all WAVs and ISOs from BINCUE

        """
        # Build data output for WAV
        data_wav = {
            "type_id": Data.WAV,
            "processed_by": [],
            "data_dir": self.ensureDir(f"{self.project_dir}/{Data.WAV.value}/{data_in["data_files"]["BIN"].replace(".bin","")}"),
            "data_files": {
                "WAV": []
            }
        }

        # Build data output ISO
        data_iso = {
            "type_id": Data.ISO9660,
            "processed_by": [],
            "data_dir": self.ensureDir(f"{self.project_dir}/{Data.ISO9660.value}/{data_in["data_files"]["BIN"].replace(".bin","")}"),
            "data_files": {
                "ISO": []
            }
        }

        # Check for files in ouput directory
        wavs = glob.glob(f"{data_wav["data_dir"]}/*.wav")
        isos = glob.glob(f"{data_iso["data_dir"]}/*.iso")

        # Don't re-convert if files exist
        if len(wavs) == 0 and len(isos) == 0 :
            # Build bchunk command to generate CUE
            cmd = f"bchunk -w {data_in["data_dir"]}/{data_in["data_files"]["BIN"]} {data_in["data_dir"]}/{data_in["data_files"]["CUE"]} {data_wav["data_dir"]}/track"

            try:
                # Run bchunk command
                result = subprocess.run([cmd], shell=True)

            except subprocess.CalledProcessError as exc:
                print("Status : FAIL", exc.returncode, exc.output)


        # Get files in ouput directory
        wavs = glob.glob(f"{data_wav["data_dir"]}/*.wav")
        # Sort wavs to have file order make sense
        wavs.sort()

        #  Build data output if WAVs were converted
        if len(wavs) > 0:

            # Add file paths to data output for all WAVs
            for wav in wavs:
                print(f"Working on: {wav}")
                data_wav["data_files"]["WAV"].append(f"{wav.replace(data_wav["data_dir"]+"/","")}")

        #  Build data output if ISOs were converted
        isos = glob.glob(f"{data_wav["data_dir"]}/*.iso") + glob.glob(f"{data_iso["data_dir"]}/*.iso")
        if len(isos) > 0:

            # Add file paths to data output for all ISOs
            for iso in isos:
                print(f"Working on: {iso}")
                # The file paths get weird, this is a fix for it
                if "WAV" in iso:
                    os.rename(
                        iso,
                        f"{data_iso["data_dir"]}/{iso.replace(data_wav["data_dir"]+"/","")}")
                    iso = f"{data_iso["data_dir"]}/{iso.replace(data_wav["data_dir"]+"/","")}"
                data_iso["data_files"]["ISO"].append(f"{iso.replace(data_iso["data_dir"]+"/","")}")

        # Clear WAV data if no WAVs were created
        if len(wavs) == 0:
            data_wav = None

        # Clear ISO data if no ISOs were created
        if len(isos) == 0:
            data_iso = None

        # Return all generated data
        return [data_wav,data_iso]


    def convert(self, media_sample):
        """Take in BINCUE and convert to WAVs and ISOs

        """

        # Setup rip output path
        self.setProjectDir(media_sample["Name"])

        # Go through all data in media sample
        for data in media_sample["data"]:
            # Check handler can work on data
            if data["type_id"] == self.type_id:
                # Check if handler has already worked on data
                if self.type_id not in data["processed_by"]:
                    # Convert data
                    print("Converting BINCUE to FLAC and ISO9660")
                    data_outputs = self.convertBINCUE(data)

                    if data_outputs is not None:
                        # Mark data as processed
                        data["processed_by"].append(self.type_id)
                        # Add new data to media sample
                        for data_new in data_outputs:
                            if data_new is not None:
                                media_sample["data"].append(data_new)

        # Return media sample with new data
        return media_sample
