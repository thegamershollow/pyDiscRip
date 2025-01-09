#!/usr/bin/env python3

import subprocess
import os
import glob
import json

import ffmpeg

from handler.data.data_handler import DataHandler, Data


class DataHandlerWAV(DataHandler):
    """API Base for signal emitters

    Manages loading API keys, logging, and registering signal recievers
    """

    def __init__(self):
        """Init with file path"""
        super().__init__()
        self.data_id=Data.WAV
        self.data_outputs=[Data.FLAC]

    def convertWAV(self,data,data_meta=None):

        # Write data
        tracks = None
        metadata = {}
        data_files = {}
        with open(f"{data_meta["data_dir"]}/{data_meta["data_files"]["JSON"]}", encoding="utf-8") as f:
            json_data = json.load(f)
            tracks = json_data["disc"]["release-list"][0]["medium-list"][0]["track-list"]

            metadata = {
                "metadata:g:1": f"artist={json_data["disc"]["release-list"][0]["artist-credit-phrase"]}",
                "metadata:g:2": f"album={json_data["disc"]["release-list"][0]["title"]}",
                "metadata:g:3": f"date={int(json_data["disc"]["release-list"][0]["date"][0:4])}"
            }

            data_files = {
                "data_id": Data.FLAC,
                "processed_by": [],
                "data_dir": f"{self.project_dir}/{Data.FLAC.value}/{self.cleanFilename(json_data["disc"]["release-list"][0]["artist-credit-phrase"])}/{json_data["disc"]["release-list"][0]["date"][0:4]} - {self.cleanFilename(json_data["disc"]["release-list"][0]["title"])}",
                "data_files": {
                    "FLAC": []
                }
            }

        # Make data_dir if not there
        if not os.path.exists(data_files["data_dir"]):
            os.makedirs(data_files["data_dir"])

        for i,v in enumerate(data["data_files"]["WAV"]):
            print(f"Working on: {data["data_files"]["WAV"][i]}: {self.cleanFilename(tracks[i]["recording"]["title"])}")

            metadata["metadata:g:0"] = f"title={tracks[i]["recording"]["title"]}"

            (ffmpeg
                .input(f"{data["data_dir"]}/{data["data_files"]["WAV"][i]}")
                .output(f"{data_files["data_dir"]}/{(i+1):02} - {self.cleanFilename(tracks[i]["recording"]["title"])}.flac", **metadata)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )

        flacs = glob.glob(f"{data_files["data_dir"]}/*.flac")
        if len(flacs) > 0:

            for flac in flacs:
                data_files["data_files"]["FLAC"].append(f"{flac.replace(data_files["data_dir"]+"/","")}")
        return data_files

    def convert(self, media_sample):

        self.setProjectDir(media_sample["Name"])

        # check if resulting ISO is UDF or ISO9660
        for data in media_sample["data"]:
            if data["data_id"] == self.data_id:
                if self.data_id not in data["processed_by"]:
                    print("Convert WAV to FLAC")
                    data_meta=None
                    for data_sup in media_sample["data"]:
                        if data_sup["data_id"] == Data.MUSICBRAINZ:
                            data_meta=data_sup

                    data_output = self.convertWAV(data, data_meta)



                    if data_output is not None:
                        data["processed_by"].append(self.data_id)
                        media_sample["data"].append(data_output)

        return media_sample
