# pyDiscRip
Automate ripping optical discs and extracting data

## Usage

```
usage: pyDiscRip [-h] [-c CSV] [-f CONFIG] [-d [CONFIGDUMP]] [-o OUTPUT]

Media ripping manager program

options:
  -h, --help            show this help message and exit
  -c, --csv CSV         CSV file in `Drive,Name,Description` format
  -f, --config CONFIG   Config file for ripping
  -d, --configdump [CONFIGDUMP]
                        Dump all config options. Optional filename to output to.
  -o, --output OUTPUT   Directory to save data in

By Shelby Jueden
```
### Rip List CSV
This program takes in a CSV as a parameter that holds data about what drive a media sample is in as well as a name and description. The CSV may optionally tell the software what format the media is if it is not an optical disc.

The headers for the CSV are almost all required, but the order is not critical. The headers is:
```
Drive,Name,Description,media_type
```

The header `media_type` is not required for optical discs, but is requried for other formats. Omitting the `media_type` header is the same as setting the `media_type` to `auto`.

#### Valid Media Types

- CD
- DVD
- Floppy

#### CSV Line Examples

- **Ripping a CD with automatic format detection:** `/dev/sr0, StAnger, Metallica - St. Anger`
- **Ripping a CD with manual format specification:** `CD, /dev/sr0, StAnger, Metallica - St. Anger`
- **Ripping a Floppy in Drive A with a Greaseweazle:** `floppy, a, doomsharev1.1_1-2, Doom Shareware v1.1 Disk 1 of 2`

### Config File

A Json configuration file may be used to change some parameters of the rip such as the `cdrdao` driver or the format the Greaseweazle `convert` function will use to decode flux. You can have all possible configuration values dumped to a file with the `-d` parameter, a filename may be specified to put them into.

## Roadmap

### Data: Virtal
A "virtual" data format should be possible to define within a config file. This would allow using tools not supported by the software during data conversion steps. Virtual formats may be possible as well but would be more unpredictable.

### Format: CD
 - Pre-gap detection and ripping (would be audio only so can go direct to WAV)

### Data: FLAC + Musicbrainz

 - **Mixed Mode Discs:** A disc that has Data tracks mixed with Audio may return metadata that includes the data tracks. This currently causes off by 1 errors.
 - - A possible solution would be to look at a BINCUE data set and determine the index positions of Data tracks and skip those in the tagging step. There is no way to cleanly associate an ISO with a BINCUE though.


