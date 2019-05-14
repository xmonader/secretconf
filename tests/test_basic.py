# Sample Test passing with nose and pytest

import nacl.utils
from nacl.public import PrivateKey, Box
from nacl.secret import SecretBox
import nacl.signing
import os
from secretconf import *

USER = "ahmed"
PASSWORD = "weakpassword"
APPNAME = 'twitter_app1'

sk = nacl.signing.SigningKey.generate()
pk = sk.verify_key
hashedsk = hash32(sk.encode())

hsk = PrivateKey(hashedsk)
hpk = hsk.public_key
box = Box(hsk, hpk)

TEST_CONFIG_PATH = '/tmp/test_mkconfig.secret'

# TODO: use a finalizer (teardown) for test functions.


def cleanup():
    os.remove(TEST_CONFIG_PATH)


def test_encrypt_decrypt():
    data = "hello world"
    assert decrypt(encrypt(data, box), box) == data


def test_encrypt_decrypt_with_sshkey():
    data = "hello world"
    assert decrypt(encrypt(data, box), box) == data

# TODO: mock the file operations calls.


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

    cleanup()


def test_read_config_file_returns_decrypted_data():
    make_config(APPNAME, {'user': USER, '__password': PASSWORD},
                config_path=TEST_CONFIG_PATH, private_key=hashedsk)

    assert os.path.exists(TEST_CONFIG_PATH)
    with open(TEST_CONFIG_PATH, 'r') as f:
        content = f.read()
        assert APPNAME in content
        assert "user" in content
        assert USER in content
        assert "__password" in content
        assert PASSWORD not in content

    conf = read_config(APPNAME, config_path=TEST_CONFIG_PATH,
                       private_key=hashedsk)
    assert APPNAME in conf
    assert 'user' in conf[APPNAME]
    assert '__password' in conf[APPNAME]
    assert conf[APPNAME]['user'] == USER
    assert conf[APPNAME]['__password'] == PASSWORD

    cleanup()


def test_make_config_creates_file_with_encrypted_data_with_multiple_apps():
    make_config(APPNAME, {'user': USER, '__password': PASSWORD},
                config_path=TEST_CONFIG_PATH, private_key=hashedsk)
    make_config('github', {'user': USER, '__token': '123456789'},
                config_path=TEST_CONFIG_PATH, private_key=hashedsk)

    assert os.path.exists(TEST_CONFIG_PATH)
    with open(TEST_CONFIG_PATH, 'r') as f:
        content = f.read()
        assert APPNAME in content
        assert "user" in content
        assert USER in content
        assert "__password" in content
        assert PASSWORD not in content
        assert "github" in content
        assert "__token" in content
        assert "123456789" not in content

    conf = read_config(APPNAME, config_path=TEST_CONFIG_PATH,
                       private_key=hashedsk)
    assert conf[APPNAME]['user'] == USER
    assert conf[APPNAME]['__password'] == PASSWORD
    assert conf['github']['user'] == USER
    assert conf['github']['__token'] == '123456789'

    cleanup()
