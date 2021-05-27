import re
import nibabel
import os
from ecatdump.helper_functions import compress, decompress


class EcatDump:

    def __init__(self, ecat_file, nifti_file=None, decompress=True):
        self.ecat_header = {}
        if os.path.isfile(ecat_file):
            self.ecat_file = ecat_file
        else:
            raise FileNotFoundError(ecat_file)

        if '.gz' in self.ecat_file and decompress is True:
            uncompressed_ecat_file = re.sub('.gz', '', self.ecat_file)
            decompress(self.ecat_file, uncompressed_ecat_file)

        if '.gz' in self.ecat_file and decompress is False:
            raise Exception("Nifti must be decompressed for reading of file headers")

        try:
            self.ecat = nibabel.ecat.load(self.ecat_file)
        except nibabel.filebasedimages.ImageFileError as err:
            print("\nFailed to load ecat image.\n")
            raise err

        self.extract_header_info()

        if not nifti_file:
            self.nifti_file = os.path.splitext(self.ecat_file)[0] + ".nii.gz"
        else:
            self.nifti_file = nifti_file

    def display_ecat_and_nifti(self):
        print(f"ecat is {self.ecat_file}\nnifti is {self.nifti_file}")

    def extract_header_info(self):
        """
        Extracts header and coverts it to sane type -> dictionary
        :return: self.header_info
        """

        header_entries = [entry for entry in self.ecat.header]
        for name in header_entries:
            value = self.ecat.header[name].tolist()
            # convert to string if value is type bytes
            if type(value) is bytes:
                try:
                    value = value.decode("utf-8")
                except UnicodeDecodeError as err:
                    print(f"Error decoding header entry {name}: {value}\n {value} is type: {type(value)}")
            self.ecat_header[name] = value

        return self.ecat_header

    def show_header(self):
        for key, value in self.ecat_header.items():
            print(f"{key}: {value}")