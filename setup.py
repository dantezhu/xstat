# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="xstat",
    version="0.1.8",
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=['statsd'],
    scripts=[],
    url="https://github.com/dantezhu/xstat",
    license="MIT",
    author="dantezhu",
    author_email="dantezhu@qq.com",
    description="make statsd work with flask, django, maple or other server",
)
