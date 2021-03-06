# -*- coding: utf-8 -*-
from urlquote._native import ffi, lib
import six

# This buffer is passed to the C interface in order to obtain the quoted string. It will be
# reallocated automatically by `_native_quote` and `_native_unquote` if its size should not be
# large enough. It is ok to reset this buffer to a smaller value but it always needs to be a valid
# buffer.
buffer = ffi.new('uint8_t[]', 1)

def _native_quote(value):
    """
    Urlencodes the given bytes
    """
    global buffer
    buffer_len = len(buffer)
    quoted_len = lib.quote(value, len(value), buffer, buffer_len)
    if quoted_len > buffer_len:
        # Our buffer has not been big enough to hold the quoted url. Let's allocate a buffer large
        # enough and try again.
        buffer = ffi.new('uint8_t[]', quoted_len)
        lib.quote(value, len(value), buffer, quoted_len)

    return ffi.string(buffer, quoted_len)

def _native_unquote(value):
    """
    Urldecodes the given bytes
    """
    global buffer
    buffer_len = len(buffer)
    unquoted_len = lib.unquote(value, len(value), buffer, buffer_len)
    if unquoted_len > buffer_len:
        # Our buffer has not been big enough to hold the unquoted url. Let's allocate a buffer large
        # enough and try again.
        buffer = ffi.new('uint8_t[]', unquoted_len)
        lib.quote(value, len(value), buffer, unquoted_len)

    return ffi.string(buffer, unquoted_len)

def quote(value):
    """
    Performs string encoding and urlencodes the given string. Always returns utf-8 encoded bytes.
    """
    if not isinstance(value, six.binary_type):
        if not isinstance(value, six.text_type):
            value = str(value)
        value = value.encode('utf-8')

    return _native_quote(value)


def unquote(value):
    """
    Decodes a urlencoded string and performs necessary decoding depending on the used Python version.
    """
    if not isinstance(value, six.binary_type):
        if not isinstance(value, six.text_type):
            value = str(value)
        value = value.encode('utf-8')

    return _native_unquote(value)
