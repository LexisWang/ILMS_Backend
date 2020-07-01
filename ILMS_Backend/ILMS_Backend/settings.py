"""
Django settings for ILMS_Backend project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import datetime
import os
import sys
from django.utils import timezone

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 添加 apps 的导包路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-lx7b@9nzhat9rtdp986f(kbdg35m0fkj$zif_)y5!v7lm=y@o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') if os.getenv('DEBUG') else True

ALLOWED_HOSTS = ['*']

# 跨域的配置
CORS_ORIGIN_WHITELIST = ()
# 允许携带cookie
CORS_ALLOW_CREDENTIALS = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',  # RestFul 风格库
    'django_filters',  # 数据库过滤插件

    'systems',
    'customers',
    'business',
    'funds',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'utils.MixinClass.my_middleware'
]

ROOT_URLCONF = 'ILMS_Backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ILMS_Backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎

        'HOST': os.getenv('MYSQL_HOST') if os.getenv('MYSQL_HOST') else "192.168.18.135",
        'PORT': os.getenv('MYSQL_PORT') if os.getenv('MYSQL_PORT') else 3306,
        'USER': os.getenv('MYSQL_ROOT_USER') if os.getenv('MYSQL_ROOT_USER') else "root",
        'PASSWORD': os.getenv('MYSQL_ROOT_PASSWORD') if os.getenv('MYSQL_ROOT_PASSWORD') else "123456-abc",
        'NAME': os.getenv('MYSQL_DATABASE') if os.getenv('MYSQL_DATABASE') else "ILMS"

        # 'HOST': '127.0.0.4',  # 数据库主机
        # 'PORT': 3306,  # 数据库端口
        # 'USER': 'root',  # 数据库用户名
        # 'PASSWORD': '123456-abc',  # 数据库用户密码
        # 'NAME': 'ILMS'  # 数据库名字
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = os.getenv('LANGUAGE_CODE') if os.getenv('LANGUAGE_CODE') else 'en-us'

TIME_ZONE = os.getenv('TIME_ZONE') if os.getenv('TIME_ZONE') else 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = os.getenv('USE_TZ') if os.getenv('USE_TZ') else True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = 'static/'

# drf 的配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    'EXCEPTION_HANDLER': 'utils.exceptions.cus_exception_handler',
}

# JWT 的配置
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

# 配置自定义的验证类
AUTH_USER_MODEL = 'systems.UsersInfo'

# Redis 缓存配置
CACHES = {
    "default": {  # 权限缓存
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('REDIS_LOCATION') if os.getenv('REDIS_LOCATION') else "redis://192.168.18.135:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'PASSWORD': os.getenv('REDIS_PASSWORD') if os.getenv('REDIS_PASSWORD') else '123456'
        }
    },
}

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'WARNING',
            # 'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'ILMS_Backend/logs/ilms.log'),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}
