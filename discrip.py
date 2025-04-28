#!/usr/bin/env python3

# Python System 
import argparse
import csv
import json
import sys
from pprint import pprint

# Hardware interfacing
import pyudev

from handler.media.manager import MediaHandlerManager
from handler.data.manager import DataHandlerManager
from handler.media.media_handler import Media
from handler.data.data_handler import Data


def rip_list_read(filepath=None):
    """ Read a CSV with drive paths, BIN names, and full media_sample names

    """

    # Open CSV with media samples to rip
    media_samples=[]
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        for row in reader:
            media_samples.append(row)

    # Return a dict of media_sample information to rip
    return media_samples


def config_read(filepath=None):
    """ Read a JSON with config parameters for media and data handlers

    """

    # Open JSON to read config data
    config_data={}
    with open(filepath, newline='') as jsonfile:
        config_data = json.load(jsonfile)

    # Return a dict of config data
    return config_data


def rip_media_sample(media_sample,config_data):
    """Determine media_sample type

    """

    # Init media manager
    media_manager = MediaHandlerManager()

    # Access the drive associated to the media to determine the type
    if "media_type" not in media_sample or media_sample["media_type"] == "auto":
        print("Finding media type")
        media_sample["media_type"] = media_manager.guess_media_type(media_sample["Drive"])


    # Get a media handler for this type of media_sample
    media_handler = media_manager.findMediaType(media_sample)


    # If a handler exists attempt to rip
    if media_handler is not None:
        # Setup config
        media_handler.config(config_data)
        # Rip media and store information about resulting data
        data_outputs = media_handler.rip(media_sample)
        # Add all data to the media object
        if data_outputs is not None:
            media_sample["data"]=[]
            for data in data_outputs:
                media_sample["data"].append(data)

            # Begin processing data
            convert_data(media_sample,config_data)

    else:
        if media_sample["media_type"] is None:
            print("Error accessing drive or media_sample")
            pprint(media_sample)
        else:
            print(f"Media type \"{media_sample["media_type"].value}\" not supported")


def convert_data(media_sample,config_data):
    """ Converts all possible data types until media sample if fully processed.

    """

    # Init media manager
    data_manager = DataHandlerManager()

    # Setup config
    data_processed=0
    while data_processed < len(media_sample["data"]):
        data_processed = len(media_sample["data"])
        for data in media_sample["data"]:
            # Get a media handler for this type of media_sample
            data_handler = data_manager.findDataType(data)

            # If a handler exists attempt to rip
            if data_handler is not None:
                # Setup config
                data_handler.config(config_data)
                # Pass entire media sample to converter to support conversion using multiple data sources at once
                media_sample = data_handler.convert(media_sample)

            else:
                print(f"No data handler found for [{data["data_id"].value}]")


def main():
    parser = argparse.ArgumentParser(
                    prog='pyDiscRip',
                    description='Disc ripping manager program',
                    epilog='By Shelby Jueden')
    parser.add_argument('-c', '--csv', help="CSV file in `Drive,Name,Description` format", default=None)
    parser.add_argument('-f', '--config', help="Config file for ripping",default=None)
    parser.add_argument('-o', '--output', help="Directory to save data in")
    args = parser.parse_args()

    if args.csv == "":
        print("Drive, Name, Description")
        sys.exit(0)

    media_samples = rip_list_read(args.csv)
    if args.config is not None:
        config_data = config_read(args.config)
    else:
        config_data = {}
    rip_count = 1
    for media_sample in media_samples:
        rip_media_sample(media_sample,config_data)
        if rip_count < len(media_samples):
            rip_count+=1
            input("Change media_samples and press Enter to continue...")


if __name__ == "__main__":
    main()
