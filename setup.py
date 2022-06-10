#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine --dev
# or
#   $ pip install devpi-client

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'g11npy'
DESCRIPTION = 'Internationalization and localization tools.'
URL = 'https://github.com/TNick/g11n'
EMAIL = 'nicu.tofan@gmail.com'
AUTHOR = 'Nicu Tofan'
REQUIRES_PYTHON = '>=3.6.0'

# Dependencies.
REQUIRED = [
    'pluggy>=1.0.0',
]

# The scripts to generate.
SCRIPTS = [

]

# Optional, development, testing.
EXTRAS = {
    'dev': [
        'pytest',
        'twine',
        'devpi-client',
        'wheel',
        'sphinx',
        'sphinx_rtd_theme',
        'recommonmark',
        'm2r',
        'coverage'
    ],
    'tests': [
        'mock',
        'pytest',
    ],
}


# Detected further down.
VERSION = None
USE_DEVPI = True
USE_PIP_SETTINGS = True
REPO_USER = ''
REPO_PASSWORD = ''
PRIVATE_REPO_URL = ''
PRIVATE_REPO_CLIENT_CERT = ''


# Find the directory where this file is located.
here = os.path.abspath(os.path.dirname(__file__))

# Get the content of the top level read-me file.
try:
    with io.open(
        os.path.join(here, 'README.md'), 
        encoding='utf-8'
    ) as f:
        long_description = f.read()
        if long_description.startswith(DESCRIPTION):
            long_description = long_description[len(DESCRIPTION):]
        else:
            long_description = '\n' + long_description
except FileNotFoundError:
    long_description = DESCRIPTION

# Read version.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace(
        "-", "_"
    ).replace(
        " ", "_"
    )
    with open(
        os.path.join(here, project_slug, '__version__.py')
    ) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


def run_command(command):
    """
    Executes a command stored in a string.
    
    The output is yielded one line at a time.
    The error messages are printed directly.
    """
    import subprocess
    from time import sleep

    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    
    # Read stdout from subprocess until the buffer is empty!
    for line in iter(p.stdout.readline, b''):
        # Don't print blank lines
        if line:
            yield line.decode('utf-8').strip()
    
    # This ensures the process has completed, 
    # AND sets the 'returncode' attr
    while p.poll() is None:
        # Don't waste CPU-cycles
        sleep(.1)
    
    # Empty STDERR buffer
    err = p.stderr.read()
    if p.returncode != 0:
        # The run_command() function is 
        # responsible for logging STDERR
        print("Error: " + str(err))


def get_pip_settings():
    """
    Retrieve pip information from configuration file.
    """
    global PRIVATE_REPO_CLIENT_CERT
    global REPO_USER
    global REPO_PASSWORD
    global PRIVATE_REPO_URL
    for line in run_command("pip config list"):
        if line.startswith("global.client-cert='"):
            PRIVATE_REPO_CLIENT_CERT = line.replace(
                "global.client-cert='", ""
            )[:-1]
        elif line.startswith("global.index-url='"):
            PRIVATE_REPO_URL = line.replace(
                "global.index-url='", ""
            )[:-1]
        elif line.startswith("global.index-user='"):
            REPO_USER = line.replace(
                "global.index-user='", ""
            )[:-1]
        elif line.startswith("global.index-password='"):
            REPO_PASSWORD = line.replace(
                "global.index-password='", ""
            )[:-1]


class UploadCommand(Command):
    """ Support setup.py upload. """

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system(
            '{0} setup.py sdist '
            'bdist_wheel --universal'.format(sys.executable)
        )

        if USE_DEVPI:
            self.status('Uploading the package to PyPI via devpi…')
            if USE_PIP_SETTINGS:
                get_pip_settings()
            command = 'devpi use "{0}" --client-cert "{1}"'.format(
                PRIVATE_REPO_URL,
                PRIVATE_REPO_CLIENT_CERT
            )
            os.system(command)

            command = 'devpi login "{0}" --password "{1}"'.format(
                REPO_USER,
                REPO_PASSWORD
            )
            os.system(command)

            command = 'devpi upload'
            os.system(command)

        else:
            self.status('Uploading the package to PyPI via Twine…')
            command = 'twine upload dist/* --verbose'
            if USE_PIP_SETTINGS:
                get_pip_settings()

            if PRIVATE_REPO_URL:
                command = '{0} --repository-url "{1}"'.format(
                    command, PRIVATE_REPO_URL
                )

            if PRIVATE_REPO_CLIENT_CERT:
                command = '{0} --client-cert "{1}"'.format(
                    command, PRIVATE_REPO_CLIENT_CERT
                )
            if REPO_USER:
                command = '{0} --username "{1}"'.format(
                    command, REPO_USER
                )
            if REPO_PASSWORD:
                command = '{0} --password "{1}"'.format(
                    command, REPO_PASSWORD
                )
            os.system(command)

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    entry_points={
        'console_scripts': SCRIPTS,
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    test_suite='pytest',
    download_url='%s/archive/v%s.zip' % (URL, about['__version__']),
    project_urls={
        "Bug Tracker": "%s/issues" % URL,
        "Documentation": URL,
        "Source Code": URL,
    },
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
