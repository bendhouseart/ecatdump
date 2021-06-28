import unittest
import os
from dotenv import load_dotenv, find_dotenv
from ecatdump.thisbytes import get_ecat_bytes, ecat_header_maps, read_bytes

# load a test ecat file (this really should live at a url somewhere)
load_dotenv(find_dotenv())
ecat_test_file = os.environ.get("TEST_ECAT_PATH")


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super(MyTestCase).setUp()
        self.ecat_test_file = ecat_test_file
        self.ecat_header_maps = ecat_header_maps
        self.read_bytes = get_ecat_bytes(self.ecat_test_file)

    def test_get_ecat_bytes(self):
        # test whether the function can open a file and return a bytes object 
        ecat_bytes = get_ecat_bytes(ecat_test_file)
        self.assertEqual(type(ecat_bytes), bytes)
    
    def test_read_first_byte_entry(self):
        # test if it can read the first byte
        first_bytes = []
        for header, entry in self.ecat_header_maps['ecat_headers'].items():
            first_bytes.append((header, entry[0]['byte'], entry[0]['variable_name']))
        

if __name__ == '__main__':
    unittest.main()
