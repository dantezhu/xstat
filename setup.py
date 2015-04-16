# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="webstat",
    version="0.1.2",
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=['statsd'],
    scripts=[],
    url="https://github.com/dantezhu/webstat",
    license="MIT",
    author="dantezhu",
    author_email="dantezhu@qq.com",
    description="make statsd work with flask or django",
)
