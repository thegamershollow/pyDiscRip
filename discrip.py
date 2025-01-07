#!/usr/bin/env python3

# Python System 
import argparse
import csv

# Hardware interfacing
import pyudev

from media_types.manager import MediaTypeManager

def drive_media_type(drivepath=None):
    # Check media type in drive which will determine how it is ripped
    context = pyudev.Context()
    a = context.list_devices(sys_name=drivepath.replace("/dev/",""))
    dev = next(iter(a))
    media_type=None
    if "ID_CDROM_MEDIA_CD" in dev:
        media_type="CD"
    elif "ID_CDROM_MEDIA_DVD" in dev:
        media_type="DVD"
    elif "ID_CDROM_MEDIA_BD" in dev:
        media_type="BD"

    return media_type

def rip_list_read(filepath=None):
    # Read a CSV with drive paths, BIN names, and full disc names

    discs=[]

    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            discs.append(row)
    # Return a dict of disc information to rip
    return discs

def rip_disc(disc=None):
    # Determine disc type
    disc["media_type"] = drive_media_type(disc["Drive"])
    media_manager = MediaTypeManager()

    media_handler = media_manager.findMediaType(disc)

    media_handler.rip(disc)


def main():
    parser = argparse.ArgumentParser(
                    prog='pyDiscRip',
                    description='Disc ripping manager program',
                    epilog='By Shelby Jueden')
    parser.add_argument('-c', '--csv', help="CSV file in `Drive,Name,Description` format")
    parser.add_argument('-o', '--output', help="Directory to save data in")
    args = parser.parse_args()

    discs = rip_list_read(args.csv)
    for disc in discs:
        rip_disc(disc)
        input("Change discs and press Enter to continue...")

if __name__ == "__main__":
    main()
