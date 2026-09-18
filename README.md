# Local Enterprise ML and Analytics Studio

An end-to-end local data and analytics platform leveraging containerised services and Kubernetes orchestration for distributed data processing, experiment tracking, and real-time visualisation.

## Project Overview

The **Local Enterprise ML & Analytics Studio** is a fully containerised architecture designed for prototyping enterprise-grade machine learning pipelines and analytical workflows. It bridges distributed processing engines, experiment tracking, data warehousing, business intelligence dashboards, and modern container orchestration into a single, cohesive local environment.

## Core Technology Stack

* **Orchestration & Infrastructure**: Docker Compose, Kubernetes, Minikube
* **Data Processing & Compute**: Apache Spark, Ray
* **Experiment Management**: MLflow Tracking Server
* **Data Warehouse**: PostgreSQL
* **Visualization & BI**: Apache Superset

## Architecture & Data Flow

1. **Ingestion & Processing**: Apache Spark processes raw workloads and computes analytical model metrics (`spark_analytics_metrics`).
2. **Persistence**: Processed metrics (`model_name`, `accuracy`, `run_count`) are automatically written and stored in the local PostgreSQL warehouse.
3. **Experiment Tracking**: MLflow tracks parameters, metrics, and model artifacts.
4. **Visualization**: Apache Superset connects directly to PostgreSQL, powering interactive dashboards (e.g., Model Accuracy Comparisons) for stakeholders.
5. **Orchestration**: Managed locally via Docker Compose for multi-container services or Minikube for native Kubernetes deployment manifests.

## Repository Structure

```text
enterprise_ml_studio/
├── docker-compose.yml              # Defines the local multi-container stack
├── app-deployment.yaml             # Single-service Kubernetes deployment manifest
├── k8s-full-stack.yaml             # Full-stack Kubernetes manifest (App + PostgreSQL + PVC)
├── Dockerfile                      # Container definition for the ML/Spark processing unit
├── Dockerfile.mlflow               # Custom build configuration for MLflow
├── Dockerfile.superset             # Custom build configuration for Apache Superset
├── superset_config.py              # Apache Superset configuration settings
├── spark_to_postgres.py            # PySpark processing and data ingestion script
├── postgresql-42.6.0.jar           # PostgreSQL JDBC driver for Spark
├── mlflow/                         # MLflow tracking directory
├── docker/                         # Additional Docker assets
└── README.md                       # Project documentation

```

## Getting Started & Installation

### Prerequisites

* [Docker](https://docs.docker.com/get-docker/?utm_source=gemini) and [Docker Compose](https://docs.docker.com/compose/install/?utm_source=gemini) installed on your local machine.
* [Minikube](https://minikube.sigs.k8s.io/docs/start/?utm_source=gemini) and `kubectl` (optional, for local Kubernetes orchestration).

---

### Option A: Local Deployment via Docker Compose

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/enterprise_ml_studio.git
cd enterprise_ml_studio

```


2. **Spin up the environment:**
```bash
docker-compose up -d

```


3. **Access the Services:**
* **Apache Superset Dashboard:** `http://localhost:8088`
* **MLflow Tracking UI:** `http://localhost:5000`
* **PostgreSQL Warehouse:** `localhost:5432`



---

### Option B: Local Kubernetes Deployment via Minikube

To test container orchestration using native Kubernetes manifests:

1. **Start Minikube:**
```bash
minikube start

```


2. **Point your terminal to Minikube's Docker daemon** (to use your locally built images):
```bash
eval $(minikube docker-env)

```


3. **Build the container image locally:**
```bash
docker build -t enterprise_ml_studio:latest .

```


4. **Deploy the full stack (PostgreSQL + ML App + PVC):**
```bash
kubectl apply -f k8s-full-stack.yaml

```


5. **Verify the deployment health:**
```bash
kubectl get pods

```



## Dashboard Setup in Apache Superset

1. Connect Superset to the PostgreSQL database warehouse using the connection string format:
```text
postgresql+psycopg2://<user>:<password>@postgres:5432/<db_name>

```


2. Register the `public.spark_analytics_metrics` dataset.
3. Create charts targeting dimensions like `model_name` and metrics like `AVG(accuracy)` to build custom monitoring views.
