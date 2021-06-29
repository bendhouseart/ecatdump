import json
from os import path
from os.path import join
import pathlib
import re

from numpy import dtype

parent_dir = pathlib.Path(__file__).parent.resolve()


# collect ecat header map
try:
    with open(join(parent_dir, 'ecat_headers.json'), 'r') as infile:
        ecat_header_maps = json.load(infile)
except FileNotFoundError:
    raise Exception("Unable to load header definitions and map from ecat_headers.json. Aborting.")


def get_ecat_bytes(path_to_ecat: str):
    # check if file exists
    if path.isfile(path_to_ecat):
        with open(path_to_ecat, 'rb') as infile:
            ecat_bytes = infile.read()
    else:
        raise Exception(f"No such file found at {path_to_ecat}")

    return ecat_bytes

def read_bytes(bytes_to_read: bytes, byte_start: int, byte_stop: int, byte_type):
    # move to start byte
    bytes_to_read.seek(byte_start, 0)

    # read a section of bytes from bytestart to byte stop
    byte_width = byte_stop - byte_start
    sought_bytes = bytes_to_read.read(byte_width)

    # attempt to decode the bytes

def get_buffer_size(data_type, variable_name):

    # ecat 6.X does stuff in a weird way
    #if len(re.findall(r'^.*?\([^\d]*(\d+)[^\d]*\).*$', variable_name)) > 0:
    #    fill_scalar = int(re.findall(r'\d+', variable_name)[0])
    first_split = variable_name.split('(')
    if len(first_split) == 2:
        fill_scalar = int(first_split[1][:-1])
    
    else:
        fill_scalar = 1
    
    scalar = int(re.findall(r'\d+', data_type)[0]) * fill_scalar
    
    #dtype =  re.findall(r'[A-z]', data_type)[0]
    return scalar

if __name__ == "__main__":
    for header, header_values in ecat_header_maps['ecat_headers'].items():
       
        print(header)
        byte_position = 0
        
        for each in header_values:
            print(each.get('byte'), each.get('variable_name'), each.get('type'), get_buffer_size(each.get('type'), each.get('variable_name')), byte_position)
            if byte_position != each.get('byte'):
                print(f"Mismatch in {header} between byte position {each.get('byte')} and calculated position {byte_position}.")
                paren_error = re.findall(r'^.*?\([^\d]*(\d+)[^\d]*\).*$', each.get('variable_name'))
            byte_position = get_buffer_size(each['type'], each['variable_name']) + byte_position
