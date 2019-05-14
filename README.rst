secretconf
==========

.. image:: https://img.shields.io/pypi/v/secretconf.svg
    :target: https://pypi.python.org/pypi/secretconf
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/xmonader/secretconf.png
   :target: https://travis-ci.org/xmonader/secretconf
   :alt: Latest Travis CI build status

.. image:: https://codecov.io/gh/xmonader/secretconf/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/xmonader/secretconf


Manage your secret configurations easily

Usage
-----
secretconf is a library to manage (encrypt/decrypt) your credentials on demand using your private key.

============
Hush
============
hush is a commandline utility installed with secretconf to make your life easier to store and update credentials

.. code-block:: bash

    hush --section twittermain --fields 'user,__token' --privatekey ~/.ssh/id_rsa  


.. code-block:: bash

    hush --help
    Usage: hush [OPTIONS]

    Options:
        --section TEXT     Section (Appname)
        --privatekey TEXT  Privatekey path
        --configpath TEXT  Secret configuration path
        --fields TEXT      quoted comma separated fields; secret fields are prefixed with __
        --help             Show this message and exit.

============


Installation
------------
* `pip3 install secretconf`

.. code-block:: bash

   git clone https://github.com/xmonader/secretconf
   cd secretconf && python3 setup.py install


Testing
------------
You can use `pytest tests` or just `tox` make sure to `install requirements-test.txt` or `make test`


Generating Docs
----------------
make gendocs

Requirements
------------

- setuptools==38.5.0
- click==6.7
- PyNaCl==1.2.1
- npyscreen==4.10.5

Licence
-------
* Software is provided as is under BSD 3-Clause License


Authors
-------

`secretconf` was written by `Ahmed Youssef <xmonader@gmail.com>`_.
