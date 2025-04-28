#!/usr/bin/env python3

# Data conversion manager for pyDiscRip. Can be used to rip a CD and fetch metadata

# Internal Modules
from handler.data.data_handler import Data
from handler.data.bincue import DataHandlerBINCUE
from handler.data.iso9660 import DataHandlerISO9660
from handler.data.wav import DataHandlerWAV


class DataHandlerManager(object):
    """Manager for data types

    Provides process control functions for converting different data types and
    setting configuration data.
    """

    def __init__(self):
        """Constructor to setup basic data and config defaults

        """
        # Call parent constructor
        super().__init__()
        # Add all supported data types
        self.data_types={}
        self.data_types["BINCUE"] = DataHandlerBINCUE()
        self.data_types["ISO9660"] = DataHandlerISO9660()
        self.data_types["WAV"] = DataHandlerWAV()


    def findDataType(self,data):
        """Match data handler to type and return handler

        """

        # Iterate through all handlers
        for data_id, data_handler in self.data_types.items():
            if data_handler.dataMatch(data):
                return data_handler

        return None


    def configDump(self):
        """Get all config data for media handlers and dump it to json

        """
        config_options={}
        # Iterate through all handlers
        for data_id, data_handler in self.data_types.items():
            # Add all config options for handler
            config_options[data_id]=data_handler.configOptions()

        return config_options

