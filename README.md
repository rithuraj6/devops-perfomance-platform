# DevOps Performance Platform

A production-style DevOps and Kubernetes performance engineering project demonstrating:

- Containerized FastAPI application
- PostgreSQL database
- Redis caching
- Kubernetes high availability
- Horizontal Pod Autoscaling
- Helm-based application deployment
- Argo CD GitOps continuous delivery
- Argo Rollouts progressive delivery
- Istio traffic management
- Canary deployments
- Prometheus monitoring
- Grafana dashboards
- K6 performance testing
- GitHub Actions CI
- Immutable application image versions
- Zero-downtime deployment strategy

> **Environment:** Local multi-node Kubernetes cluster using Minikube.
>
> The project is designed using production-style Kubernetes/GitOps patterns, but the current implementation is intentionally deployed on a local Minikube cluster rather than EKS/AKS/GKE.

---

# 1. Project Overview

The DevOps Performance Platform is a containerized FastAPI application deployed on a multi-node Kubernetes cluster.

The project demonstrates how a DevOps platform can combine:

```text
Developer
    |
    | git push
    v
GitHub Repository
    |
    v
GitHub Actions CI
    |
    +--> Run tests
    |
    +--> Build Docker image
    |
    +--> Push image to GHCR
    |
    +--> Update Helm desired state
    |
    +--> Commit and push to Git
    |
    v
Argo CD
    |
    | detects Git change
    v
Helm
    |
    v
Argo Rollouts
    |
    +--> Canary deployment
    |
    v
Istio
    |
    v
Kubernetes
    |
    +--> FastAPI
    +--> PostgreSQL
    +--> Redis

Observability and scaling operate independently:

FastAPI
   |
   | /metrics
   v
Prometheus
   |
   v
Grafana


CPU Usage
   |
   v
Metrics Server
   |
   v
HPA
   |
   v
Argo Rollout Pods
2. Architecture
Application Architecture
                         Internet / Client
                                |
                                v
                     Istio Ingress Gateway
                                |
                                v
                         Istio VirtualService
                                |
                                v
                       performance-api Service
                                |
                                v
                         Argo Rollout Pods
                         /              \
                        /                \
                 FastAPI Pod          FastAPI Pod
                        |                |
                        +-------+--------+
                                |
                 +--------------+--------------+
                 |                             |
                 v                             v
            PostgreSQL                       Redis
             Database                       Cache
DevOps Architecture
                         Developer
                            |
                            | git push
                            v
                     GitHub Repository
                            |
                            v
                    GitHub Actions CI
                     /       |       \
                    /        |        \
              pytest      Docker      Helm
                           build      update
                              |          |
                              v          v
                            GHCR      Git commit
                                         |
                                         v
                                      Argo CD
                                         |
                                         v
                                      Helm
                                         |
                                         v
                                  Argo Rollouts
                                         |
                                         v
                                       Istio
                                         |
                                         v
                                  Kubernetes
3. Technology Stack
Component	Technology
Application	Python / FastAPI
Database	PostgreSQL
Cache	Redis
Containerization	Docker
Orchestration	Kubernetes
Local Cluster	Minikube
Package Manager	Helm
CI	GitHub Actions
CD / GitOps	Argo CD
Progressive Delivery	Argo Rollouts
Traffic Management	Istio
Monitoring	Prometheus
Visualization	Grafana
Load Testing	K6
Container Registry	GitHub Container Registry
Application Protocol	HTTP / REST
4. Repository Structure
.
├── app/
│   ├── Dockerfile
│   ├── pytest.ini
│   ├── requirements.txt
│   ├── src/
│   │   ├── cache.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── init_db.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── routers/
│   │       └── products.py
│   └── tests/
│       ├── conftest.py
│       ├── test_health.py
│       └── test_products.py
│
├── helm/
│   ├── app/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   │       ├── configmap.yaml
│   │       ├── destination-rule.yaml
│   │       ├── gateway.yaml
│   │       ├── hpa.yaml
│   │       ├── ingress.yaml
│   │       ├── rollout.yaml
│   │       ├── secret.yaml
│   │       ├── service.yaml
│   │       ├── servicemonitor.yaml
│   │       └── virtual-service.yaml
│   │
│   ├── postgresql/
│   │   └── values.yaml
│   │
│   └── redis/
│       └── values.yaml
│
├── load-test/
│   └── api-load.js
│
├── reports/
│   ├── architecture/
│   ├── performance/
│   └── screenshots/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── compose.yaml
└── README.md

The application deployment manifests are managed through the Helm chart under:

helm/app/

The project does not use a second raw Kubernetes application-manifest deployment path.

5. Application

The application is built using FastAPI.

Main endpoints include:

GET /health
GET /ready
GET /metrics
GET /api/products
GET /api/products/{id}

Example:

curl http://performance.local/health

Expected response:

{
  "status": "healthy"
}

Readiness:

curl http://performance.local/ready

Expected response:

{
  "status": "ready"
}

Products:

curl http://performance.local/api/products
6. Docker

The application is containerized using Docker.

The Docker image is published to GitHub Container Registry:

ghcr.io/rithuraj6/devops-perfomance-api

The project intentionally does not use:

:latest

Application images are versioned using CI-generated build/version identifiers.

This provides traceability between:

Git commit
    |
    v
CI build
    |
    v
Docker image
    |
    v
Helm desired state
    |
    v
Kubernetes deployment
7. Kubernetes

The application runs on a multi-node Minikube Kubernetes cluster.

Example cluster:

Minikube Control Plane
        |
        +------------------+
        |                  |
        v                  v
     Node 1             Node 2
        |                  |
        +--------+---------+
                 |
                 v
          Application Pods

The application is configured with multiple replicas:

replicaCount: 2

Pod anti-affinity is used to prefer scheduling replicas on different Kubernetes nodes.

This reduces the impact of losing a single node.

8. High Availability

The FastAPI application is stateless and runs with multiple replicas.

Example:

performance-api
       |
       +---- Pod 1
       |
       +---- Pod 2

The Kubernetes Service provides stable access to the pods.

Readiness and liveness probes are configured:

/ready
/health

Readiness determines whether a pod can receive traffic.

Liveness determines whether Kubernetes should restart an unhealthy container.

9. Horizontal Pod Autoscaling

The application uses Kubernetes HPA.

Configuration:

Minimum replicas: 2
Maximum replicas: 5
CPU target: 60%

The HPA targets the Argo Rollout:

HPA
 |
 v
Argo Rollout
 |
 +---- Pod
 +---- Pod
 +---- Pod
 ...

During K6 load testing, CPU utilization increased and HPA scaled the application from:

2 replicas
     |
     v
3 replicas

After the load decreased, the replica count returned toward the configured minimum.

10. Helm

The application deployment is managed using Helm.

Main chart:

helm/app/

Validate the chart:

helm lint helm/app

Render the chart:

helm template performance-api helm/app

The Helm chart manages:

Rollout
Service
HPA
ConfigMap
Secret
ServiceMonitor
Istio Gateway
Istio VirtualService
Istio DestinationRule

This keeps the Kubernetes desired state version-controlled and reproducible.

11. GitOps with Argo CD

Argo CD is responsible for Continuous Delivery.

The Git repository acts as the source of truth.

The deployment flow is:

GitHub Actions
      |
      | update Helm values
      |
      v
Git Repository
      |
      | Argo CD detects change
      v
Argo CD
      |
      v
Helm rendering
      |
      v
Kubernetes

GitHub Actions does not directly deploy the application.

There is no:

kubectl apply
kubectl set image
kubectl patch

deployment step in CI.

Instead, CI updates the desired Helm state and pushes the change to Git.

Argo CD then reconciles the Kubernetes cluster with Git.

12. Continuous Integration

GitHub Actions performs CI tasks.

The pipeline performs:

Git Push
   |
   v
Run tests
   |
   v
Build Docker image
   |
   v
Push image to GHCR
   |
   v
Update Helm image version
   |
   v
Commit desired state
   |
   v
Push to Git

The application tests are executed using:

pytest

The pipeline only builds and publishes the application when appropriate.

13. Dynamic Build Version

The application image version is generated dynamically by GitHub Actions.

The important principle is:

Do NOT hardcode:

image:
  tag: latest

Instead:

CI Build
   |
   | dynamic build/version number
   v
GHCR image
   |
   v
helm/app/values.yaml
   |
   v
Argo CD

This makes every deployment traceable to a specific CI build.

For example:

Build 42
   |
   v
ghcr.io/rithuraj6/devops-perfomance-api:42
   |
   v
Helm values
   |
   v
Argo CD

The build number is therefore passed dynamically from CI into the GitOps desired state.

14. Canary Deployment

Argo Rollouts manages progressive delivery.

The current Rollout strategy is Canary.

Example progression:

Stable
  |
  | 10%
  v
Canary
  |
  | 25%
  v
Canary
  |
  | 50%
  v
Canary
  |
  | 75%
  v
Canary
  |
  | 100%
  v
Stable

Configured progression:

10%
25%
50%
75%
100%

Pauses are included between stages.

This allows the new version to receive gradually increasing traffic instead of immediately receiving 100% of production traffic.

15. Istio Traffic Management

Istio is used for service-to-service traffic management and progressive delivery.

The application uses:

Istio Gateway
       |
       v
VirtualService
       |
       v
DestinationRule
       |
       +---- stable
       |
       +---- canary

The Argo Rollouts controller dynamically manages the stable and canary subsets.

Example:

route:
  - destination:
      host: performance-api
      subset: stable
    weight: 100

  - destination:
      host: performance-api
      subset: canary
    weight: 0

During a canary rollout, these weights are adjusted by Argo Rollouts.

16. Zero-Downtime Deployment

Zero-downtime behavior is achieved using:

Multiple application replicas
Kubernetes Service
Readiness probes
Liveness probes
Argo Rollouts
Progressive traffic shifting
Istio traffic management
Controlled rollout progression

Traffic is shifted gradually instead of replacing all application pods simultaneously.

17. Blue-Green Deployment

The project also includes Blue-Green deployment design as part of the progressive delivery requirement.

The concept is:

                 Traffic
                    |
                    v
               Active Service
                    |
                    v
                 BLUE
                    |
              switch traffic
                    |
                    v
                 GREEN

Blue-Green deployment maintains two application environments:

BLUE  = current version
GREEN = new version

Traffic can then be switched between them.

The active Canary configuration remains the primary live deployment strategy used for the performance demonstration, while the Blue-Green approach is retained as a supported progressive-delivery strategy for the project requirement.

18. PostgreSQL

PostgreSQL is used as the application database.

The database is deployed in Kubernetes using Helm.

Database configuration includes:

Database:
performance_db

User:
app_user

Port:
5432

Persistent storage is configured using a Kubernetes PersistentVolumeClaim.

Example storage:

10Gi

Database data was validated after restarting the database workload.

Existing sample data includes products such as:

Kubernetes Laptop
DevOps Monitor
19. Redis

Redis is used as the application caching layer.

Redis is also deployed using Helm.

Example persistence:

1Gi

The application uses Redis to reduce repeated database access and improve response performance.

Architecture:

Client
  |
  v
FastAPI
  |
  +---- Cache hit ----> Redis
  |
  +---- Cache miss ---> PostgreSQL
20. Prometheus Monitoring

The FastAPI application exposes Prometheus metrics through:

/metrics

A Kubernetes ServiceMonitor is managed through Helm:

helm/app/templates/servicemonitor.yaml

Prometheus discovers the application through the ServiceMonitor.

Important application metrics include:

http_requests_total
http_request_duration_seconds_bucket
http_request_duration_seconds_count
http_request_duration_seconds_sum

Prometheus was verified to scrape both application pods successfully.

21. Grafana

Grafana is used to visualize application and Kubernetes performance.

The dashboard includes:

API request rate
HPA replica count
HPA desired replicas
P95 latency
CPU utilization

Example monitoring flow:

Application
     |
     v
Prometheus
     |
     v
Grafana

The dashboard provides visibility into application behavior during load testing and deployments.

22. Performance Testing

K6 is used for HTTP load testing.

Test script:

load-test/api-load.js

The test gradually increases traffic:

10 VUs
   |
   v
25 VUs
   |
   v
50 VUs
   |
   v
0 VUs

The test validates:

HTTP success rate
Response latency
Request throughput
Application scalability
HPA behavior
23. Performance Test Results

A full K6 test was executed against:

GET /api/products

Test duration:

3 minutes

Maximum virtual users:

50

Results:

Metric	Result
Total requests	4,144
Average throughput	22.96 req/s
HTTP failures	0.00%
P95 latency	18.43 ms
Maximum VUs	50
Checks passed	100%

The application successfully handled the load without HTTP request failures.

24. HPA Performance During Load

During the K6 test, CPU utilization increased sufficiently to trigger HPA scaling.

Observed behavior:

Initial replicas
      |
      v
     2
      |
      | increased CPU load
      v
     3

The HPA configuration was:

minReplicas: 2
maxReplicas: 5
CPU target: 60%

This demonstrates that the application can automatically scale based on CPU utilization.

25. Prometheus P95 Latency

Prometheus was also used to calculate application request latency.

Example PromQL:

histogram_quantile(
  0.95,
  sum by (le) (
    rate(http_request_duration_seconds_bucket{
      namespace="performance-platform",
      handler="/api/products",
      method="GET"
    }[5m])
  )
)

An observed value during monitoring was approximately:

95 ms

The K6 end-to-end test reported a lower P95 during its measured run:

18.43 ms

The difference is expected because the measurements come from different observation windows and measurement layers.

26. CPU Monitoring

Application CPU utilization can be queried using Prometheus.

Example:

sum by (pod) (
  rate(
    container_cpu_usage_seconds_total{
      namespace="performance-platform",
      pod=~"performance-api-.*",
      cpu="total"
    }[5m]
  )
) * 100

This allows CPU utilization to be correlated with HPA scaling behavior.

27. Health Validation

Application health was validated through Istio ingress.

Health:

curl -i http://performance.local/health

Readiness:

curl -i http://performance.local/ready

Products:

curl -i http://performance.local/api/products

Individual product:

curl -i http://performance.local/api/products/1

All tested endpoints returned successful responses.

28. Useful Commands
Kubernetes
kubectl get nodes
kubectl get pods -n performance-platform
kubectl get rollout -n performance-platform
kubectl get hpa -n performance-platform
kubectl get svc -n performance-platform
Argo Rollouts
kubectl argo rollouts get rollout performance-api \
  -n performance-platform

Watch rollout:

kubectl argo rollouts get rollout performance-api \
  -n performance-platform \
  --watch
Helm

Lint:

helm lint helm/app

Render:

helm template performance-api helm/app
Prometheus

Port-forward:

kubectl port-forward \
  -n monitoring \
  svc/monitoring-kube-prometheus-prometheus \
  9090:9090
Grafana

Port-forward:

kubectl port-forward \
  -n monitoring \
  svc/monitoring-grafana \
  3000:80
29. GitOps Deployment Flow

The complete deployment lifecycle is:

1. Developer changes application
             |
             v
2. git push
             |
             v
3. GitHub Actions starts
             |
             +---- pytest
             |
             +---- Docker build
             |
             +---- Push image to GHCR
             |
             +---- Generate build/version
             |
             +---- Update Helm values
             |
             +---- Commit desired state
             |
             v
4. GitHub repository changes
             |
             v
5. Argo CD detects Git change
             |
             v
6. Argo CD renders Helm chart
             |
             v
7. Argo Rollouts creates new ReplicaSet
             |
             v
8. Istio controls traffic
             |
             v
9. Canary progression
             |
             v
10. New version becomes stable

This separates:

CI = GitHub Actions
CD = Argo CD
Progressive Delivery = Argo Rollouts
Traffic Management = Istio