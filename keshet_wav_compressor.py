# Copyright 2020

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
# and associated documentation files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial 
# portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT 
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import struct
import logging
import binascii
import os, argparse, sys
from subprocess import call

try:
    import compress_wav
except ModuleNotFoundError:
    sys.exit("Please add the location of the compress_wav module to PYTHONPATH")


def compress(file, remove_after_compress = False):
    try:
        logging.info("Extracting WAV files from '{}'".format(file))
        with open(file, "rb") as f:
            out_base_name, _ = os.path.splitext(file)
            num_segments, = struct.unpack("<H", f.read(2))
            logging.debug("Number of segments: {}".format(num_segments))
            for i in range(0, num_segments):
                header = f.read(0xC2)
                g_filename = out_base_name + ".G" + "{0:0>2}".format(i+1)
                with open(g_filename, 'wb') as new_file:
                    if (i == 0):
                        new_file.write(struct.pack("<H", num_segments))
                    new_file.write(header)

                s = struct.Struct('<186x I 4x')
                unpacked_data = s.unpack(header)
                wav_size = unpacked_data[0]
                logging.debug("Handling WAV file of size {}".format(wav_size))
                wav = f.read(wav_size)
                w_filename = out_base_name + ".W" + "{0:0>2}".format(i + 1) + ".wav"
                with open(w_filename, 'wb') as new_file:
                    new_file.write(wav)
                
                compress_wav.compress_wav(w_filename, remove_file = True)
                
        if remove_after_compress:
            try:
                os.remove(file)
            except PermissionError as e:
                raise RuntimeError("Can't remove '{}', is the file read only?\nOS Message: {}".format(file, str(e)))
    except RuntimeError as e:
        sys.exit(str(e))

def main(parent_directory, remove_after_compress):
    for file_path in compress_wav.find_files(parent_directory, ['.gnd']):
        compress(file_path, remove_after_compress)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='WAV Compressor for Keshet-Orion games')
    parser.add_argument('-d', '--directory', action='store', required=True, help="Parent directory containing game")
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose output")
    parser.add_argument('-r', '--remove', action='store_true', default=False, help="Remove WAV files after compression")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level = logging.DEBUG)
    
    main(args.directory, args.remove)