import errno

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "dev.cov19ap@gmail.com"
EMAIL_HOST_PASSWORD = "1A2b3F4gm"

ORDER_AMOUNT = 1

PAYMENT_CALLBACK_URL = "http://localhost:8000"

CRYPTO_CALLBACK_URL = "http://localhost:8000"

PANEL_SERVICE_URL = "http://localhost:8000"


LOGGING_ROOT = "logs"
if not os.path.exists(os.path.dirname(LOGGING_ROOT)):
    try:
        os.mkdir(LOGGING_ROOT)
    except OSError as exc:
        # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # filters will define when a logger should run
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
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    # handlers define the file to be written, which level to write in that file,
    # which format to use and which filter applies to that logger
    'handlers': {
        'debug_logfile': {
            'level': 'DEBUG',
            # 'filters': ['require_debug_true'], # do not run debug logger in production
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'debug.log'),
            'formatter': 'verbose'
        },
        'error_logfile': {
            'level': 'ERROR',
            # 'filters': ['require_debug_false'], # run logger in production
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'error.log'),
            'formatter': 'verbose'
        },
        'info_logfile': {
            'level': 'INFO',
            # 'filters': ['require_debug_false'], # run logger in production
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'info.log'),
            'formatter': 'verbose'
        },
        'celery_logfile': {
            'level': 'ERROR',
            # 'filters': ['require_debug_false'], # run logger in production
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'celery.log'),
            'formatter': 'verbose'
        },
    },
    # here the handlers for the loggers and the level of each logger is defined
    'loggers': {
        'error_logger': {
            'handlers': ['error_logfile'],
            'level': 'ERROR'
        },
        'debug_logger': {
            'handlers': ['debug_logfile'],
            'level': 'DEBUG'
        },
        'info_logger': {
            'handlers': ['info_logfile'],
            'level': 'DEBUG'
        },
        'celery_logger': {
            'handlers': ['celery_logfile'],
            'level': 'ERROR'
        },
    }
}

PAYMENT_BLACK_LIST = ["IR"]

CRYPTOM_API_URL = "http://localhost:8001"
CRYPTOM_CREATE_TRANSACTION = "/mocks/v1/payment"
