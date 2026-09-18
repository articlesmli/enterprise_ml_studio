from pyspark.sql import SparkSession

# Initialize Spark session cleanly without packages or ivy paths
spark = SparkSession.builder \
    .appName("EnterpriseMLStudio-SparkIntegration") \
    .getOrCreate()

data = [
    ("model_v1", 0.85, 100),
    ("model_v2", 0.91, 150),
    ("model_v3", 0.88, 200)
]
columns = ["model_name", "accuracy", "run_count"]

df = spark.createDataFrame(data, columns)

jdbc_url = "jdbc:postgresql://ml-postgres:5432/ml_studio"
connection_properties = {
    "user": "ml_user",
    "password": "ml_password",
    "driver": "org.postgresql.Driver"
}

df.write \
    .jdbc(url=jdbc_url, table="spark_analytics_metrics", mode="overwrite", properties=connection_properties)

print("Data successfully written from Spark to PostgreSQL!")
spark.stop()