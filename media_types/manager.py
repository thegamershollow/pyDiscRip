#!/usr/bin/env python3

# Media types
from media_types.cd import MediaTypeCD


class MediaTypeManager(object):

    def __init__(self):
        super().__init__()
        self.media_types={}
        self.media_types["CD"] = MediaTypeCD()

    def findMediaType(self,media_sample):
        for media_id, media_type in self.media_types.items():
            if media_type.mediaMatch(media_sample):
                return media_type

        return None


