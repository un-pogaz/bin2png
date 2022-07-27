import sys, os, argparse
import struct, pathlib
from PIL import Image


MIN_SIZE = 100

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--size', help='Output PNG size (square), must be greater than '+str(MIN_SIZE), default=512, type=int, required=False)
parser.add_argument('-d', '--output-dir', help='Output directory', default='', type=pathlib.Path, required=False)
parser.add_argument('-n', '--output-name', help='Output name', default=None, type=pathlib.Path, required=False)
parser.add_argument('-f', '--overwrite', help='Overwrite existing output PNGs', action='store_true', required=False)
parser.add_argument('bin', help='Target binary file', type=pathlib.Path)
args = parser.parse_args()


if args.size < MIN_SIZE:
    print('ERROR: The wanted size for the output PNG is too small.')
    print('Size request is {}. Minimal size is {}.'.format(args.size, MIN_SIZE))
    sys.exit(1)

if not os.path.exists(args.bin) or not os.path.isfile(args.bin):
    print('ERROR: Target binary file does not exist.')
    print('Request binary file: "{}"'.format(args.bin))
    sys.exit(2)

if os.path.exists(args.output_dir) and not os.path.isdir(args.output_dir):
    print('ERROR: The output directory is not a folder.')
    print('Request output: "{}"'.format(args.output_dir))
    sys.exit(3)


if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

with open(args.bin, 'rb') as f:
    data = f.read()

def encode_header(length,chunk_number):
    return struct.pack('<8sLL',b'bin2png\1', length, chunk_number)

# encode a dummy header so we know how big it is
HEADER_LENGTH = len(encode_header(0,0))
W,H = args.size,args.size
CHUNKSIZE = (W*H)-HEADER_LENGTH
NAME=os.path.basename(args.output_name or args.bin)

chunks = []
for i in range((len(data) + CHUNKSIZE) // CHUNKSIZE):
    chunks.append(data[i*CHUNKSIZE:(i+1)*CHUNKSIZE])

def build_name(i):
    rslt = NAME+'.{:04d}.png'.format(i)
    if str(args.output_dir) != ('' or os.path.curdir):
        rslt = os.path.join(args.output_dir, rslt)
    return rslt

# test/calc if chunks already exist
ALREADY = 0
for i in range(len(chunks)):
    n = build_name(i)
    if os.path.exists(n):
        if not args.overwrite:
            print('ERROR: One of the output PNG already exist.')
            print('Already exist output: "{}"'.format(n))
            sys.exit(4)
        else:
            ALREADY = ALREADY + 1

# write the chunks
print('{} chunks'.format(len(chunks)))
print('WARNING: {} chunks has overwrited on anothers files'.format(ALREADY)) if ALREADY else ''
for i, rawchunk in enumerate(chunks):
    if len(rawchunk) < CHUNKSIZE:
        rawchunk = rawchunk+  (b'\0' * (CHUNKSIZE - len(rawchunk)))
    chunk = encode_header(len(data),i)+rawchunk
    im = Image.frombuffer('L', (W,H), chunk)
    im.save(build_name(i))
