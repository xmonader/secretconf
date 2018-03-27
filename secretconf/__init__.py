"""secretconf - secret configurations easily"""


__version__ = '0.1.0'
__author__ = 'Ahmed Youssef <xmonader@gmail.com>'
__all__ = []

"""
secretconf file looks like this
```
[sillyapp2]
user = xmonader
__password = RSE6sNZDb04mnQhF6bPRWW3SVrCyy+u13hpBiiman4XmBcip9N8Ga3q9O2sZxZadLqCd

[sillyapp3]
user = xmon121
__password = rjR4gSRQCCfOu4q0g7GyUFXiTTocYyKMP+cWbuHL9QaPfh9a/pKxrZEfpiQbhQ==

[sillyapp1]
user = ash
__password = 8wNHS635V5Dxu/aeX1T4xt+OuH2KFzLU4TgOSU90VzMZh2nDY9ui0yhFX8yzyg==
```



hush --section sillyapp1 --fields 'user,__password'


"""

import os
import base64
import hashlib
from configparser import ConfigParser
import nacl.utils
from nacl.public import PrivateKey, Box
from nacl.secret import SecretBox
import click
import npyscreen


def hash32(data):
    """
    Get sha256 of bytes

    @param data bytes: usually the private_key to be used later with encrypt, decrypt functions.

    returns sha256 digets of data bytes.
    """
    m = hashlib.sha256()
    m.update(data)
    return m.digest()

def encrypt(data, private_key):
    """
    Encrypt data using private_key

    @param data bytes : bytes to encrypt
    @param private_key: key of 32 bytes (you should use sha256 or hash32 function on the bytes of your private key)

    returns string of base64 encoded encrytped data using private_key
    """

    if isinstance(data, str):
        data = data.encode()

    box = SecretBox(private_key)
    nonce = nacl.utils.random(SecretBox.NONCE_SIZE)

    return base64.b64encode(box.encrypt(data, nonce)).decode()

def decrypt(data, private_key):
    """
    Decrypt data using private_key

    @param data bytes : data to decrypt
    @param private_key: key of 32 bytes (you should use sha256 or hash32 function on the bytes of your private key)

    returns string of the original data 
    """
    box = SecretBox(private_key)
    _bytes = base64.b64decode(data)
    return box.decrypt(_bytes).decode()

def make_config(section=None, data={}, config_path='/tmp/secrets.conf', private_key=''):
    """
    stores credentials section or app with data in specific configuration path using a private key
    data keys prefixed with __ are considered private and will be encrypted.

    @param section str: application or section name.
        e.g: myapp, githubuser, gitlaborg
    @param data dict: dict of fields and their values [fields prefixed with __ are private]
        e.g: {'name': 'xmonader', '__password': 'notmypassword'}

    @param config_path str: secretconf path defaults to /tmp/secrets.conf
    @param private_key: key of 32 bytes (you should use sha256 or hash32 function on the bytes of your private key)
     """

    if not os.path.exists(config_path):
        os.mknod(config_path)
    conf = ConfigParser()
    conf.read_file(open(config_path)) 
    conf[section] = {}
    for k, v in data.items():
        if k.startswith("__"):
            v = encrypt(v, private_key)
        conf[section][k] = v

    with open(config_path, "w") as cf:
        conf.write(cf)

def read_config(section=None, config_path='/tmp/secrets.conf', private_key=''):
    """
    reads credentials section or app with data in specific configuration path using a private key
    data keys prefixed with __ are considered private and will be encrypted.

    @param section str: application or section name.
        e.g: myapp, githubuser, gitlaborg
    @param config_path str: secretconf path defaults to /tmp/secrets.conf
    @param private_key: key of 32 bytes (you should use sha256 or hash32 function on the bytes of your private key)
     """

    data = {}
    if not os.path.exists(config_path):
        os.mknod(config_path)

    conf = ConfigParser()
    conf.read_file(open(config_path)) 
    
    for s in conf.sections():
        secdict = {}
        for k, v in conf[s].items():
            if k.startswith("__"):
                v = decrypt(v, private_key)
            secdict[k] = v
        data[s] = secdict

    return data


# TODO: support passphrases and use ssh-key in agent.
@click.command()
@click.option('--section', default='', help='Section (Appname)')
@click.option('--privatekey', default='~/.ssh/id_rsa', help='Privatekey path')
@click.option('--configpath', default='/tmp/secrets.conf', help='Secret configuration path')
@click.option('--fields', default='', help='quoted comma separated fields; secret fields are prefixed with __')
def hush(section, privatekey, configpath, fields):
    privatekey = os.path.expanduser(privatekey)
    configpath = os.path.expanduser(configpath)
    assert os.path.exists(privatekey)

    privatekey = open(privatekey, 'rb').read()
    privatekey = hash32(privatekey)

    widgets = []

    data = read_config(section, configpath, privatekey)
    if section not in data:
        data[section] = {}
    fields = [f.strip() for f in fields.split(",")]

    def curses_app(*args):
        form = npyscreen.Form()
        for f in fields:
            w = form.add(npyscreen.TitleText, name=f, value=data[section].get(f, ''))
            w._forfield = f 
            widgets.append(w)       

        form.edit()
        for w in widgets:
            data[section][w._forfield] = w.value

    npyscreen.wrapper_basic(curses_app) 
    make_config(section=section, data=data[section], config_path=configpath, private_key=privatekey) 

if __name__ == '__main__':
    hush()