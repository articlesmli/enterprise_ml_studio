# Local Enterprise ML and Analytics Studio

Designed and deployed a local containerised data and analytics platform facilitating distributed Spark execution, end-to-end machine learning pipelines, and GenAI experimentation. Streamlined local development workflows and cloud-native simulation utilizing distributed tools and enterprise platforms including **Kubernetes, Minikube, Kubeflow, Ray, MLflow, and Apache Superset**, backed by Infrastructure-as-Code deployment manifests and persistent database orchestration.

## Project Overview

The **Local Enterprise ML & Analytics Studio** bridges distributed processing engines, experiment tracking, data warehousing, business intelligence dashboards, and modern container orchestration into a single, cohesive environment.

## Core Technology Stack

* **Orchestration & Infrastructure**: Docker Compose, Kubernetes, Minikube, GitHub Actions (CI/CD)
* **Data Processing & Compute**: Apache Spark, Ray, Kubeflow
* **Experiment Management**: MLflow Tracking Server
* **Data Warehouse**: PostgreSQL
* **Visualization & BI**: Apache Superset

## Architecture & Data Flow

1. **Ingestion & Processing**: Apache Spark processes raw workloads and computes analytical model metrics (`spark_analytics_metrics`).
2. **Persistence**: Processed metrics (`model_name`, `accuracy`, `run_count`) are automatically written and stored in the local PostgreSQL warehouse.
3. **Experiment Tracking**: MLflow tracks parameters, metrics, and model artifacts.
4. **Visualization**: Apache Superset connects directly to PostgreSQL, powering interactive dashboards (e.g., Model Accuracy Comparisons) for stakeholders.
5. **Orchestration & CI/CD**: Managed locally via Docker Compose or Kubernetes manifests (`k8s-full-stack.yaml`), with automated building and linting powered by GitHub Actions CI/CD pipelines.

## 📁 Repository Structure

```text
enterprise_ml_studio/
├── .github/workflows/ci-cd.yml     # Automated CI/CD testing, building, and deployment pipeline
├── docker-compose.yml              # Defines the local multi-container stack
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
* [Minikube](https://minikube.sigs.k8s.io/?utm_source=gemini) and `kubectl` for Kubernetes orchestration.

---

### Option A: Local Deployment via Docker Compose

1. **Clone the repository:**
```bash
git clone https://github.com/articlesmli/enterprise_ml_studio.git
cd enterprise_ml_studio

```


2. **Spin up the environment:**
```bash
docker-compose up -d

```



---

### Option B: Local Kubernetes Deployment via Minikube

1. **Start Minikube and point your terminal to its Docker daemon:**
```bash
minikube start
eval $(minikube docker-env)

```


2. **Build the container image locally:**
```bash
docker build -t enterprise_ml_studio:latest .

```


3. **Deploy the full stack (PostgreSQL + ML App + PVC):**
```bash
kubectl apply -f k8s-full-stack.yaml

```



---

## Dashboard Setup in Apache Superset

1. Connect Superset to the PostgreSQL database warehouse using the connection string format:
```text
postgresql+psycopg2://<user>:<password>@postgres-service:5432/<db_name>

```


2. Register the `public.spark_analytics_metrics` dataset.
3. Create charts targeting dimensions like `model_name` and metrics like `AVG(accuracy)` to build custom monitoring views.
