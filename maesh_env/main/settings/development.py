from ._base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u8$em6-r#$i91=knt^uud&cy_r33imh4%cx9stx)newdmfd-17'

ALLOWED_HOSTS = ['localhost','10.202.1.171','192.168.1.70','maesh.io','172.20.10.2','10.10.3.126']

SITE = 'http://localhost:8000/'
LOCAL_DEV = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#API input data for all banks
API = {
    "dbs": {
        "url": "https://www.dbs.com/sandbox/api/sg/v1",
        "client_id": "6fce2916-d21e-4114-8433-8428d41effae",
        "client_secret": "527011b7-d982-478e-bd22-d28b54e33829"
    },
    "ocbc": {
        "url": "https://api.ocbc.com",
        "client_id": "1sQ5xa9nwB9i2E4l3BVAfyLMIe8a",
        "client_secret": "caHxtf_qg_pdCOBmsiMU5nR_fxAa",
        "access_token": "8c24fe6033a55fb4a8622239a0df7742"
    },
    "uob": {
        "url": "",
        "client_id": "",
        "client_secret": ""
    },
    "citi": {
        "url": "https://sandbox.apihub.citi.com/gcb/api",
        "client_id": "ff629055-00ed-4fcf-a4a3-8e99b2020a3c",
        "client_secret": "yK4rF0dK2xC5wN3fC7hF3vW6rQ8rY3kP5gE8rF6cT1gD6yP2iP"
    }
}

AUTHORIZATION = {
    "dbs": {
        'params': {
            'response_type': 'code',
            'client_id': API['dbs']['client_id'],
            'scope': 'Read',
            'redirect_uri': SITE+'payment_maesh_dbs',
            'state': '0399', #I think this number is random
        },
        'endpoint': API['dbs']['url']+'/oauth/authorize'
    },
    "ocbc": {
        'params': {
            'client_id': API['ocbc']['client_id'],
            'redirect_uri': SITE+'payment_maesh_ocbc',
            'scope': 'transactional'
        },
        'endpoint': API['ocbc']['url']+'/ocbcauthentication/api/oauth2/authorize'
    },
    "citi": {
        'params': {
            'response_type':'code',
            'client_id': API['citi']['client_id'],
            'scope': 'external_domestic_transfers',
            'countryCode':'SG',
            'businessCode':'GCB',
            'locale':'en_SG',
            'state':'12093', #This number has a purpose, but not now
            'redirect_uri': SITE+'payment_maesh_citi'
        },
        'endpoint': API['citi']['url']+'/authCode/oauth2/authorize'
    },
}

ACCESS_TOKEN = {
    "dbs": {
        'endpoint': API['dbs']['url']+'/oauth/tokens',
        'grant_type':'token',
    },
    "ocbc": {
        'endpoint': API['ocbc']['url']+'',
        'grant_type':'token',
    },
    "citi": {
        'endpoint': API['citi']['url']+'/authCode/oauth2/token/sg/gcb',
        'grant_type':'authorization_code',
    },
}

SALT_EDGE = {
    "app_id" : "BuOgKt4pJIYHXJvnQ5JWsJDncLUFvOx_UjMW_UJiH_M",
    "secret" : "BIwi-knfi5GG_oNvyd-R4as5D_RNHNy_BvZjTrJ0n7M"
}