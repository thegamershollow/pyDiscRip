#!/usr/bin/env python3

import subprocess

from media_types.media_type import MediaType


class MediaTypeCD(MediaType):
    """API Base for signal emitters

    Manages loading API keys, logging, and registering signal recievers
    """

    def __init__(self):
        """Init with file path"""
        super().__init__()
        self.media_id="CD"
        self.cd_sessions=0
        self.cd_tracks=0

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
            self.cd_sessions=int(str(result.stdout).split("Sessions             : ")[1][:1])
            print(f"Sessions Found: {self.cd_sessions}")


    def ripBinCue(self, media_sample):


        sessions = 1
        while sessions <= self.cd_sessions:

            cmd = f"cdrdao read-cd --read-raw --datafile \"{media_sample["Name"]}-{sessions}\".bin --device \"{media_sample["Drive"]}\" --session \"{sessions}\"  \"{media_sample["Name"]}-{sessions}\".toc"

            try:
                result = subprocess.run([cmd], shell=True)

            except subprocess.CalledProcessError as exc:
                print("Status : FAIL", exc.returncode, exc.output)


            cmd = f"toc2cue \"{media_sample["Name"]}-{sessions}\".toc \"{media_sample["Name"]}-{sessions}\".cue"

            try:
                result = subprocess.run([cmd], shell=True)

            except subprocess.CalledProcessError as exc:
                print("Status : FAIL", exc.returncode, exc.output)

            sessions += 1

    def fetchMetadata(self,media_sample):
        # https://python-discid.readthedocs.io/en/latest/usage/#fetching-metadata
        return

    def rip(self, media_sample):
        print("Ripping as CD")
        self.countSessions(media_sample)
        self.ripBinCue(media_sample)


