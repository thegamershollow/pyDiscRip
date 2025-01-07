#!/usr/bin/env python3

import json

class MediaType(object):
    """Base class for Media Types to handle identification and ripping


    """

    def __init__(self):
        """Init"""

        self.media_id=None


    def rip(self, media_sample):
        print("Ripping would happen here")


    def mediaMatch(self, media_sample=None):
        """Check if the media sample should be handled by this type"""

        if media_sample["media_type"] == self.media_id:
            print("Media type Match: "+self.media_id)
            return True

        return False
