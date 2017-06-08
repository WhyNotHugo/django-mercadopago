#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='django-mercadopago-simple',
    description='MercadoPago integration for django',
    author='Hugo Osvaldo Barrera',
    author_email='hbarrera@z47.io',
    url='https://gitlab.com/hobarrera/django-mercadopago',
    license='ISC',
    packages=find_packages(),
    long_description=open('README.rst').read(),
    install_requires=open('requirements.txt').readlines(),
    use_scm_version={'version_scheme': 'post-release'},
    setup_requires=['setuptools_scm'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
