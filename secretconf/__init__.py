"""secretconf - secret configurations easily"""

__version__ = '0.1.0'
__author__ = 'Ahmed Youssef <xmonader@gmail.com>'
__all__ = []

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
    m = hashlib.sha256()
    m.update(data)
    return m.digest()

def encrypt(data, private_key):
    if isinstance(data, str):
        data = data.encode()

    box = SecretBox(private_key)
    nonce = nacl.utils.random(SecretBox.NONCE_SIZE)

    return base64.b64encode(box.encrypt(data, nonce)).decode()

def decrypt(data, private_key):
    box = SecretBox(private_key)
    _bytes = base64.b64decode(data)
    return box.decrypt(_bytes).decode()

def make_config(section=None, data={}, config_path='/tmp/secrets.conf', private_key=''):
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
    data = {}
    if not os.path.exists(config_path):
        os.mknod(config_path)

    conf = ConfigParser()
    conf.read_file(open(config_path)) 
    
    if section is None:
        for s in conf.sections():
            data[s] = {}
            for k, v in s.items():
                if k.startswith("__"):
                    v = decrypt(v, private_key)
                data[s][k] = v
    else:
        if section in conf:
            s = conf[section]
            for k, v in s.items():
                if k.startswith("__"):
                    v = decrypt(v, private_key)
                data[k] = v

    return data


# TODO: support passphrases and use ssh-key in agent.
@click.command()
@click.option('--section', default='', help='Section (Appname)')
@click.option('--privatekey', default='~/.ssh/id_rsa', help='Privatekey path')
@click.option('--configpath', default='/tmp/secrets.conf', help='Secret configuration path')
@click.option('--fields', default='', help='quoted comma separated fields; secret fields are prefixed with _')
def hush(section, privatekey, configpath, fields):
    from npyscreen import Form
    privatekey = os.path.expanduser(privatekey)
    configpath = os.path.expanduser(configpath)
    assert os.path.exists(privatekey)

    privatekey = open(privatekey, 'rb').read()
    privatekey = hash32(privatekey)

    widgets = []

    data = read_config(section, configpath, privatekey)
    fields = [f.strip() for f in fields.split(",")]

    def curses_app(*args):
        form = Form()
        for f in fields:
            w = form.add(npyscreen.TitleText, name=f, value=data.get(f, ''))
            w._forfield = f 
            widgets.append(w)       

        form.edit()
        for w in widgets:
            data[w._forfield] = w.value

    npyscreen.wrapper_basic(curses_app) 

    make_config(section=section, data=data, config_path=configpath, private_key=privatekey) 

if __name__ == '__main__':
    hush()