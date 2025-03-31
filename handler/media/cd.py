#!/usr/bin/env python3

import os
import subprocess
import json
from pathlib import Path

import libdiscid
import musicbrainzngs

from handler.media.media_handler import MediaHandler, Media
from handler.data.data_handler import Data


class MediaHandlerCD(MediaHandler):
    """API Base for signal emitters

    Manages loading API keys, logging, and registering signal recievers
    """

    def __init__(self):
        """Init with file path"""
        super().__init__()
        self.media_id=Media.CD
        self.cd_sessions=0
        self.cd_tracks=0
        self.config_data={
            "cdrdao_driver":"generic-mmc-raw:0x20000"
        }
        self.data_outputs=[Data.BINCUE,Data.MUSICBRAINZ]

    def countSessions(self,media_sample):
# Sample output
# cdrdao disk-info --device  /dev/sr1
# Cdrdao version 1.2.4 - (C) Andreas Mueller <andreas@daneb.de>
# /dev/sr1: HL-DT-ST BD-RE WP50NB40       Rev: 1.03
# Using driver: Generic SCSI-3/MMC - Version 2.0 (options 0x0000)
#
# That data below may not reflect the real status of the inserted medium
# if a simulation run was performed before. Reload the medium in this case.
#
# CD-RW                : no
# Total Capacity       : n/a
# CD-R medium          : n/a
# Recording Speed      : n/a
# CD-R empty           : no
# Toc Type             : CD-DA or CD-ROM
# Sessions             : 2
# Last Track           : 23
# Appendable           : no
        cmd = f"cdrdao disk-info --device {media_sample["Drive"]}"

        try:
            result = subprocess.run([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        except subprocess.CalledProcessError as exc:
            print("Status : FAIL", exc.returncode, exc.output)
        else:
            self.log("cdrdao-disk-info",result.stdout.decode("utf-8"))
            self.cd_sessions=int(result.stdout.decode("utf-8").split("Sessions             : ")[1][:1])
            print(f"Sessions Found: {self.cd_sessions}")


    def ripBinCue(self, media_sample):

        print("Begin rip")
        datas=[]
        sessions = 1
        while sessions <= self.cd_sessions:
            print(f"Rip session: {sessions}")
            data = {
                "data_id": Data.BINCUE,
                "processed_by": [],
                "data_dir": f"{self.project_dir}/{Data.BINCUE.value}/{media_sample["Name"]}-S{sessions}",
                "data_files": {
                    "BIN": f"{media_sample["Name"]}-S{sessions}.bin",
                    "CUE": f"{media_sample["Name"]}-S{sessions}.cue",
                    "TOC": f"{media_sample["Name"]}-S{sessions}.toc"
                }
            }

            # Make data_dir if not there
            if not os.path.exists(data["data_dir"]):
                os.makedirs(data["data_dir"])

            # Don't re-rip BIN/TOC
            if not os.path.exists(f"{data["data_dir"]}/{data["data_files"]["BIN"]}"):
                # Build cdrdao command to read CD
                cmd = f"cdrdao read-cd --read-raw --datafile \"{data["data_dir"]}/{data["data_files"]["BIN"]}\" --device \"{media_sample["Drive"]}\" --session \"{sessions}\"  --driver {self.config_data["cdrdao_driver"]} \"{data["data_dir"]}/{data["data_files"]["TOC"]}\""

                self.log("cmd",cmd)
                try:
                    result = subprocess.run([cmd], shell=True)

                except subprocess.CalledProcessError as exc:
                    print("Status : FAIL", exc.returncode, exc.output)


            # Don't re-convert CUE
            if not os.path.exists(f"{data["data_dir"]}/{data["data_files"]["CUE"]}"):
                # Build toc2cue command to generate CUE
                cmd = f"toc2cue \"{data["data_dir"]}/{data["data_files"]["TOC"]}\" \"{data["data_dir"]}/{data["data_files"]["CUE"]}\""

                try:
                    result = subprocess.run([cmd], shell=True)

                except subprocess.CalledProcessError as exc:
                    print("Status : FAIL", exc.returncode, exc.output)

            sessions += 1
            datas.append(data)

        return datas

    def fetchMetadata(self,media_sample):
        data = {
            "data_id": Data.MUSICBRAINZ,
            "processed_by": [],
            "data_dir": f"{self.project_dir}/{Data.MUSICBRAINZ.value}",
            "data_files": {
                "JSON": f"{media_sample["Name"]}-musicbrainz.json"
            }
        }

        # Make data_dir if not there
        if not os.path.exists(data["data_dir"]):
            os.makedirs(data["data_dir"])

        if not os.path.exists(f"{data["data_dir"]}/{data["data_files"]["JSON"]}"):
            # https://python-discid.readthedocs.io/en/latest/usage/#fetching-metadata
            musicbrainzngs.set_useragent("AkBKukU: pyDiscRip", "0.1", "akbkuku@akbkuku.com")

            try:
                disc = libdiscid.read(device=media_sample["Drive"])
                self.log("disc.id",disc.id)
            except libdiscid.exceptions.DiscError:
                print("no actual audio tracks on disc: CDROM or DVD?")
                return None
            try:
                result = musicbrainzngs.get_releases_by_discid(disc.id,
                                                            includes=["artists", "recordings"])
            except musicbrainzngs.ResponseError:
                print("disc not found or bad response")
            else:
                if result.get("disc"):
                    #self.log("mb-disc",result,json_output=True)
                    print("artist:\t%s" %
                        result["disc"]["release-list"][0]["artist-credit-phrase"])
                    print(result["disc"]["release-list"][0])
                    print("title:\t%s" % result["disc"]["release-list"][0]["title"])

                    # Write data
                    with open(f"{data["data_dir"]}/{data["data_files"]["JSON"]}", 'w', encoding="utf-8") as output:
                        output.write(json.dumps(result, indent=4))

                elif result.get("cdstub"):
                    self.log("mb-cdstub",result,json_output=True)
                    print("artist:\t" % result["cdstub"]["artist"])
                    print("title:\t" % result["cdstub"]["title"])
                    print("----------------------CONGRATS!----------------------")
                    print("You just found a cdstub entry which I couldn't find a sample of how to use. If you are not me, please make an issue on github and attatch the json log file that was just saved. For now this software cannot handle that data and you will have to do manual tagging.")
                    input("Press Enter to continue...")
                    return None
                return data
        return data

    def rip(self, media_sample):
        print("Ripping as CD")
        datas=[]
        self.setProjectDir(media_sample["Name"])
        self.countSessions(media_sample)
        data_output = self.fetchMetadata(media_sample)

        if data_output is not None:
                datas.append(data_output)

        data_outputs = self.ripBinCue(media_sample)

        if data_outputs is not None:
            for data in data_outputs:
                datas.append(data)

        return datas


