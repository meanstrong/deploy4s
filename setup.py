#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

import deploy4s


with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="deploy4s",
    version=deploy4s.__version__,
    packages=find_packages(exclude=["test*"]),
    install_requires=["PyYAML"],
    zip_safe=False,

    url="https://github.com/meanstrong/deploy4s",
    description="A deploy tools for CodeDeploy",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="pengmingqiang",
    author_email="rockypengchina@outlook.com",
    maintainer="pengmingqiang",
    maintainer_email="rockypengchina@outlook.com",
    platforms=['any'],
    license="Apache 2.0",
    entry_points={
        'console_scripts': [
            'deploycli = deploy4s.cli:main',
        ]
    },
)
