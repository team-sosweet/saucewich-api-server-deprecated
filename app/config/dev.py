class DevConfig():
    HOST = 'localhost'
    PORT = 8888
    DEBUG = True

    RUN_SETTING = dict(**{
        'host': HOST,
        'port': PORT,
        'debug': DEBUG
    })

    API_VERSION = '1.0.0'
    API_TITLE = 'Saucewich API'
    API_DESCRIPTION = 'Saucewich data-server API'
    API_PRODUCES_CONTENT_TYPES = ['application/json']
    API_CONTACT_EMAIL = 'dev.moreal@gmail.com'

    API_URI_FILTER = 'slash'
