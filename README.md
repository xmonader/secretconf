# secretconf

![[https://pypi.python.org/pypi/secretconf](pypi)](https://img.shields.io/pypi/v/secretconf.svg)
![[https://travis-ci.org/xmonader/secretconf]](https://travis-ci.org/xmonader/secretconf.png)

![[https://codecov.io/gh/xmonader/secretconf]](https://codecov.io/gh/xmonader/secretconf/branch/master/graph/badge.svg)


Manage your secret configurations easily

# Installation
```bash
pip3 install secretconf --user
```


# Usage
secretconf is a library to manage (encrypt/decrypt) your credentials on demand using public key encryption.

# Hush
hush is a commandline utility installed with secretconf to make your life easier to store and update credentials

```bash
hush --section twittermain --fields 'user,__token' --privatekey ~/.ssh/id_rsa  
```

```bash

hush --help
Usage: hush [OPTIONS]

Options:
    --section TEXT     Section (Appname)
    --privatekey TEXT  Privatekey path
    --configpath TEXT  Secret configuration path
    --fields TEXT      quoted comma separated fields; secret fields are prefixed with __
    --help             Show this message and exit.

```


# Installation

-  `pip3 install secretconf`

```bash
   git clone https://github.com/xmonader/secretconf
   cd secretconf && python3 setup.py install
```


# Testing
You can use `pytest tests` or just `tox` make sure to `install requirements-test.txt` or `make test`


# Generating Docs
`make gendocs`

# Requirements

- setuptools==38.5.0
- click==6.7
- PyNaCl==1.2.1
- npyscreen==4.10.5

# License
Software is provided as is under BSD 3-Clause License


# Authors

`secretconf` was written by `Ahmed Youssef <xmonader@gmail.com>`_.
