# secretconf

![[https://pypi.python.org/pypi/secretconf](pypi)](https://img.shields.io/pypi/v/secretconf.svg)
![[https://travis-ci.org/xmonader/secretconf]](https://travis-ci.org/xmonader/secretconf.png)

![[https://codecov.io/gh/xmonader/secretconf]](https://codecov.io/gh/xmonader/secretconf/branch/master/graph/badge.svg)


Manage your secret configurations easily

# Installation
`pip3 install secretconf --user`


# Usage
secretconf is a library to manage (encrypt/decrypt) your credentials on demand using public key encryption.

## Hush
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

### Data storage
You can configure where to save the data using `--configpath` which is set to `/tmp/secrets.conf` by default. 
```toml
[twittermain]
user = ahmed
__token = eYCWre9l7IauoHs6K3D5J2wkgnQQBtFV4CoZE3W4tpbxa7Z7Qt+c/LnQhSI=

```
> Please notice that you can't use multiple keys on the same `configpath` file

# API usage 
secretconf [documentation](https://xmonader.github.io/secretconf/api/secretconf/)

## make_config
```python
def test_make_config_creates_file_with_encrypted_data():
    make_config(APPNAME, {'user': USER, '__password': PASSWORD},
                config_path=TEST_CONFIG_PATH, private_key=hashedsk)

    assert os.path.exists(TEST_CONFIG_PATH)
    with open(TEST_CONFIG_PATH, 'r') as f:
        content = f.read()
        assert "user" in content
        assert USER in content
        assert "__password" in content
        assert PASSWORD not in content
```


## read_config

```python
    conf = read_config(APPNAME, config_path=TEST_CONFIG_PATH,
                       private_key=hashedsk)
    assert APPNAME in conf
    assert 'user' in conf[APPNAME]
    assert '__password' in conf[APPNAME]
    assert conf[APPNAME]['user'] == USER
    assert conf[APPNAME]['__password'] == PASSWORD
```

# Testing
secretconf tests exists in [tests](./tests) directory 
- basic tests `test_basic.py`: encryption/decryption and usage of `make_config` and `read_config`
- property based tests `test_properties.py`

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
