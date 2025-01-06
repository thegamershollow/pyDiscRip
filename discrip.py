#!/usr/bin/env python3

# Python System 
import argparse
import csv

# Hardware interfacing
import pyudev


def drive_media_type(drivepath=None):
    # Check media type in drive which will determine how it is ripped
    context = pyudev.Context()
    a = context.list_devices(sys_name=drivepath.replace("/dev/",""))
    dev = next(iter(a))
    # print(dev)
    # print(dict(dev.properties))
    media_type=None
    if dev.properties.get("ID_CDROM_MEDIA_CD", False):
        print("CD drive contains a CD")
        media_type="CD"
    elif dev.properties.get("ID_CDROM_MEDIA_DVD", False):
        print("CD drive contains a DVD")
        media_type="DVD"

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

    if disc["media_type"] == "CD":
        print("Rip as CD")

    if disc["media_type"] == "DVD":
        print("Rip as DVD")

def main():
    parser = argparse.ArgumentParser(
                    prog='pyDiscRip',
                    description='Disc ripping manager program',
                    epilog='By Shelby Jueden')
    parser.add_argument('-c', '--csv', help="CSV file in `Drive,Dir Name,Description` format")
    args = parser.parse_args()

    discs = rip_list_read(args.csv)
    for disc in discs:
        rip_disc(disc)

    print("disc ripper")




if __name__ == "__main__":
    main()
