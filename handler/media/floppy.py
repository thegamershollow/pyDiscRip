#!/usr/bin/env python3

import os
import subprocess
import json
from pathlib import Path
import importlib
from pprint import pprint

from handler.media.media_handler import MediaHandler, Media
from handler.data.data_handler import Data


class MediaHandlerFloppy(MediaHandler):
    """API Base for signal emitters

    Manages loading API keys, logging, and registering signal recievers
    """

    def __init__(self):
        """Init with file path"""
        super().__init__()
        self.media_id=Media.Floppy
        self.config_data={
            "flux_output":"raw",
            "gw":{
                "revs": None,
                "tracks": None,
                "hard-sectors": None,
                "seek-retries": None,
                "pll": None,
                "densel": None,
                "reverse": None
                }
        }
        self.data_outputs=[Data.Flux]

    def ripToKryoFlux(self, media_sample):

        data = {}

        if self.config_data["flux_output"] == "raw":
            data = {
                "data_id": Data.Flux,
                "processed_by": [],
                "data_dir": f"{self.project_dir}/{Data.Flux.value}",
                "data_files": {
                    "flux": f"track00.0.raw"
                }
            }

        # Make data_dir if not there
        if not os.path.exists(data["data_dir"]):
            os.makedirs(data["data_dir"])

        mod = importlib.import_module('greaseweazle.tools.read')
        main = mod.__dict__['main']

        args=[]
        args.append("doesn't matter?")
        args.append("read")
        args.append("--drive")
        args.append(media_sample["Drive"])

        pprint(self.config_data)
        # Add config options
        if "revs" in self.config_data["gw"] and self.config_data["gw"]["revs"] is not None:
            args.append("--revs")
            args.append(str(self.config_data["gw"]["revs"]))
        if "tracks" in self.config_data["gw"] and self.config_data["gw"]["tracks"] is not None:
            args.append("--tracks")
            args.append(str(self.config_data["gw"]["tracks"]))
        if "seek-retries" in self.config_data["gw"] and self.config_data["gw"]["seek-retries"] is not None:
            args.append("--seek-retries")
            args.append(str(self.config_data["gw"]["seek-retries"]))
        if "pll" in self.config_data["gw"] and self.config_data["gw"]["pll"] is not None:
            args.append("--pll")
            args.append(self.config_data["gw"]["pll"])
        if "densel" in self.config_data["gw"] and self.config_data["gw"]["densel"] is not None:
            args.append("--densel")
            args.append(self.config_data["gw"]["densel"])
        if "hard-sectors" in self.config_data["gw"] and self.config_data["gw"]["hard-sectors"] is not None:
            args.append("--hard-sectors")
        if "reverse" in self.config_data["gw"] and self.config_data["gw"]["reverse"] is not None:
            args.append("--reverse")

        args.append(f"{data["data_dir"]}/{data["data_files"]["flux"]}")

        self.log("floppy_gw_args",args,json_output=True)

        res = main(args)

    def rip(self, media_sample):

        print("Temporary hard coded 80-Track")
        self.setProjectDir(media_sample["Name"])

        self.ripToKryoFlux(media_sample)

        return None


