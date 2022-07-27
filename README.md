# bin2png

**forked from [foone/bin2png](https://github.com/foone/bin2png)**

The changes may seem important, but in fact they are not. I've just slightly modify the code to use advanced arguments with [argparse](https://docs.python.org/3/library/argparse.html) (and added small options).

```
bin2png.py [-h] [-s SIZE] [-d OUTPUT_DIR] [-n OUTPUT_NAME] [-f] bin

positional arguments:
  bin                   Target binary file

options:
  -h, --help            show this help message and exit
  -s SIZE, --size SIZE  Output PNG size (square), must be greater than 100
  -d OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Output directory
  -n OUTPUT_NAME, --output-name OUTPUT_NAME
                        Output name
  -f, --overwrite       Overwrite existing output PNGs
```

```
pngs2bin.py [-h] [-o OUTPUT_FILE] [-f] pngs [pngs ...]

positional arguments:
  pngs                  Sources PNG files

options:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Output file
  -f, --overwrite       Overwrite the output file
```