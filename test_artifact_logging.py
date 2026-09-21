import os
import mlflow

# 1. Point MLflow to your active port-forwarded server
mlflow.set_tracking_uri("http://127.0.0.1:8080")

# 2. Create a brand-new experiment using the proxy artifact destination
experiment_name = "k8s_proxied_experiment"
try:
    exp_id = mlflow.create_experiment(
        experiment_name, 
        artifact_location="mlflow-artifacts:/"
    )
    mlflow.set_experiment(experiment_name)
except Exception:
    mlflow.set_experiment(experiment_name)

# 3. Create a local dummy file to act as our artifact
artifact_filename = "model_summary.txt"
with open(artifact_filename, "w") as f:
    f.write("This is a test artifact proxied through Kubernetes persistent volume storage.")

# 4. Start an MLflow run to log metadata and artifacts
with mlflow.start_run() as run:
    # Log parameters and metrics (saved to PostgreSQL)
    mlflow.log_param("environment", "kubernetes-minikube-proxy")
    mlflow.log_metric("accuracy", 0.99)
    
    # Log the artifact file (proxied to Kubernetes PVC)
    mlflow.log_artifact(artifact_filename)
    
    print(f"Successfully logged run ID: {run.info.run_id}")

# Clean up local dummy file
if os.path.exists(artifact_filename):
    os.remove(artifact_filename)

print("Check the MLflow UI—your run and artifact should now be successfully recorded!")