#!/usr/bin/env python3

# Media ripping manager for pyDiscRip. Can be used to rip a CD and fetch metadata

# External Modules
import pyudev

# Internal Modules
from handler.media.cd import MediaHandlerCD
from handler.media.dvd import MediaHandlerDVD
from handler.media.floppy import MediaHandlerFloppy
from handler.media.media_handler import Media


class MediaHandlerManager(object):
    """Manager for media types

    Provides process control functions for ripping different media types and
    setting configuration data.
    """

    def __init__(self):
        """Constructor to setup basic data and config defaults

        """
        # Call parent constructor
        super().__init__()

        # Add all supported media types
        self.media_types={}
        self.media_types["CD"] = MediaHandlerCD()
        self.media_types["DVD"] = MediaHandlerDVD()
        self.media_types["Floppy"] = MediaHandlerFloppy()


    def findMediaType(self,media_sample):
        """Match media handler to type and return handler

        """

        # Iterate through all handlers
        for type_id, media_type in self.media_types.items():
            # If handler can proccess media return it
            if media_type.mediaMatch(media_sample):
                return media_type

        # No handlers found
        return None


    def configDump(self):
        """Get all config data for media handlers and dump it to json

        """
        config_options={}
        # Iterate through all handlers
        for type_id, media_type in self.media_types.items():
            # Add all config options for handler
            config_options[type_id]=media_type.configOptions()

        return config_options


    def guessMediaType(self,drivepath=None):
        """ Guess media type in drive which will determine how it is ripped

        Only useful for optical discs.
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

