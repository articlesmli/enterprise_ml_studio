import mlflow
from pyspark.sql import SparkSession

# 1. Set MLflow tracking URI to persist data across the cluster
mlflow.set_tracking_uri("http://mlflow-service:5000")

# 2. Initialize Spark Session with PostgreSQL JDBC Driver Configuration
spark = SparkSession.builder \
    .appName("EnterpriseML-SparkToPostgres") \
    .config("spark.jars", "/app/postgresql-42.6.0.jar") \
    .getOrCreate()

print("Spark Session initialized successfully with PostgreSQL JDBC driver.")

# 3. Start an MLflow tracking run
with mlflow.start_run(run_name="csv_to_postgres_job"):
    try:
        # Path to your CSV file inside the container (adjust filename as needed)
        csv_file_path = "/app/data/input_data.csv"
        
        print(f"Reading data from CSV: {csv_file_path}")
        df = spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv(csv_file_path)
        
        # Log row count as an MLflow metric
        row_count = df.count()
        mlflow.log_metric("dataset_row_count", row_count)
        print(f"Successfully read {row_count} rows from CSV.")

        # 4. Define your PostgreSQL connection properties (using unified 'ml_studio' DB)
        jdbc_url = "jdbc:postgresql://postgres-service:5432/ml_studio"
        connection_properties = {
            "user": "postgres",
            "password": "postgres",
            "driver": "org.postgresql.Driver"
        }

        # 5. Write the DataFrame to PostgreSQL
        target_table = "processed_ml_data"
        print(f"Writing data to PostgreSQL table: {target_table}")
        
        df.write \
            .jdbc(url=jdbc_url, table=target_table, mode="append", properties=connection_properties)

        print(f"Data successfully written to PostgreSQL database 'ml_studio' in table '{target_table}'!")
        mlflow.log_param("status", "SUCCESS")

    except Exception as e:
        print(f"Error during Spark CSV processing: {e}")
        mlflow.log_param("status", "FAILED")
        raise e

    finally:
        spark.stop()
        print("Spark Session stopped.")