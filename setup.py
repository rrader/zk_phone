#!/usr/bin/env python

from setuptools import setup

setup(
    name='zk_phone',
    version='1.0',
    description='Zakupki Phone',
    author='Roman Rader',
    author_email='antigluk@gmail.com',
    url='https://github.com/rrader/zk_phone',
    install_requires=[
        'pad4pi==1.0.0',
        'charlcd==0.4.0',
        'RPi.GPIO==0.6.3',
        'netifaces',
    ],
    entry_points={
        'console_scripts': [
            'zk_phone = zk_phone.main:main',
            'zk_phone_simulator = zk_phone.lib.simulator.main',
        ],
    },
)
