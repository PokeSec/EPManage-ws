"""
auth.py : Authentication Logic

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
import jwt
import logging

from epmanage_ws import settings


def check_token(token, audience, options=None):
    """Verifies a token"""
    if not token:
        return None
    tmp = token.split(' ')
    if len(tmp) == 2 and tmp[0] == 'Bearer':
        if not options:
            options = {}
        decode_options = dict(
            verify_signature=True,
            verify_iat=True,
            verify_nbf=True,
            verify_exp=True,
            verify_iss=True,
            verify_aud=True,
            require_exp=True,
            require_iat=True,
            require_nbf=True)
        decode_options.update(options)
        try:
            data = jwt.decode(tmp[1],
                              open(settings.config.AUTH_PUBKEY).read(),
                              algorithm='RS512',
                              options=decode_options,
                              issuer='auth_module',
                              audience=audience)
            return data
        except jwt.exceptions.InvalidTokenError:
            logging.exception("Auth error")
            return None
    else:
        logging.error("Invalid token")
        return None
