# DevOps Performance & Scalability Platform

A production-style DevOps project demonstrating:

- Containerized FastAPI application
- Kubernetes high availability
- Multi-node Kubernetes deployment
- Horizontal Pod Autoscaling
- NGINX Ingress
- Canary deployment
- Blue-Green deployment
- GitHub Actions CI/CD
- Prometheus and Grafana monitoring
- k6 performance testing
- PostgreSQL with persistent storage
- Redis caching
- PostgreSQL indexing and query optimization

> The implementation was validated on a local 2-node Minikube cluster.
> The Kubernetes manifests are designed to demonstrate the required
> Kubernetes concepts without claiming an EKS deployment.

---

## Architecture

```text
                         Developer
                             |
                             v
                     GitHub Repository
                             |
                             v
                       GitHub Actions
                       CI Pipeline
                      /           \
                 pytest        Docker Build
                                  |
                                  v
                                GHCR
                                  |
                                  v
                     Self-Hosted Runner
                                  |
                                  v
                         2-Node Minikube
                                  |
                           NGINX Ingress
                                  |
                   +--------------+--------------+
                   |                             |
                   v                             v
          performance.local          bluegreen.performance.local
                   |                             |
                   v                             v
          performance-api              performance-api-bg
             Service                     Service
                   |                    /           \
                   |                   /             \
                   v                  v               v
             API Pods              BLUE            GREEN
             2 replicas           2 pods           2 pods
                   |
          +--------+--------+
          |                 |
          v                 v
      PostgreSQL          Redis
      StatefulSet         StatefulSet
          |                 |
          v                 v
         PVC               PVC

              Prometheus
                   |
              ServiceMonitor
                   |
                   v
                Grafana

                 HPA
                  |
                  v
          API replicas: 2 → 5
Technology Stack
Python
FastAPI
Docker
Kubernetes
Minikube
NGINX Ingress
Helm
GitHub Actions
GitHub Container Registry
Prometheus
Grafana
PostgreSQL
Redis
k6
Repository Structure
devops-perfomance-platform/
│
├── app/
│   ├── src/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
├── helm/
│   ├── postgresql/
│   │   └── values.yaml
│   └── redis/
│       └── values.yaml
│
├── k8s/
│   ├── base/
│   └── ingress/
│       ├── blue-deployment.yaml
│       ├── green-deployment.yaml
│       ├── bluegreen-service.yaml
│       └── bluegreen-ingress.yaml
│
├── load-test/
│   └── api-load.js
│
├── reports/
│   └── performance/
│       ├── database-indexing.md
│       ├── k6-results.md
│       ├── query-with-index.txt
│       └── query-without-index.txt
│
├── compose.yaml
└── README.md
Application

The application is implemented using FastAPI.

Main API endpoint:

GET /api/products

Health endpoints:

GET /health
GET /ready

Prometheus metrics:

GET /metrics

The application uses:

PostgreSQL for persistent data
Redis for caching
SQLAlchemy for database access
Prometheus instrumentation for HTTP metrics
Local Development

Create a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

cd app
pip install -r requirements.txt

Run tests:

pytest

Expected:

8 passed
Docker

Build:

docker build -t devops-perfomance-api:test ./app

Run:

docker run --rm \
  -d \
  --name performance-api-test \
  -p 8001:8000 \
  devops-perfomance-api:test

Test:

curl http://localhost:8001/health
Kubernetes

The application runs in:

performance-platform

namespace.

The application Deployment is configured with:

2 initial replicas
CPU requests/limits
Readiness probe
Liveness probe
Pod anti-affinity
RollingUpdate strategy

The two API replicas were validated across the two Minikube nodes.

Example:

kubectl get pods -n performance-platform -o wide
High Availability

The Kubernetes cluster consists of two nodes:

minikube
minikube-m02

The API uses pod anti-affinity to prefer scheduling replicas on different Kubernetes nodes.

This provides node-level distribution for the API workload.

The application is stateless, with state stored externally in PostgreSQL and Redis.

Horizontal Pod Autoscaling

The HPA configuration uses:

Minimum replicas: 2
Maximum replicas: 5
CPU target: 60%

Check:

kubectl get hpa -n performance-platform

The final performance test reached 50 VUs successfully while maintaining two API replicas because CPU utilization remained below the configured scaling threshold.

The HPA was therefore configured and operational, but the final k6 workload did not force a scale-up event.

PostgreSQL

PostgreSQL is deployed using the Bitnami Helm chart.

Configuration:

helm/postgresql/values.yaml

Features:

Persistent storage
10Gi volume
Resource requests/limits
Database initialization through SQLAlchemy
Non-root container security context

Install:

helm install performance-postgresql \
  bitnami/postgresql \
  -n performance-platform \
  -f helm/postgresql/values.yaml
Redis

Redis is deployed using Helm.

Configuration:

helm/redis/values.yaml

Features:

Standalone Redis
Authentication
Persistent storage
1Gi volume
Resource requests/limits

Install:

helm install performance-redis \
  bitnami/redis \
  -n performance-platform \
  -f helm/redis/values.yaml
Redis Caching

The /api/products endpoint uses Redis caching.

Cache key:

products:list

Cache TTL:

60 seconds

Individual products use:

product:<id>

The cache reduces repeated PostgreSQL queries for frequently accessed product data.

Database Indexing

The products.category column is indexed using SQLAlchemy:

category = mapped_column(
    String(100),
    nullable=False,
    index=True,
)

Query execution results are documented in:

reports/performance/database-indexing.md

The repository contains both indexed and non-indexed query results for comparison.

NGINX Ingress

NGINX Ingress is used for HTTP routing.

The primary application hostname is:

performance.local

The Minikube NGINX controller is exposed through NodePort:

30900

Example:

curl -H "Host: performance.local" \
  http://192.168.49.2:30900/api/products
Canary Deployment

A canary deployment was demonstrated using:

Separate canary Deployment
Separate canary Service
NGINX Canary Ingress
10% configured canary weight

The canary pod reached Ready state and NGINX logs confirmed requests reaching the canary upstream.

The temporary canary resources were removed after validation to keep the final cluster state clean.

The test did not claim an exact 10% measured traffic distribution.

Blue-Green Deployment

Blue-Green deployment uses two independent environments:

performance-api-blue
performance-api-green

Both environments run simultaneously.

The traffic Service:

performance-api-bg

initially selects:

version: blue

Traffic can be switched to Green by changing the selector to:

version: green

The Blue → Green cutover was successfully demonstrated.

Before:

performance-api-bg
        |
        +--> Blue Pod
        +--> Blue Pod

After:

performance-api-bg
        |
        +--> Green Pod
        +--> Green Pod

The application remained available during the switch.

Monitoring

Prometheus and Grafana are used for observability.

The API exposes:

/metrics

Prometheus discovers the application through:

k8s/base/servicemonitor.yaml

Important metrics include:

http_requests_total
http_request_duration_seconds

Grafana dashboard includes:

API request rate
P95 latency
HPA replica count
HPA desired replicas

Observed P95 latency in Grafana:

~95 ms
Performance Testing

Load testing uses k6.

Test script:

load-test/api-load.js

Load profile:

30s → 10 VUs
60s → 25 VUs
60s → 50 VUs
30s → ramp down

Maximum:

50 VUs

Final test results:

Metric	Result
Requests	4,169
Throughput	23.10 req/s
Failed requests	0.00%
Successful checks	100%
Average latency	1.89 ms
Median latency	1.67 ms
P90	2.29 ms
P95	2.64 ms
Maximum latency	60.72 ms
Maximum VUs	50

Thresholds:

P95 < 1000 ms     PASS
Failure rate < 1% PASS

Full report:

reports/performance/k6-results.md

These results represent the local Minikube environment and should not be interpreted as production-scale capacity.

CI/CD
Continuous Integration

GitHub Actions runs CI on:

Push to main
Pull requests to main

Pipeline:

Git Push
   |
   v
pytest
   |
   v
Docker Build
   |
   v
GHCR

The Docker image is published using:

<git-sha>
latest

Workflow:

.github/workflows/ci.yml
Continuous Deployment

CD uses a GitHub self-hosted runner running on the Kubernetes host.

Workflow:

.github/workflows/cd.yml

The CD pipeline:

Checks out the repository.
Verifies Kubernetes access.
Applies Blue-Green resources.
Deploys the immutable Git SHA image to Green.
Waits for the Green rollout.
Verifies Green pods.
Switches the Blue-Green Service to Green.
Verifies Green endpoints.
Performs an application health check.

The deployment image uses:

ghcr.io/rithuraj6/devops-perfomance-api:<git-sha>

rather than relying exclusively on latest.

The CD workflow is currently manually triggered using:

workflow_dispatch

This was intentional during validation to prevent an automatic local-cluster deployment on every push.

Self-Healing

The API is managed by a Kubernetes Deployment.

If an API pod fails, Kubernetes automatically creates a replacement pod.

This demonstrates Kubernetes Deployment-based self-healing.

PostgreSQL is managed using a StatefulSet with persistent storage, allowing its pod to be recreated without losing persisted database data.

Persistent Storage

PostgreSQL uses a persistent volume:

10Gi

Redis uses:

1Gi

Persistence was validated by restarting the database workloads and verifying that stored data remained available.

Security

Sensitive Kubernetes credentials are excluded from Git.

The real secret:

k8s/base/secret.yaml

is ignored using .gitignore.

Only:

k8s/base/secret.example.yaml

is committed.

The example contains placeholder credentials.

The application containers also use a non-root user.

Verification Summary
Feature	Status
FastAPI application	✅
Automated application tests	✅
Docker build	✅
GHCR image publishing	✅
2-node Kubernetes cluster	✅
API high availability	✅
Pod anti-affinity	✅
Kubernetes self-healing	✅
HPA	✅
NGINX Ingress	✅
Canary deployment demonstration	✅
Blue-Green deployment	✅
Blue → Green cutover	✅
GitHub Actions CI	✅
GitHub Actions CD	✅
Self-hosted runner	✅
PostgreSQL Helm deployment	✅
PostgreSQL persistence	✅
PostgreSQL indexing	✅
Redis Helm deployment	✅
Redis caching	✅
Redis persistence	✅
Prometheus	✅
Grafana	✅
ServiceMonitor	✅
k6 performance testing	✅
Performance report	✅
Kubernetes secrets excluded from Git	✅
Project Status
Phase 1 — Application Foundation

✅ Completed

Phase 2 — Containerization

✅ Completed

Phase 3 — Kubernetes Deployment

✅ Completed

Phase 4 — Persistence

✅ Completed

Phase 5 — Autoscaling

✅ Completed

Phase 6 — Ingress & Traffic Management

✅ Completed

Phase 7 — Observability

✅ Completed

Phase 8 — Performance Testing

✅ Completed

Phase 9 — Blue-Green Deployment

✅ Completed

Phase 10 — CI/CD

✅ Completed
