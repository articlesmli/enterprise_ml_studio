# Enterprise ML Studio: Production MLflow on Kubernetes

A production-grade, highly reliable MLflow tracking server deployment running on Kubernetes. This architecture uses an external PostgreSQL database for metadata persistence and a Kubernetes Persistent Volume Claim (PVC) for centralized artifact storage, ensuring zero data loss across pod restarts and scaling events.

---

## Architecture & Technology Stack

* **Orchestration:** Kubernetes
* **MLflow Version:** `v2.11.3`
* **Metadata Database:** PostgreSQL (`ml-postgres:5432/ml_studio`) via `psycopg2-binary`
* **Artifact Storage:** Kubernetes Persistent Volume Claim (`mlflow-artifact-pvc`, 10Gi) mounted at `/mlflow/artifacts`
* **Service Discovery:** Kubernetes ClusterIP Service on port `5000`

---

## Prerequisites

Before deploying the MLflow tracking server, ensure your cluster has the following provisioned:

1. An active PostgreSQL database service (`ml-postgres`) accessible within the cluster network.
2. A bound Persistent Volume Claim named `mlflow-artifact-pvc` with read/write access.

---

## Deployment Manifest (`k8s-full-stack.yaml`)

The complete deployment and service manifest configures the container runtime, runtime dependency installation (`psycopg2-binary`), database connection strings, and volume mounts.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlflow-tracking-server
  labels:
    app: mlflow
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mlflow
  template:
    metadata:
      labels:
        app: mlflow
    spec:
      containers:
      - name: mlflow
        image: ghcr.io/mlflow/mlflow:v2.11.3
        ports:
        - containerPort: 5000
          name: http
        command:
          - /bin/sh
          - -c
          - |
            pip install --no-cache-dir psycopg2-binary &&
            exec mlflow server \
              --host 0.0.0.0 \
              --port 5000 \
              --backend-store-uri postgresql://ml_user:ml_password@ml-postgres:5432/ml_studio \
              --default-artifact-root mlflow-artifacts:/ \
              --artifacts-destination /mlflow/artifacts \
              --serve-artifacts
        volumeMounts:
        - name: mlflow-storage
          mountPath: /mlflow/artifacts
      volumes:
      - name: mlflow-storage
        persistentVolumeClaim:
          claimName: mlflow-artifact-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: mlflow-tracking-server
  labels:
    app: mlflow
spec:
  type: ClusterIP
  selector:
    app: mlflow
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000
      name: http

```

---

## Operations & Management

### 1. Deploy or Update the Stack

Apply the manifest to your Kubernetes cluster:

```bash
kubectl apply -f k8s-full-stack.yaml
kubectl rollout status deployment/mlflow-tracking-server

```

### 2. Verify Health and Pod Status

Confirm that the tracking server pod is running successfully (`1/1 Running`):

```bash
kubectl get pods -l app=mlflow

```

### 3. Verify Storage Mounts

Ensure the Persistent Volume Claim is properly bound and mounted inside the active container:

```bash
kubectl exec -it deployment/mlflow-tracking-server -c mlflow -- ls -la /mlflow/artifacts

```

### 4. Accessing the MLflow UI

To forward traffic locally to your workstation for testing or interactive tracking:

```bash
kubectl port-forward svc/mlflow-tracking-server 5000:5000

```

Navigate to `http://localhost:5000` in your web browser.

---

## Troubleshooting

* **Database Connection Errors / Missing Driver:**
If the container logs show `ModuleNotFoundError: No module named 'psycopg2'`, ensure the container startup command includes the inline `pip install psycopg2-binary` step as defined in the manifest above.
* **Persistent Volume Permission Issues:**
If pods fail to write artifacts, verify that the underlying storage class for `mlflow-artifact-pvc` allows read/write permissions for the container user.


## File tree
enterprise_ml_studio/
├── .github/
│   └── workflows/
│       └── ci-cd.yml             # GitHub Actions continuous integration and deployment pipeline
├── ai_services/
│   ├── agent_tools.py            # Custom GenAI agent tools implementation
│   ├── mcp_server.py             # Model Context Protocol (MCP) server configuration
│   └── requirements.txt          # Python dependencies specifically for AI services[cite: 2]
├── data/
│   └── input_data.csv            # Raw dataset used for your machine learning workflows[cite: 2]
├── docker/
│   └── superset_config.py        # Configuration files for Apache Superset[cite: 2]
├── mlflow/
│   └── artifacts/                # Local mount directory/folder for storing MLflow model artifacts[cite: 2]
├── terraform/
│   ├── .terraform/               # Local Terraform plugins and cache[cite: 2]
│   ├── .terraform.lock.hcl       # HashiCorp Configuration Language lock file for dependencies[cite: 2]
│   ├── main.tf                   # Main Terraform infrastructure-as-code orchestration file[cite: 2]
│   ├── terraform.tfstate         # Local state tracking file for Terraform[cite: 2]
│   └── terraform.tfstate.backup  # Backup of the previous Terraform state[cite: 2]
├── .dockerignore                 # Specifies files to ignore when building Docker images[cite: 2]
├── .env                          # Environment variables configuration file[cite: 2]
├── argocd-app.yaml               # ArgoCD application manifest for GitOps synchronization[cite: 2]
├── docker-compose.yml            # Multi-container local orchestration setup[cite: 2]
├── Dockerfile                    # Base or main container build file[cite: 2]
├── Dockerfile.mlflow             # Custom Dockerfile tailored for the MLflow server
├── Dockerfile.superset           # Custom Dockerfile tailored for Apache Superset
├── k8s-full-stack.yaml           # Consolidated Kubernetes deployment, service, and PVC configuration
├── mlflow-pvc.yaml               # Kubernetes Persistent Volume Claim configuration for MLflow[cite: 3]
├── postgresql-42.6.0.jar         # JDBC driver for connecting Spark/Java workloads to PostgreSQL[cite: 3]
├── README.md                     # Comprehensive project documentation and guides[cite: 3]
├── spark-job.yaml                # Kubernetes manifest to run distributed Spark processing jobs[cite: 3]
├── spark_to_postgres.py          # PySpark script for migrating or querying data with PostgreSQL[cite: 3]
├── superset_config.py            # Global Superset application configurations[cite: 3]
├── test_artifact_logging.py      # Test script to verify MLflow artifact logging functionality[cite: 3]
└── test_mlflow.py                # Validation script to test connection and logging to MLflow[cite: 3]