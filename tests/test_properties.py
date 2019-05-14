from hypothesis import given
from hypothesis.strategies import text
import nacl.utils
import nacl.signing
from nacl.public import PrivateKey, Box
from nacl.secret import SecretBox
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


@given(text())
def test_decode_inverts_encode(s):
    assert decrypt(encrypt(s, box), box) == s
