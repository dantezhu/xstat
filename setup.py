# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="webstat",
    version="0.1.1",
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=['statsd'],
    scripts=[],
    url="https://github.com/dantezhu/webstat",
    license="MIT",
    author="dantezhu",
    author_email="dantezhu@qq.com",
    description="join statsd with flask or django",
)
