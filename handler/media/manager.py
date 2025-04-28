#!/usr/bin/env python3

# Media types
from handler.media.cd import MediaHandlerCD
from handler.media.dvd import MediaHandlerDVD
from handler.media.floppy import MediaHandlerFloppy
from handler.media.media_handler import Media

# Hardware interfacing
import pyudev

class MediaHandlerManager(object):

    def __init__(self):
        super().__init__()
        self.media_types={}
        self.media_types["CD"] = MediaHandlerCD()
        self.media_types["DVD"] = MediaHandlerDVD()
        self.media_types["Floppy"] = MediaHandlerFloppy()

    def findMediaType(self,media_sample):
        for media_id, media_type in self.media_types.items():
            if media_type.mediaMatch(media_sample):
                return media_type

        return None

    def configDump(self):
        config_options={}
        for media_id, media_type in self.media_types.items():
            config_options[media_id]=media_type.configOptions()

        return config_options


    def guess_media_type(self,drivepath=None):
        """ Guess media type in drive which will determine how it is ripped

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
