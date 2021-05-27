import argparse
from ecatdump.ecat_dump import EcatDump
"""
simple command line tool to extract header info from ecat files.
"""


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("ecat", metavar="ecat_file", help="Ecat image to collect info from.")
    parser.add_argument("--nifti", "-n", metavar="file_name", help="Name of nifti output file", required=False)
    parser.add_argument("--dump", "-d", help="Dump information in Header", action="store_true", default=True)
    parser.add_argument("--convert", "-c", help="If supplied will attempt conversion.")
    args = parser.parse_args()
    return args


def main():
    cli_args = cli()
    ecat = EcatDump(cli_args.ecat)
    if cli_args.dump:
        ecat.show_header()


if __name__ == "__main__":
    main()
