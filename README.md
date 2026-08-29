# DevOps Performance & Scalability Platform

A production-style DevOps project demonstrating:

- Kubernetes high availability
- Horizontal Pod Autoscaling
- Load balancing and ingress
- Canary deployments
- Blue-green deployments
- CI/CD automation
- Prometheus and Grafana monitoring
- k6 performance testing
- PostgreSQL optimization
- Redis caching

## Technology Stack

- Python / FastAPI
- Docker
- Kubernetes
- AWS EKS
- Helm
- NGINX / Istio
- Jenkins
- Argo Rollouts
- Prometheus
- Grafana
- PostgreSQL
- Redis
- k6


# DevOps Performance & Scalability Platform

A production-style DevOps project demonstrating containerized application deployment,
Kubernetes orchestration, horizontal scaling, persistent storage, observability,
performance testing, and CI/CD automation.

The project uses a FastAPI application backed by PostgreSQL and Redis and deploys
the application to Kubernetes using Helm and Kubernetes manifests.


Repository Structure
devops-perfomance-platform/
│
├── app/
│   ├── src/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── init_db.py
│   │   ├── models.py
│   │   └── ...
│   │
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── helm/
│   ├── postgresql/
│   │   └── values.yaml
│   └── redis/
│       └── values.yaml
│
├── k8s/
│   └── base/
│       ├── namespace.yaml
│       ├── configmap.yaml
│       ├── secret.example.yaml
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       ├── hpa.yaml
│       └── servicemonitor.yaml
│
├── load-test/
│
├── reports/
│   └── performance/
│       ├── database-indexing.md
│       ├── query-with-index.txt
│       └── query-without-index.txt
│
├── compose.yaml
└── README.md

# DevOps Performance & Scalability Platform

A production-style DevOps project demonstrating containerized application deployment,
Kubernetes orchestration, horizontal scaling, persistent storage, observability,
performance testing, and CI/CD automation.

The project uses a FastAPI application backed by PostgreSQL and Redis and deploys
the application to Kubernetes using Helm and Kubernetes manifests.

---

## Architecture

