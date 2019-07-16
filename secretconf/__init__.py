"""secretconf - secret configurations easily"""


__version__ = '0.1.0'
__author__ = 'Ahmed Youssef <xmonader@gmail.com>'

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
import nacl.encoding
# from nacl.secret import SecretBox
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


def encrypt(data, box):
    """
    Encrypt data using private_key

    @param data bytes : bytes to encrypt
    @param box: nacl box to encrypt data

    returns string of base64 encoded encrytped data using private_key
    """

    if isinstance(data, str):
        data = data.encode()

    return base64.b64encode(box.encrypt(data)).decode()


def decrypt(data, box):
    """
    Decrypt data using private_key

    @param data bytes : data to decrypt
    @param private_key: nacl box to decrypt data

    returns string of the original data 
    """
    _bytes = base64.b64decode(data)
    return box.decrypt(_bytes).decode()


def make_config(section=None, data=None, config_path='/tmp/secrets.conf', private_key=''):
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
    data = data or {}
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        os.mknod(config_path)
    conf = ConfigParser()
    conf.read_file(open(config_path))
    conf[section] = {}
    sk = PrivateKey(private_key, nacl.encoding.Base64Encoder())

    pk = sk.public_key
    box = Box(sk, pk)

    for k, v in data.items():
        if k.startswith("__"):
            v = encrypt(v, box)
        conf[section][k] = v

    with open(config_path, "w") as cf:
        conf.write(cf)

save_config = write_config = make_config

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
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        os.mknod(config_path)

    conf = ConfigParser()
    conf.read_file(open(config_path))

    sk = PrivateKey(private_key, nacl.encoding.Base64Encoder())
    pk = sk.public_key
    box = Box(sk, pk)

    for s in conf.sections():
        secdict = {}
        for k, v in conf[s].items():
            if k.startswith("__"):
                v = decrypt(v, box)
            secdict[k] = v
        data[s] = secdict

    return data

@click.command()
@click.option('--name', help='Keypair name')
def hush_keygen(name):
    if not name:
        print("didn't specify --name. will generate (mykey.priv, mykey.pub)")
        name = "mykey"
    hsk = PrivateKey.generate()
    hpk = hsk.public_key
    cwd = os.getcwd()

    skpath = os.path.join(cwd, name + ".priv")
    pkpath = os.path.join(cwd, name + ".pub")
    with open(skpath, "wb") as f:
        f.write(hsk.encode(nacl.encoding.Base64Encoder()))
    with open(pkpath, "wb") as f:
        f.write(hpk.encode(nacl.encoding.Base64Encoder()))


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
    # privatekey = hash32(privatekey)

    widgets = []

    data = read_config(section, configpath, privatekey)
    if section not in data:
        data[section] = {}
    fields = [f.strip() for f in fields.split(",")]

    def curses_app(*args):
        form = npyscreen.Form()
        for f in fields:
            w = form.add(npyscreen.TitleText, name=f,
                         value=data[section].get(f, ''))
            w._forfield = f
            widgets.append(w)

        form.edit()
        for w in widgets:
            data[section][w._forfield] = w.value

    npyscreen.wrapper_basic(curses_app)
    make_config(section=section, data=data[section],
                config_path=configpath, private_key=privatekey)


if __name__ == '__main__':
    hush()
