import os
import hashlib
import binascii


def create_activation_key(username):
    if isinstance(username, str):
        username = username.encode('utf-8')

    elif not isinstance(username, bytes):
        raise TypeError('Type of parameter username must be str or bytes')

    salt = binascii.hexlify(os.urandom(10))

    return hashlib.sha256(username + salt).hexdigest()
