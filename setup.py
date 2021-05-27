"""
This tool provides similar utility and output to ecat images that dcmdump from the dcmtk does for dicom images.
"""
from setuptools import find_packages, setup

dependencies = ['nibabel']

setup(
    name='ecatdump',
    version='0.1.0',
    url='https://github.com/bendhouseart/ecatdump',
    license='BSD',
    author='Anthony Galassi',
    author_email='28850131+bendhouseart@users.noreply.github.com',
    description='This tool provides similar utility and output to ecat images that dcmdump from the dcmtk does for dicom images.',
    long_description=__doc__,
    packages=find_packages(exclude=['tests', '.git']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'ecatdump = ecatdump.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
