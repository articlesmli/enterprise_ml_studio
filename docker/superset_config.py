#------------------------------------------------------------------------------
# Superset specific config
#------------------------------------------------------------------------------
ROW_LIMIT = 5000

SUPERSET_WORKERS = 2

#------------------------------------------------------------------------------
# Flask SQLALCHEMY config
#------------------------------------------------------------------------------
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://ml_user:ml_password@ml-postgres:5432/ml_studio"

SECRET_KEY = "your-super-secret-key-change-this-in-production"