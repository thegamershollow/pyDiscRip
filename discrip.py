#!/usr/bin/env python3

# Python System 
import argparse
import csv
import json

# Hardware interfacing
import pyudev

from media_types.manager import MediaTypeManager
from media_types.media_type import Media

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
    """ Read a CSV with drive paths, BIN names, and full disc names

    """

    # Open CSV with media samples to rip
    discs=[]
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        for row in reader:
            discs.append(row)

    # Return a dict of disc information to rip
    return discs


def rip_disc(disc):
    """Determine disc type

    """

    # Access the drive associated to the media to determine the type
    disc["media_type"] = drive_media_type(disc["Drive"])

    # Init media manager
    media_manager = MediaTypeManager()

    # Get a media handler for this type of disc
    media_handler = media_manager.findMediaType(disc)

    # If a handler exists attempt to rip
    if media_handler is not None:
        # Rip media and store information about resulting data
        data_outputs = media_handler.rip(disc)
        # Add all data to the media object
        if data_outputs is not None:
            disc["data"]=[]
            disc["data_processed"]=0
            for data in data_outputs:
                disc["data"].append(data)

            # Begin processing data
            convert_data(disc)

    else:
        if disc["media_type"] is None:
            print("Error accessing drive or disc")
        else:
            print(f"Media type \"{disc["media_type"].value}\" not supported")

def convert_data(disc):
    """ Converts all possible data types until media sample if fully processed.

    """

    while disc["data_processed"] < len(disc["data"]):
        for data in disc["data"]:
            print(f"{data["data_id"].value}: {data["data_processed"]}")
            disc["data_processed"]+=1

def main():
    parser = argparse.ArgumentParser(
                    prog='pyDiscRip',
                    description='Disc ripping manager program',
                    epilog='By Shelby Jueden')
    parser.add_argument('-c', '--csv', help="CSV file in `Drive,Name,Description` format")
    parser.add_argument('-o', '--output', help="Directory to save data in")
    args = parser.parse_args()

    discs = rip_list_read(args.csv)
    rip_count = 1
    for disc in discs:
        rip_disc(disc)
        if rip_count < len(discs):
            rip_count+=1
            input("Change discs and press Enter to continue...")


if __name__ == "__main__":
    main()
