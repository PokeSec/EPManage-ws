"""
settings.py : Project configuration

This file is part of EPControl.

Copyright (C) 2016  Jean-Baptiste Galet & Timothe Aeberhardt

EPControl is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

EPControl is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with EPControl.  If not, see <http://www.gnu.org/licenses/>.
"""


class Config(object):
    """Config class"""
    # ------------------------------------------------------------------------------
    # Basic config
    DEBUG = False

    # ------------------------------------------------------------------------------
    # Http config
    PREFERRED_URL_SCHEME = 'https'
    SESSION_COOKIE_SECURE = True
    MAX_CONTENT_LENGTH = 64 * 1024 * 1024  # 64Mo
    SESSION_COOKIE_DOMAIN = 'FIXME-YOURDOMAIN'
    SECRET_KEY = 'FIXME-VERYLONG LINE!'  # noqa pylint: disable=C0301

    # ------------------------------------------------------------------------------
    # Crypto config
    AUTH_PUBKEY = 'FIXME-PATH-TO-JWT-PUBKEY'

    def __load_from_obj(self, obj):
        for key in dir(obj):
            if key.isupper() and not getattr(self, key, None):
                setattr(self, key, getattr(obj, key))

    def __load_from_dict(self, data):
        for key, value in data.items():
            if key.isupper() and not getattr(self, key, None):
                setattr(self, key, value)

    def __init__(self):
        # Load Flask default settings
        from flask import Flask
        self.__load_from_dict(Flask.default_config)

        self.__clientdb = None

    def get(self, item, default=None):
        return getattr(self, item, default)

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __delitem__(self, key):
        return delattr(self, key)

    def __contains__(self, item):
        return item in self.keys()

    def __len__(self):
        return len(self.keys())

    def __iter__(self):
        yield from self.keys()

    def keys(self):
        return [x for x in dir(self) if x.isupper()]

    def setdefault(self, key, default=None):
        if key not in self:
            setattr(self, key, default)


class DebugConfig(Config):
    """Config class - Debug"""
    DEBUG = True

    def __init__(self):
        super(DebugConfig, self).__init__()


config = None
