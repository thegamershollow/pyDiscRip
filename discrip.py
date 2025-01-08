#!/usr/bin/env python3

# Python System 
import argparse
import csv
import json

# Hardware interfacing
import pyudev

from handler.media.manager import MediaHandlerManager
from handler.media.media_handler import Media

def drive_media_type(drivepath=None):
    """ Check media type in drive which will determine how it is ripped

    """

    # Init udev interface to access drive
    context = pyudev.Context()

    # Get info from device
    # NOTE: Returns as list but we are accessing a specific device
    for dev in context.list_devices(sys_name=drivepath.replace("/dev/","")):
        #print(json.dumps(dict(dev.properties),indent=4))
        # Determine media type by ID
        if "ID_CDROM_MEDIA_CD" in dev:
            media_type=Media.CD
        elif "ID_CDROM_MEDIA_DVD" in dev:
            media_type=Media.DVD
            print("Is DVD")
        elif "ID_CDROM_MEDIA_BD" in dev:
            media_type="BD"
        else:
            media_type=None

    return media_type


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


def rip_media_sample(media_sample):
    """Determine media_sample type

    """

    # Access the drive associated to the media to determine the type
    media_sample["media_type"] = drive_media_type(media_sample["Drive"])

    # Init media manager
    media_manager = MediaHandlerManager()

    # Get a media handler for this type of media_sample
    media_handler = media_manager.findMediaType(media_sample)

    # If a handler exists attempt to rip
    if media_handler is not None:
        # Rip media and store information about resulting data
        data_outputs = media_handler.rip(media_sample)
        # Add all data to the media object
        if data_outputs is not None:
            media_sample["data"]=[]
            media_sample["data_processed"]=0
            for data in data_outputs:
                media_sample["data"].append(data)

            # Begin processing data
            convert_data(media_sample)

    else:
        if media_sample["media_type"] is None:
            print("Error accessing drive or media_sample")
        else:
            print(f"Media type \"{media_sample["media_type"].value}\" not supported")

def convert_data(media_sample):
    """ Converts all possible data types until media sample if fully processed.

    """

    while media_sample["data_processed"] < len(media_sample["data"]):
        for data in media_sample["data"]:
            print(f"{data["data_id"].value}: {data["data_processed"]}")
            media_sample["data_processed"]+=1

def main():
    parser = argparse.ArgumentParser(
                    prog='pyDiscRip',
                    description='Disc ripping manager program',
                    epilog='By Shelby Jueden')
    parser.add_argument('-c', '--csv', help="CSV file in `Drive,Name,Description` format")
    parser.add_argument('-o', '--output', help="Directory to save data in")
    args = parser.parse_args()

    media_samples = rip_list_read(args.csv)
    rip_count = 1
    for media_sample in media_samples:
        rip_media_sample(media_sample)
        if rip_count < len(media_samples):
            rip_count+=1
            input("Change media_samples and press Enter to continue...")


if __name__ == "__main__":
    main()
