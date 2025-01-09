#!/usr/bin/env python3

# Media types
from handler.data.data_handler import Data

from handler.data.bincue import DataHandlerBINCUE
from handler.data.iso9660 import DataHandlerISO9660
from handler.data.wav import DataHandlerWAV

class DataHandlerManager(object):

    def __init__(self):
        super().__init__()
        self.data_types={}
        self.data_types["BINCUE"] = DataHandlerBINCUE()
        self.data_types["ISO9660"] = DataHandlerISO9660()
        self.data_types["WAV"] = DataHandlerWAV()

    def findDataType(self,data):

        for data_id, data_handler in self.data_types.items():
            if data_handler.dataMatch(data):
                return data_handler

        return None


