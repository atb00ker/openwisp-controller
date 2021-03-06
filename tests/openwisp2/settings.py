import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = True
TESTING = sys.argv[1:2] == ['test']
SHELL = 'shell' in sys.argv or 'shell_plus' in sys.argv

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': os.path.join(BASE_DIR, 'openwisp-controller.db'),
    }
}

SPATIALITE_LIBRARY_PATH = 'mod_spatialite.so'

SECRET_KEY = 'fn)t*+$)ugeyip6-#txyy$5wf2ervc0d2n#h)qb)y5@ly$t*@w'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    # openwisp2 admin theme
    # (must be loaded here)
    'openwisp_utils.admin_theme',
    # all-auth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_extensions',
    # openwisp2 modules
    'openwisp_controller.config',
    'openwisp_controller.pki',
    'openwisp_controller.geo',
    'openwisp_controller.connection',
    'openwisp_users',
    # admin
    'django.contrib.admin',
    'django.forms',
    # other dependencies
    'sortedm2m',
    'reversion',
    'leaflet',
    'flat_json_widget',
    # rest framework
    'rest_framework',
    'rest_framework_gis',
    # channels
    'channels',
    # 'debug_toolbar',
]
EXTENDED_APPS = ('django_x509', 'django_loci')

AUTH_USER_MODEL = 'openwisp_users.User'
SITE_ID = 1

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'openwisp_utils.staticfiles.DependencyFinder',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]
# INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'openwisp2.urls'

ASGI_APPLICATION = 'openwisp_controller.geo.channels.routing.channel_routing'
CHANNEL_LAYERS = {
    'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'},
}

TIME_ZONE = 'Europe/Rome'
LANGUAGE_CODE = 'en-gb'
USE_TZ = True
USE_I18N = False
USE_L10N = False
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = f'{os.path.dirname(BASE_DIR)}/media/'

CORS_ORIGIN_ALLOW_ALL = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'openwisp_utils.loaders.DependencyLoader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'openwisp_utils.admin_theme.context_processor.menu_items',
            ],
        },
    }
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

EMAIL_PORT = '1025'  # for testing purposes
LOGIN_REDIRECT_URL = 'admin:index'
ACCOUNT_LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL
OPENWISP_ORGANIZATON_USER_ADMIN = True  # tests will fail without this setting

# during development only
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if not TESTING:
    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost/1')
else:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    CELERY_BROKER_URL = 'memory://'

LOGGING = {
    'version': 1,
    'filters': {'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue'}},
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        }
    },
}

if not TESTING and SHELL:
    LOGGING.update(
        {
            'loggers': {
                '': {
                    # this sets root level logger to log debug and higher level
                    # logs to console. All other loggers inherit settings from
                    # root level logger.
                    'handlers': ['console'],
                    'level': 'DEBUG',
                    'propagate': False,
                },
                'django.db': {
                    'level': 'DEBUG',
                    'handlers': ['console'],
                    'propagate': False,
                },
            }
        }
    )

OPENWISP_CONTROLLER_CONTEXT = {'vpnserver1': 'vpn.testdomain.com'}

TEST_RUNNER = 'openwisp_utils.tests.TimeLoggingTestRunner'
if TESTING:
    OPENWISP_CONTROLLER_HARDWARE_ID_ENABLED = True

if os.environ.get('SAMPLE_APP', False):
    # Replace Config
    config_index = INSTALLED_APPS.index('openwisp_controller.config')
    INSTALLED_APPS.remove('openwisp_controller.config')
    INSTALLED_APPS.insert(config_index, 'openwisp2.sample_config')
    # Replace Pki
    pki_index = INSTALLED_APPS.index('openwisp_controller.pki')
    INSTALLED_APPS.remove('openwisp_controller.pki')
    INSTALLED_APPS.insert(pki_index, 'openwisp2.sample_pki')
    # Replace Geo
    geo_index = INSTALLED_APPS.index('openwisp_controller.geo')
    INSTALLED_APPS.remove('openwisp_controller.geo')
    INSTALLED_APPS.insert(geo_index, 'openwisp2.sample_geo')
    # Replace Connection
    connection_index = INSTALLED_APPS.index('openwisp_controller.connection')
    INSTALLED_APPS.remove('openwisp_controller.connection')
    INSTALLED_APPS.insert(connection_index, 'openwisp2.sample_connection')
    # Extended apps
    EXTENDED_APPS = (
        'django_x509',
        'django_loci',
        'openwisp_controller.config',
        'openwisp_controller.pki',
        'openwisp_controller.geo',
        'openwisp_controller.connection',
    )
    # Swapper
    CONFIG_DEVICE_MODEL = 'sample_config.Device'
    CONFIG_CONFIG_MODEL = 'sample_config.Config'
    CONFIG_TEMPLATETAG_MODEL = 'sample_config.TemplateTag'
    CONFIG_TAGGEDTEMPLATE_MODEL = 'sample_config.TaggedTemplate'
    CONFIG_TEMPLATE_MODEL = 'sample_config.Template'
    CONFIG_VPN_MODEL = 'sample_config.Vpn'
    CONFIG_VPNCLIENT_MODEL = 'sample_config.VpnClient'
    CONFIG_ORGANIZATIONCONFIGSETTINGS_MODEL = 'sample_config.OrganizationConfigSettings'
    PKI_CA_MODEL = 'sample_pki.Ca'
    PKI_CERT_MODEL = 'sample_pki.Cert'
    GEO_LOCATION_MODEL = 'sample_geo.Location'
    GEO_FLOORPLAN_MODEL = 'sample_geo.FloorPlan'
    GEO_DEVICELOCATION_MODEL = 'sample_geo.DeviceLocation'
    CONNECTION_CREDENTIALS_MODEL = 'sample_connection.Credentials'
    CONNECTION_DEVICECONNECTION_MODEL = 'sample_connection.DeviceConnection'

# local settings must be imported before test runner otherwise they'll be ignored
try:
    from .local_settings import *
except ImportError:
    pass
