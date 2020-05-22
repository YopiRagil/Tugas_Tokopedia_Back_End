import configparser

cfg = configparser.ConfigParser()
cfg.read("config.cfg")


class Config:
    SQLALCHEMY_DATABASE_URI = "%s+%s://%s:%s@%s:%s/%s" % (
        cfg["database"]["default_connection"],
        cfg["mysql"]["driver"],
        cfg["mysql"]["user"],
        cfg["mysql"]["password"],
        cfg["mysql"]["host"],
        cfg["mysql"]["port"],
        cfg["mysql"]["db"],
    )
    SQLALCHEMY_TRACK_MODIFICATION = False


class DevelopmentConfig(Config):
    APP_DEBUG = False
    DEBUG = False
    MAX_BYTES = 10000
    APP_PORT = 9090


class ProductionConfig(Config):
    APP_DEBUG = True
    DEBUG = True
    MAX_BYTES = 100000
    APP_PORT = 5050


class TestConfig(Config):
    APP_DEBUG = True
    DEBUG = True
    MAX_BYTES = 100000
    APP_PORT = 5050

    SQLALCHEMY_DATABASE_URI = "%s+%s://%s:%s@%s:%s/%s_test" % (
        cfg["database"]["default_connection"],
        cfg["mysql"]["driver"],
        cfg["mysql"]["user"],
        cfg["mysql"]["password"],
        cfg["mysql"]["host"],
        cfg["mysql"]["port"],
        cfg["mysql"]["db"],
    )
    SQLALCHEMY_TRACK_MODIFICATION = False
