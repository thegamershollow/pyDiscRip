# pyDiscRip
Automate ripping optical discs and extracting data

## Usage

This program takes in a CSV as a parameter that holds data about what drive a media sample is in as well as a name and description.

## Errata

### FLAC + Musicbrainz

 - **Mixed Mode Discs:** A disc that has Data tracks mixed with Audio may return metadata that includes the data tracks. This currently causes off by 1 errors.
 - - A possible solution would be to look at a BINCUE data set and determine the index positions of Data tracks and skip those in the tagging step. There is no way to cleanly associate an ISO with a BINCUE though.