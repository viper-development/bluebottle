from bluebottle.settings.testing import *
from bluebottle.settings.secrets import *

# Database
DATABASES = {
    'default': {
        "ENGINE": "bluebottle.clients.postgresql_backend",
        'HOST': 'db',
        'PORT': '5432',
        'NAME': 'bluebottle_test',
        'USER': 'bluebottle_test',
        'PASSWORD': 'password'
    }
}


SLOW_TEST_THRESHOLD_MS = 1000
DEBUG = True
