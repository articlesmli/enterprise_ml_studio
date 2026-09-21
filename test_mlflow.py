import mlflow

# Point MLflow to your local port-forwarded tracking server
mlflow.set_tracking_uri("http://localhost:8080")

# Set an experiment name
mlflow.set_experiment("kubernetes_test_experiment")

# Start a run and log some parameters and metrics
with mlflow.start_run():
    mlflow.log_param("model_type", "linear_regression")
    mlflow.log_metric("accuracy", 0.95)
    print("Successfully logged run to MLflow tracking server!")
