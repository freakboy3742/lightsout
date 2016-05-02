#/usr/bin/env python
import io
import re
from setuptools import setup, find_packages


with io.open('./lightsout/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='lightsout',
    version=version,
    description='A tool to convert online radio playlist data into playable Spotify playlists',
    long_description=long_description,
    author='Russell Keith-Magee',
    author_email='russell@keith-magee.com',
    # url='http://pybee.org/lightsout',
    url='https://github.com/freakboy3742/lightsout',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'spotipy'
    ],
    entry_points={
        'console_scripts': [
            'lightsout = lightsout.__main__:main',
        ]
    },
    license='New BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Multimedia :: Sound/Audio',
    ],
    test_suite='tests'
)
