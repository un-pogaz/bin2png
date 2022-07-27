import sys, os, argparse, re
import struct, pathlib
from PIL import Image


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output-file', help='Output file', default=None, type=pathlib.Path, required=False)
parser.add_argument('-f', '--overwrite', help='Overwrite output file', action='store_true', required=False)
parser.add_argument('pngs', help='Sources PNG files', type=pathlib.Path, nargs='+')
args = parser.parse_args()


if not args.output_file:
    args.output_file = re.sub(r'\.\d{4}.png$', '', os.path.basename(args.pngs[0]))

if os.path.exists(args.output_file) and not args.overwrite:
    print('ERROR: The output file already exist.')
    print('Target output: "{}"'.format(args.output_file))
    sys.exit(1)

if not os.path.exists(os.path.dirname(args.output_file)):
    os.makedirs(os.path.dirname(args.output_file))


chunks = {}

lengths = set()
for png in args.pngs:
    im = Image.open(png).convert('L')
    
    data = im.tobytes()
    signature, length, chunk_number = struct.unpack('<8sLL', data[:16])
    if signature != b'bin2png\1':
        print('ERROR: Invalid signature in source PNG.')
        print('Invalid signature in {}: {}'.format(png, repr(signature)))
        sys.exit(2)
    lengths.add(length)
    chunks[chunk_number] = data[16:]

if len(lengths) != 1:
    print('ERROR: Multiple lengths in images! Are you mixing different volumes?')
    print('Lengths: {}'.format(lengths))
    sys.exit(3)
output_length = list(lengths)[0]

with open(args.output_file, 'wb') as f:
    for i in range(len(chunks)):
        f.write(chunks[i])
    f.seek(output_length, os.SEEK_SET)
    f.truncate() # this is not the smart way to do this but I am lazy
    print('File "{}" writed'.format(args.output_file))
