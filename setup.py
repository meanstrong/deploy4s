#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="deploy4s",
    version="0.0.1",
    packages=find_packages(exclude=["test*"]),
    # py_modules=["test"],
    # data_files=[(".", ["pip_requirements.txt"])],
    install_requires=["PyYAML"],
    zip_safe=False,

    url="https://github.com/meanstrong/deploy4s",
    license=license,
    description="A deploy tools for CodeDeploy",
    long_description=readme,
    author="pengmingqiang",
    author_email="rockypengchina@outlook.com",
    maintainer="pengmingqiang",
    maintainer_email="rockypengchina@outlook.com",
    platforms=['any'],

    entry_points={
        'console_scripts': [
            'deploycli = deploy4s.cli:main',
        ]
    },
)
