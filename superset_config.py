ROW_LIMIT = 5000
SUPERSET_WEBSERVER_TIMEOUT = 60
SECRET_KEY = "your-super-secret-key-change-it"

# Connect Superset metadata to your PostgreSQL instance
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://ml_user:ml_password@ml-postgres:5432/ml_studio_db"