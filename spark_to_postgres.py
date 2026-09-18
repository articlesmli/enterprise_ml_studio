from pyspark.sql import SparkSession

# Initialize Spark Session with PostgreSQL JDBC Driver Configuration
spark = SparkSession.builder \
    .appName("EnterpriseML-SparkToPostgres") \
    .config("spark.jars", "/app/postgresql-42.6.0.jar") \
    .getOrCreate()

print("Spark Session initialized successfully with PostgreSQL JDBC driver.")

# Add your existing data processing and JDBC write logic below:
# df = spark.read...
# df.write.format("jdbc")...
