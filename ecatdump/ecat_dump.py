import re
import nibabel
import os
import json
from ecatdump.helper_functions import compress, decompress


class EcatDump:

    def __init__(self, ecat_file, nifti_file=None, decompress=True):
        self.ecat_header = {}
        self.subheaders = []
        self.ecat_info = {}
        self.affine = {}
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

        # extract ecat info
        self.extract_header_info()
        self.extract_subheaders()
        self.extract_affine()

        # aggregate ecat info into ecat_info dictionary
        self.ecat_info['header'] = self.ecat_header
        self.ecat_info['subheaders'] = self.subheaders
        self.ecat_info['affine'] = self.affine

        if not nifti_file:
            self.nifti_file = os.path.splitext(self.ecat_file)[0] + ".nii.gz"
        else:
            self.nifti_file = nifti_file

    def display_ecat_and_nifti(self):
        print(f"ecat is {self.ecat_file}\nnifti is {self.nifti_file}")

    def extract_affine(self):
        self.affine = self.ecat.affine.tolist()

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

    def extract_subheaders(self):
        # collect subheaders
        subheaders = self.ecat.dataobj._subheader.subheaders
        for subheader in subheaders:
            holder = {}
            subheader_data = subheader.tolist()
            subheader_dtypes = subheader.dtype.descr

            for i in range(len(subheader_data)):
                holder[subheader_dtypes[i][0]] = {
                    'value': self.transform_from_bytes(subheader_data[i]),
                    'dtype': self.transform_from_bytes(subheader_dtypes[i][1])}

            self.subheaders.append(holder)

    def show_affine(self):
        for row in self.affine:
            print(row)

    def show_header(self):
        for key, value in self.ecat_header.items():
            print(f"{key}: {value}")

    def show_subheaders(self):
        for subheader in self.subheaders:
            print(subheader)

    def json_out(self):
        temp_json = json.dumps(self.ecat_info, indent=4)
        print(temp_json)

    @staticmethod
    def transform_from_bytes(bytes_like):
        if type(bytes_like) is bytes:
            return bytes_like.decode()
        else:
            return bytes_like
