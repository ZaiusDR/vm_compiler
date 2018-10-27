#!/usr/bin/env python

import setuptools

setuptools.setup(
    name='hack-vm-compiler',
    version='1.0',
    description='Jack VM Compiler for Hack Computer Platform',
    author='Eduardo Suarez',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'VMTranslator = vmcompiler.VMTranslator:main'
        ]
    }
)
