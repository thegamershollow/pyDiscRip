#!/usr/bin/env python3

import sys, os
import json
from enum import Enum
from datetime import datetime

from handler.handler import Handler

class Media(Enum):
    CD="CD"
    DVD="DVD"

class MediaHandler(Handler):
    """Base class for Media Types to handle identification and ripping


    """

    def __init__(self):
        """Init"""

        super().__init__()
        self.media_id=None
        self.project_dir="./"
        self.project_timestamp=str(datetime.now().isoformat()).replace(":","-")
        self.data_outputs=[]


    def mediaMatch(self, media_sample=None):
        """Check if the media sample should be handled by this type"""
        return media_sample["media_type"] == self.media_id
