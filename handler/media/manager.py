#!/usr/bin/env python3

# Media types
from handler.media.cd import MediaHandlerCD
from handler.media.dvd import MediaHandlerDVD


class MediaHandlerManager(object):

    def __init__(self):
        super().__init__()
        self.media_types={}
        self.media_types["CD"] = MediaHandlerCD()
        self.media_types["DVD"] = MediaHandlerDVD()

    def findMediaType(self,media_sample):
        for media_id, media_type in self.media_types.items():
            if media_type.mediaMatch(media_sample):
                return media_type

        return None


