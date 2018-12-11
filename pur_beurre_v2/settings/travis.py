from . import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

from . import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://d767892c56054439a3eb13cc3824706b@sentry.io/1317774",
    integrations=[DjangoIntegration()]
)

SECRET_KEY = ')kto17qw(m#8)g0bc)9#v3$p5rq(v@$u0zlezr7**73&ixp35v'
DEBUG = False
ALLOWED_HOSTS = ['pshop.me', 'www.pshop.me', '46.101.170.37']

