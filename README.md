srtCleaner-addic7ed
==========

Clean _Addic7ed_ info from `srt` files downloaded from [Addic7ed.com](http://www.addic7ed.com/index.php).

#### Requirements
* Python2.7
* argparse
* traceback

#### Usage
```
usage: srtCleaner-addic7ed [-h] [--version] [-d] [-r] [-n] [-v] [-s] srt

Clean "Addic7ed" from srt files.

positional arguments:
  srt         Parse input.

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
  -d          Specify a Directory to clean all the srt files within.
  -r          Recursively parse directories. Used with "-d".
  -n          Run in test mode. Do not save output.
  -v          Run in Verbose mode. Outputs extra information.
  -s          Run Silently. Squash all output including errors.
```
