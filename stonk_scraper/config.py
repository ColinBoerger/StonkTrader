"""
Fake Passports development configuration.
Referenced from Flask config used in EECS 485.
Jason Kim, Fall 2019
"""

import os

# Root of this application.
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
# do we hard code a secret key here?
SECRET_KEY = b'FIXME SET THIS WITH: $ python3 -c "import os; print(os.urandom(24))" '  # noqa: E501  pylint: disable=line-too-long

SESSION_COOKIE_NAME = 'login'

DATABASE_FILENAME = 'test1.db'
'''os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'stonk_scraper.sqlite3'
)
'''