#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='django-mercadopago',
    description='MercadoPago integration for django',
    author='Hugo Osvaldo Barrera',
    author_email='hbarrera@z47.io',
    url='https://github.com/WhyNotHugo/django-mercadopago',
    license='ISC',
    packages=find_packages(),
    long_description=open('README.rst').read(),
    install_requires=[
        'wheel>=0.26.0',
        'Django>=1.8.5',
        'mercadopago>=0.3.4',
        'setuptools-git>=1.1',
        'setuptools-scm>=1.8.0',
    ],
    use_scm_version={'version_scheme': 'post-release'},
    setup_requires=['setuptools_scm'],
    extras_require={
        'fixtures': ['factory-boy'],
        'celery-task': ['celery'],
    },
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
