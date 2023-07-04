from urllib.parse import urlparse

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

# parse database config from env vars
DATABASE_STRING_SPLIT = os.environ.get("DATABASE_ADDRESS").split("/")
db_name = DATABASE_STRING_SPLIT[len(DATABASE_STRING_SPLIT) - 1]
db_user = DATABASE_STRING_SPLIT[2].split(":")[0]
db_password = DATABASE_STRING_SPLIT[2].split(":")[1].split("@")[0]
db_host = DATABASE_STRING_SPLIT[2].split(":")[1].split("@")[1]
db_port = DATABASE_STRING_SPLIT[2].split(":")[2]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": db_name,
        "USER": db_user,
        "PASSWORD": db_password,
        "HOST": db_host,
        "PORT": db_port,
    }
}
#
# STATIC_URL = "/static/"
#
# # for django >= 3.1
# STATIC_ROOT = Path(BASE_DIR).joinpath("static")


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "172.30.150.14"
EMAIL_USE_TLS = False
EMAIL_PORT = 587
EMAIL_HOST_USER = "info@tourist.health"

ORDER_AMOUNT = 1

PAYMENT_CALLBACK_URL = "https://api.tourist.health"

PANEL_SERVICE_URL = "http://127.0.0.1:8000"

SESSION_ENGINE = 'redis_sessions.session'

SESSION_REDIS = {
    'host': '172.30.150.50',
    'port': 6379,
    'db': 0,
    'password': "",
    'prefix': 'session',
    'socket_timeout': 1
}


CACHEOPS_REDIS = {
    'host': '172.30.150.50', # redis-server is on same machine
    'port': 6379,        # default redis port
    'db': 0,             # SELECT non-default redis database
                         # using separate redis db or redis instance
                         # is highly recommended
    'socket_timeout': 3,   # connection timeout in seconds, optional
    'password': '',     # optional
}

CACHEOPS = {
    'order.*': {'ops': 'get', 'timeout': 60 * 60 * 24},
}

GRAYLOG_URI = "udp://172.30.150.17:12201"
GRAYLOG_FACILITY = "tourist-health-api-dev"

LOGGING = {
        'version': 1,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        # format in which logs will be written
        'formatters': {
            'simple': {
                'format': '[%(asctime)s] %(levelname)s %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'verbose': {
                # 'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
                'format': ' %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'facility': GRAYLOG_FACILITY
            },
        },
        'handlers': {
            'debug_log': {
                'level': 'DEBUG',
                'class': 'graypy.GELFUDPHandler',
                'host': urlparse(GRAYLOG_URI).hostname,
                'port': urlparse(GRAYLOG_URI).port,
                'formatter': 'verbose',
                'facility': GRAYLOG_FACILITY
            },
            'erro_log': {
                'level': 'ERROR',
                'class': 'graypy.GELFUDPHandler',
                'host': urlparse(GRAYLOG_URI).hostname,
                'port': urlparse(GRAYLOG_URI).port,
                'formatter': 'verbose',
                'facility': GRAYLOG_FACILITY
            },
            'info_log': {
                'level': 'INFO',
                'class': 'graypy.GELFUDPHandler',
                'host': urlparse(GRAYLOG_URI).hostname,
                'port': urlparse(GRAYLOG_URI).port,
                'formatter': 'verbose',
                'facility': GRAYLOG_FACILITY
            },
        },
        'loggers': {
            'error_logger': {
                'handlers': ['erro_log'],
                'level': 'ERROR',
                'propagate': True,
            },
            'debug_logger': {
                'handlers': ['debug_log'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'info_logger': {
                'handlers': ['info_log'],
                'level': 'INFO',
                'propagate': True,
            },
            'celery_logger': {
                'handlers': ['erro_log'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }

PAYMENT_BLACK_LIST = ["IR"]

CRYPTO_CALLBACK_URL = "http://172.30.150.12:8000"
CRYPTOM_API_URL = "http://172.30.151.21:9000"
CRYPTOM_CREATE_TRANSACTION = "/v1/payment"

sentry_sdk.init(
    dsn="https://4f895616039d47598889eda10c77f5fd@sentry.int.hidoctor.health/9",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,

    # By default the SDK will try to use the SENTRY_RELEASE
    # environment variable, or infer a git commit
    # SHA as release, however you may want to set
    # something more human-readable.
    # release="myapp@1.0.0",
)
