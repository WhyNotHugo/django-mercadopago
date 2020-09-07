#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup

setup(
    name="django-mercadopago",
    description="MercadoPago integration for django",
    author="Hugo Osvaldo Barrera",
    author_email="hugo@barrera.io",
    url="https://github.com/WhyNotHugo/django-mercadopago",
    license="ISC",
    packages=find_packages(),
    long_description=open("README.rst").read(),
    install_requires=[
        "wheel>=0.26.0",
        "Django>=2.2.0",
        "mercadopago<1.0.0",
        "setuptools-git>=1.1",
        "setuptools-scm>=1.8.0",
    ],
    use_scm_version={"version_scheme": "post-release"},
    setup_requires=["setuptools_scm"],
    extras_require={"fixtures": ["factory-boy"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