```text
                         Developer
                             |
                             v
                        GitHub Repository
                             |
                             v
                      GitHub Actions CI
                       /             \
                      /               \
                pytest             Docker Build
                                      |
                                      v
                                    GHCR
                                      |
                                      v
                         Kubernetes / Minikube
                                      |
                              NGINX Ingress
                                      |
                              performance.local
                                      |
                                      v
                         performance-api Service
                              (ClusterIP)
                                      |
                         +------------+------------+
                         |                         |
                         v                         v
                   API Pod 1                  API Pod 2
                         |                         |
                         +------------+------------+
                                      |
                           +----------+----------+
                           |                     |
                           v                     v
                     PostgreSQL               Redis
                     StatefulSet            StatefulSet
                           |                     |
                           v                     v
                         PVC                   PVC

                    +---------------------------+
                    |                           |
                    v                           v
                 Prometheus                 Grafana
                    |
                    v
              API /metrics

                    HPA
                     |
                     v
             API replicas: 2 -> 5
Local Development

Create and activate the Python virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

cd app
pip install -r requirements.txt

Run tests:

pytest

Expected result:

8 passed
Docker

Build the application image:

docker build -t devops-perfomance-api:test ./app

Run the container:

docker run --rm \
  -d \
  --name performance-api-test \
  -p 8001:8000 \
  devops-perfomance-api:test

Test:

curl http://localhost:8001/health

Stop the container:

docker stop performance-api-test
Kubernetes

The application is deployed into the:

performance-platform

namespace.

Create the namespace:

kubectl apply -f k8s/base/namespace.yaml

Apply configuration:

kubectl apply -f k8s/base/configmap.yaml
kubectl apply -f k8s/base/secret.yaml

Deploy the application:

kubectl apply -f k8s/base/deployment.yaml
kubectl apply -f k8s/base/service.yaml

Verify:

kubectl get pods -n performance-platform
PostgreSQL and Redis

PostgreSQL and Redis are deployed using Helm.

PostgreSQL

Configuration:

helm/postgresql/values.yaml

Install:

helm install performance-postgresql \
  bitnami/postgresql \
  -n performance-platform \
  -f helm/postgresql/values.yaml

PostgreSQL uses a persistent volume:

10Gi
Redis

Configuration:

helm/redis/values.yaml

Install:

helm install performance-redis \
  bitnami/redis \
  -n performance-platform \
  -f helm/redis/values.yaml

Redis uses a persistent volume:

1Gi

Check Helm releases:

helm list -n performance-platform
Database Initialization

The SQLAlchemy models are initialized using:

python -m src.init_db

Inside Kubernetes:

kubectl run db-init \
  --rm -it \
  --restart=Never \
  -n performance-platform \
  --image=ghcr.io/rithuraj6/devops-perfomance-api:latest \
  --image-pull-policy=IfNotPresent \
  --env="APP_ENV=production" \
  --env="DATABASE_HOST=performance-postgresql" \
  --env="DATABASE_PORT=5432" \
  --env="DATABASE_NAME=performance_db" \
  --env="DATABASE_USER=app_user" \
  --env="DATABASE_PASSWORD=app_password" \
  --command -- python -m src.init_db

The products table is created automatically from the SQLAlchemy model.

Persistent Storage Validation

PostgreSQL data was tested by creating a product and then restarting the
PostgreSQL StatefulSet pod.

Example query:

SELECT COUNT(*) FROM products;

Result:

 count
-------
     1

After deleting and recreating the PostgreSQL pod, the product remained available.

This demonstrates that the database is using persistent storage rather than
ephemeral container storage.

Redis persistence was also tested successfully using:

devops:persistence-test

with the value:

hello-kubernetes
Horizontal Pod Autoscaling

The API Deployment has:

Minimum replicas: 2
Maximum replicas: 5
CPU target: 60%

Check the HPA:

kubectl get hpa -n performance-platform

Example:

NAME                  REFERENCE                    TARGETS   MINPODS   MAXPODS   REPLICAS
performance-api-hpa   Deployment/performance-api   cpu: 1%/60%   2     5         2

During load testing the HPA successfully scaled the application:

2 replicas
   |
   v
3 replicas
   |
   v
4 replicas
   |
   v
5 replicas

After load was removed, the deployment scaled back toward the minimum.

Load Testing

Load was generated from inside the Kubernetes cluster:

kubectl run load-client \
  --rm -it \
  --restart=Never \
  -n performance-platform \
  --image=curlimages/curl \
  -- sh

Then:

while true; do
  curl -s http://performance-api:8000/api/products > /dev/null
done

The CPU load caused the HPA to increase the API replica count.

The Kubernetes metrics server was used to observe resource consumption:

kubectl top pods -n performance-platform
NGINX Ingress

NGINX Ingress was enabled in Minikube:

minikube addons enable ingress

Ingress configuration:

k8s/base/ingress.yaml

The application is exposed through:

performance.local

The local /etc/hosts configuration maps the hostname to the Minikube IP.

Verify:

curl -H "Host: performance.local" \
  http://192.168.49.2:30811/health

Expected:

{
  "status": "healthy"
}

API request:

curl -H "Host: performance.local" \
  http://192.168.49.2:30811/api/products
Monitoring

The project uses Prometheus and Grafana for observability.

Prometheus scrapes the API through a Kubernetes ServiceMonitor.

ServiceMonitor:

k8s/base/servicemonitor.yaml

The API exposes:

/metrics

Prometheus target verification confirmed both API pods as:

health: up

The application also exposes the metric:

http_requests_total

Example Prometheus query:

http_requests_total

Metrics include:

HTTP handler
HTTP method
HTTP status
Pod
Namespace
Service
Instance
Grafana

Grafana is used to visualize Kubernetes and application metrics.

Port-forward Grafana:

kubectl port-forward \
  -n monitoring \
  svc/monitoring-grafana \
  3000:80

Then access:

http://localhost:3000
CI/CD

GitHub Actions automatically runs on:

push to main
pull request to main

Workflow:

Git Push
   |
   v
GitHub Actions
   |
   v
Run pytest
   |
   | tests pass
   v
Docker Build
   |
   v
Login to GHCR
   |
   v
Push Docker Image
   |
   +----------------------------+
   |                            |
   v                            v
commit SHA tag              latest tag

Workflow file:

.github/workflows/ci.yml

The pipeline:

Checks out the repository.
Installs Python 3.12.
Installs application dependencies.
Runs pytest.
Builds the Docker image.
Authenticates to GHCR.
Pushes the image using both Git commit SHA and latest.
Container Registry

Images are published to GitHub Container Registry:

ghcr.io/rithuraj6/devops-perfomance-api

The Kubernetes Deployment currently consumes:

ghcr.io/rithuraj6/devops-perfomance-api:latest

The CI pipeline also publishes immutable commit-SHA tags.

Kubernetes Self-Healing

The API is managed by a Kubernetes Deployment with two replicas.

Pod failure was tested by deleting the API pods:

kubectl delete pod \
  -n performance-platform \
  -l app=performance-api

Kubernetes automatically created replacement pods.

This demonstrated Deployment-based self-healing.

PostgreSQL is managed by a StatefulSet, allowing its pod to be recreated
while retaining its persistent volume.

Helm Validation

Helm templates were rendered locally before deployment:

helm template performance-postgresql \
  bitnami/postgresql \
  --namespace performance-platform \
  -f helm/postgresql/values.yaml

Redis:

helm template performance-redis \
  bitnami/redis \
  --namespace performance-platform \
  -f helm/redis/values.yaml

Both charts were successfully deployed and verified.


Security

Sensitive Kubernetes credentials are not committed to Git.

The real secret file:

k8s/base/secret.yaml

is excluded through .gitignore.

Only the example template is committed:

k8s/base/secret.example.yaml

The example file contains placeholder values such as:

DATABASE_PASSWORD: "change-me"
REDIS_PASSWORD: "change-me"
Verification Summary

The following functionality has been tested successfully:

Feature	Status
FastAPI application	✅
Unit/API tests	✅ 8 passed
Docker build	✅
Docker container	✅
PostgreSQL	✅
Redis	✅
PostgreSQL persistent storage	✅
Redis persistent storage	✅
Kubernetes Deployment	✅
Kubernetes Service	✅
2 API replicas	✅
Pod self-healing	✅
HPA	✅ 2 → 5 replicas
Metrics Server	✅
NGINX Ingress	✅
Custom hostname	✅
Prometheus	✅
ServiceMonitor	✅
API metrics	✅
Grafana	✅
GitHub Actions	✅
GHCR image publishing	✅
GHCR → Kubernetes deployment	✅
Kubernetes/Helm validation	✅
Secrets excluded from Git	✅
Current Project Status
Phase 1 — Application Foundation

Completed

Phase 2 — Containerization

Completed

Phase 3 — Kubernetes Deployment

Completed

Phase 4 — Persistence

Completed

Phase 5 — Autoscaling

Completed

Phase 6 — Ingress

Completed

Phase 7 — Observability

Completed

Phase 8 — CI/CD

Completed
