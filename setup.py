#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages
import deploy
import time

setup(
    name="deploy",
    version="0.0.1",
    packages=find_packages(exclude=["test*"]),
    # py_modules=["test"],
    # data_files=[(".", ["pip_requirements.txt"])],
    install_requires=["PyYAML"],
    zip_safe=False,

    description="A deploy tools for CodeDeploy",
    author="pengmingqiang",
    author_email="pmq2008@gmail.com",

    license="GPL",
    platforms="Independant",
    url="",
    entry_points={
        'console_scripts': [
            'deploycli = deploy.cli:main',
        ]
    },
)
