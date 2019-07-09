from hypothesis import given
from hypothesis.strategies import text
import nacl.utils
from nacl.public import PrivateKey, Box
import os
from secretconf import *

USER = "ahmed"
PASSWORD = "weakpassword"
APPNAME = 'twitter_app1'

hsk = PrivateKey.generate()
hpk = hsk.public_key
box = Box(hsk, hpk)


@given(text())
def test_decode_inverts_encode(s):
    assert decrypt(encrypt(s, box), box) == s
