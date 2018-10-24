"""
Django settings for osd project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!


# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tracker',
    'exambuilder',
    'school',
    'timetable',
    'searchableselect',
    'teachnet',
    'journal',
    'ckeditor',
    'dynamic_formsets',
    'debug_toolbar',
    'django.contrib.admin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'osd.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'osd.wsgi.application'

# new

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DB stored in settings_secret


LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kuala_Lumpur'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../../static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# For CKEditor - rich text

CKEDITOR_CONFIGS = {
    'default': {

    },
    'large': {
        'toolbar': 'full',
        # 'extraPlugins': 'autogrow',
        'removeButtons': 'Save,Source,NewPage,Preview,Print,Templates,Cut,Copy,Paste,PasteText,PasteFromWord,Undo,Redo,Replace,Find,SelectAll,Scayt,Form,Checkbox,Radio,Textarea,TextField,Select,Button,ImageButton,HiddenField,CopyFormatting,RemoveFormat,Outdent,Indent,Blockquote,CreateDiv,JustifyRight,JustifyBlock,BidiLtr,BidiRtl,Language,Anchor,Unlink,Image,Flash,HorizontalRule,Iframe,PageBreak,ShowBlocks,Maximize,About',

    },

    'small': {
        'toolbar': 'full',
        'removeButtons': 'Save,Source,NewPage,Preview,Print,Templates,Cut,Copy,Paste,PasteText,PasteFromWord,Undo,Redo,Replace,Find,SelectAll,Scayt,Form,Checkbox,Radio,Textarea,TextField,Select,Button,ImageButton,HiddenField,CopyFormatting,RemoveFormat,Outdent,Indent,Blockquote,CreateDiv,JustifyRight,JustifyBlock,BidiLtr,BidiRtl,Language,Anchor,Unlink,Image,Flash,HorizontalRule,Iframe,PageBreak,ShowBlocks,Maximize,About',

        'width': 500,

        'height': 100,

    },
}

INTERNAL_IPS = [
    '127.0.0.1',
]

CALENDAR_START_MONDAY_DAY = 20
CALENDAR_START_MONTH = 8
CALENDAR_START_YEAR = 2018

CALENDAR_END_MONDAY_DAY = 1
CALENDAR_END_MONTH = 7
CALENDAR_END_YEAR = 2019

CALENDAR_START_DATE = datetime.date(CALENDAR_START_YEAR, CALENDAR_START_MONTH, CALENDAR_START_MONDAY_DAY)
CALENDAR_END_DATE = datetime.date(CALENDAR_END_YEAR, CALENDAR_END_MONTH, CALENDAR_END_MONDAY_DAY)
