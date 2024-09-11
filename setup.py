from setuptools import find_packages, setup

setup(
    name="xbeam_virtualizarr",
    version="0.0.1",
    install_requires=[
        # 'apache-beam[gcp]',
        'xarray_beam',
        'xarray',
        'kerchunk',
        'fastparquet',
        'pyarrow',
        'gcsfs',
        'google-cloud',
    ],
    packages=find_packages(),
)