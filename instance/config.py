import os

class Config(object):
    """
    Common configurations
    """
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:cj@localhost:5432/bucketlist"
    SECRET_KEY = os.getenv("SECRET_KEY")
  
class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:cj@localhost:5432/test_db'
    DEBUG = True

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing':TestingConfig,
}
