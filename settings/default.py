# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "YOUR KEY"

DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'console_admin',
    'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.gis',
    'geoaware',
    'django_user_agents',
    'proxmate',
    'blog',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'geoaware.middleware.GeoAwareSessionMiddleware',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'message': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 300,
        'KEY_FUNCTION': 'utils.cache.make_key',
        'OPTIONS': {
            'MAX_ENTRIES': 100000,
        },
        'KEY_PREFIX': 'message'
    },
    'server_list': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 300,
        'KEY_FUNCTION': 'utils.cache.make_key',
        'OPTIONS': {
            'MAX_ENTRIES': 100000,
        },
        'KEY_PREFIX': 'server_list'
    },
    'packages_version': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 300,
        'KEY_FUNCTION': 'utils.cache.make_key',
        'OPTIONS': {
            'MAX_ENTRIES': 100000,
        },
        'KEY_PREFIX': 'packages_version'
    },
    'channels': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 300,
        'KEY_FUNCTION': 'utils.cache.make_key',
        'OPTIONS': {
            'MAX_ENTRIES': 100000,
        },
        'KEY_PREFIX': 'channels'
    },
    'daily_check': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 300,
        'KEY_FUNCTION': 'utils.cache.make_key',
        'KEY_PREFIX': 'daily_check'
    },
}


ROOT_URLCONF = 'proxmate.urls'

# this is for admin login
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'website/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.core.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'proxmate.wsgi.application'

WEBSITE_URL = 'https://proxmate.me/'

# Paypal
USER_AGENTS_CACHE = 'default'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

ADMIN_MENU = [
    {
        'name': 'Users',
        'models': [
            'User',
            'Message',
            'Payment',
            'Subscription',
        ],
        'icon': 'icon-user'
    },
    {
        'name': 'Inventory',
        'models': [
            'Country',
            'Server',
            'Package',
            'blog.post'
        ],
        'icon':'icon-user'
    },
    {
        'name': 'Blog',
        'models': [
            'Post',
        ],
        'icon':'icon-user'
    },
    {
        'name': 'Reports',
        'models': [
            ('Users', '/console/reports/users'),
            ('Usage', '/console/reports/usage'),
        ],
        'icon':'icon-user'
    }
]


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

BOOTSTRAP_ADMIN_SIDEBAR_MENU = True

GEOIP_PATH = '/usr/share/GeoIP'

CONSOLE_ADMIN_APP_NAME = ''
CONSOLE_ADMIN_APP_LOGO_URL = STATIC_URL + 'img/icon128.png'


SMTP2GO_USERNAME = 'smtp2go_email'
SMTP2GO_PASSWORD = 'smtp2go_password'


PAYPAL_MERCHANT_ID = 'YOUR PAYPAL ID'
PAYPAL_ACTION_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'

ELASTICSEARCH_ENABLED = False
ELASTICSEARCH_INDEX = "ELASTIC_ADDRESS"
ELASTICSEARCH_ADDRESS = "127.0.0.1"
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_USERNAME = ""
ELASTICSEARCH_PASSWORD = ""
