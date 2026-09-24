<div align="center">

# ⚡ DevOps Performance Platform
### Production-Style Kubernetes & GitOps Performance Engineering

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=00C7B7)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)

![ArgoCD](https://img.shields.io/badge/Argo%20CD-EF7B4D?style=flat-square&logo=argo&logoColor=white)
![ArgoRollouts](https://img.shields.io/badge/Argo%20Rollouts-F4511E?style=flat-square&logo=argo&logoColor=white)
![Istio](https://img.shields.io/badge/Istio-466BB0?style=flat-square&logo=istio&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-0F1689?style=flat-square&logo=helm&logoColor=white)
![GitHubActions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white)
![K6](https://img.shields.io/badge/K6-7D64FF?style=flat-square&logo=k6&logoColor=white)

![HPA](https://img.shields.io/badge/HPA-enabled-brightgreen?style=flat-square)
![Zero Downtime](https://img.shields.io/badge/deployments-zero--downtime-success?style=flat-square)
![Failures](https://img.shields.io/badge/HTTP%20failures-0.00%25-brightgreen?style=flat-square)
![P95](https://img.shields.io/badge/P95%20latency-18.43ms-blue?style=flat-square)
![Cluster](https://img.shields.io/badge/cluster-Minikube-informational?style=flat-square)

</div>

<br>

A production-style DevOps and Kubernetes **performance engineering** project demonstrating a full path from commit to canary rollout — containerized FastAPI, GitOps delivery, progressive traffic shifting, autoscaling, and full observability.

> 🧪 **Environment:** Local multi-node Kubernetes cluster using **Minikube.**
> The project is designed using production-style Kubernetes/GitOps patterns, but is intentionally deployed on a local Minikube cluster rather than EKS/AKS/GKE.

<br>

## ✨ What This Project Demonstrates

<table>
<tr>
<td valign="top" width="33%">

**🏗️ Platform**
- Containerized FastAPI app
- PostgreSQL database
- Redis caching
- Kubernetes high availability
- Horizontal Pod Autoscaling
- Immutable image versions
- Zero-downtime deployments

</td>
<td valign="top" width="33%">

**🔄 Delivery**
- Helm-based deployment
- Argo CD GitOps
- Argo Rollouts (canary)
- Istio traffic management
- Blue-green design
- GitHub Actions CI

</td>
<td valign="top" width="33%">

**📊 Observability**
- Prometheus monitoring
- Grafana dashboards
- K6 performance testing
- P95 latency tracking
- CPU-driven autoscaling

</td>
</tr>
</table>

<br>

## 1️⃣ Project Overview

The DevOps Performance Platform is a containerized FastAPI application deployed on a multi-node Kubernetes cluster, combining **CI, GitOps delivery, progressive rollout, service mesh routing, and observability-driven autoscaling.**

```mermaid
flowchart TD
    Dev([👨‍💻 Developer]) -->|git push| GH[(📦 GitHub Repository)]
    GH --> CI[⚙️ GitHub Actions CI]

    subgraph CIPIPE[" "]
        direction LR
        T[🧪 Run Tests] --> B[🐳 Build Image]
        B --> P[📤 Push to GHCR]
        P --> U[📝 Update Helm State]
        U --> C[✅ Commit & Push]
    end

    CI --> CIPIPE
    CIPIPE --> ACD[🔄 Argo CD]
    ACD -->|detects Git change| HL[📦 Helm]
    HL --> AR[🚀 Argo Rollouts]
    AR -->|canary| IS[🔀 Istio]
    IS --> K8S[☸️ Kubernetes]

    K8S --> F[🧩 FastAPI]
    K8S --> PG[(🗄️ PostgreSQL)]
    K8S --> R[(⚡ Redis)]

    style Dev fill:#6366f1,color:#fff,stroke:#4338ca
    style GH fill:#24292e,color:#fff,stroke:#000
    style CI fill:#2088FF,color:#fff,stroke:#0b5ed7
    style ACD fill:#EF7B4D,color:#fff,stroke:#c2531f
    style HL fill:#0F1689,color:#fff,stroke:#000060
    style AR fill:#F4511E,color:#fff,stroke:#b8340f
    style IS fill:#466BB0,color:#fff,stroke:#2d4a80
    style K8S fill:#326CE5,color:#fff,stroke:#1e40af
    style F fill:#00C7B7,color:#000,stroke:#059669
    style PG fill:#4169E1,color:#fff,stroke:#1e3a8a
    style R fill:#DC382D,color:#fff,stroke:#991b1b
```

**Observability and scaling operate independently of the delivery pipeline:**

```mermaid
flowchart LR
    F[🧩 FastAPI /metrics] --> P[📈 Prometheus]
    P --> G[📊 Grafana]

    CPU[📟 CPU Usage] --> MS[📏 Metrics Server]
    MS --> HPA[📐 HPA]
    HPA --> RP[🚀 Argo Rollout Pods]

    style F fill:#00C7B7,color:#000
    style P fill:#E6522C,color:#fff
    style G fill:#F46800,color:#fff
    style HPA fill:#22c55e,color:#fff
    style RP fill:#F4511E,color:#fff
```

<br>

## 2️⃣ Architecture

### 🧩 Application Architecture

```mermaid
flowchart TD
    Client([🌐 Internet / Client]) --> GW[🚪 Istio Ingress Gateway]
    GW --> VS[🔀 Istio VirtualService]
    VS --> SVC[🧭 performance-api Service]
    SVC --> RP{Argo Rollout Pods}
    RP --> P1[🧩 FastAPI Pod]
    RP --> P2[🧩 FastAPI Pod]
    P1 --> PG[(🗄️ PostgreSQL)]
    P1 --> R[(⚡ Redis)]
    P2 --> PG
    P2 --> R

    style Client fill:#6366f1,color:#fff
    style GW fill:#466BB0,color:#fff
    style VS fill:#466BB0,color:#fff
    style SVC fill:#0ea5e9,color:#fff
    style P1 fill:#00C7B7,color:#000
    style P2 fill:#00C7B7,color:#000
    style PG fill:#4169E1,color:#fff
    style R fill:#DC382D,color:#fff
```

### ⚙️ DevOps Architecture

```mermaid
flowchart TD
    Dev([👨‍💻 Developer]) -->|git push| GH[(📦 GitHub Repository)]
    GH --> CI[⚙️ GitHub Actions CI]
    CI --> PT[🧪 pytest]
    CI --> DB[🐳 Docker Build]
    CI --> HU[📝 Helm Update]
    DB --> GHCR[(📦 GHCR)]
    HU --> GC[✅ Git Commit]
    GHCR --> ACD[🔄 Argo CD]
    GC --> ACD
    ACD --> HL[📦 Helm]
    HL --> AR[🚀 Argo Rollouts]
    AR --> IS[🔀 Istio]
    IS --> K8S[☸️ Kubernetes]

    style Dev fill:#6366f1,color:#fff
    style GH fill:#24292e,color:#fff
    style CI fill:#2088FF,color:#fff
    style GHCR fill:#2496ED,color:#fff
    style ACD fill:#EF7B4D,color:#fff
    style AR fill:#F4511E,color:#fff
    style IS fill:#466BB0,color:#fff
    style K8S fill:#326CE5,color:#fff
```

<br>

## 3️⃣ Technology Stack

| Component | Technology |
|---|---|
| 🧩 **Application** | Python / FastAPI |
| 🗄️ **Database** | PostgreSQL |
| ⚡ **Cache** | Redis |
| 🐳 **Containerization** | Docker |
| ☸️ **Orchestration** | Kubernetes |
| 🧪 **Local Cluster** | Minikube |
| 📦 **Package Manager** | Helm |
| ⚙️ **CI** | GitHub Actions |
| 🔄 **CD / GitOps** | Argo CD |
| 🚀 **Progressive Delivery** | Argo Rollouts |
| 🔀 **Traffic Management** | Istio |
| 📈 **Monitoring** | Prometheus |
| 📊 **Visualization** | Grafana |
| 🧪 **Load Testing** | K6 |
| 📦 **Container Registry** | GitHub Container Registry |
| 🌐 **Application Protocol** | HTTP / REST |

<br>

## 4️⃣ Repository Structure

```
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
```

> ℹ️ Application deployment manifests are managed entirely through the Helm chart under `helm/app/`. The project does not use a second raw Kubernetes manifest deployment path.

<br>

## 5️⃣ Application

Built using **FastAPI**. Main endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Liveness check |
| `GET` | `/ready` | Readiness check |
| `GET` | `/metrics` | Prometheus metrics |
| `GET` | `/api/products` | List products |
| `GET` | `/api/products/{id}` | Get a single product |

```bash
curl http://performance.local/health
# { "status": "healthy" }

curl http://performance.local/ready
# { "status": "ready" }

curl http://performance.local/api/products
```

<br>

## 6️⃣ Docker

The application is containerized using Docker and published to **GitHub Container Registry**:

```
ghcr.io/rithuraj6/devops-perfomance-api
```

🚫 The project intentionally **does not** use `:latest`. Every image is versioned with a CI-generated build identifier, giving full traceability:

```mermaid
flowchart LR
    A[🔀 Git Commit] --> B[⚙️ CI Build]
    B --> C[🐳 Docker Image]
    C --> D[📦 Helm Desired State]
    D --> E[☸️ Kubernetes Deployment]

    style A fill:#24292e,color:#fff
    style B fill:#2088FF,color:#fff
    style C fill:#2496ED,color:#fff
    style D fill:#0F1689,color:#fff
    style E fill:#326CE5,color:#fff
```

<br>

## 7️⃣ Kubernetes

The application runs on a **multi-node Minikube** cluster.

```mermaid
flowchart TD
    CP[🎛️ Minikube Control Plane] --> N1[🖥️ Node 1]
    CP --> N2[🖥️ Node 2]
    N1 --> Pods[📦 Application Pods]
    N2 --> Pods

    style CP fill:#326CE5,color:#fff
    style N1 fill:#0ea5e9,color:#fff
    style N2 fill:#0ea5e9,color:#fff
    style Pods fill:#22c55e,color:#fff
```

```yaml
replicaCount: 2
```

Pod anti-affinity is used to prefer scheduling replicas on **different nodes**, reducing the impact of losing a single node.

<br>

## 8️⃣ High Availability

The FastAPI application is **stateless** and runs with multiple replicas behind a stable Kubernetes Service.

```mermaid
flowchart LR
    SVC[🧭 performance-api Service] --> P1[📦 Pod 1]
    SVC --> P2[📦 Pod 2]

    style SVC fill:#0ea5e9,color:#fff
    style P1 fill:#22c55e,color:#fff
    style P2 fill:#22c55e,color:#fff
```

| Probe | Path | Purpose |
|---|---|---|
| 🟢 Readiness | `/ready` | Determines whether a pod can receive traffic |
| ❤️ Liveness | `/health` | Determines whether Kubernetes should restart an unhealthy container |

<br>

## 9️⃣ Horizontal Pod Autoscaling

| Setting | Value |
|---|---|
| Minimum replicas | `2` |
| Maximum replicas | `5` |
| CPU target | `60%` |

```mermaid
flowchart TD
    HPA[📐 HPA] --> R[🚀 Argo Rollout]
    R --> P1[📦 Pod]
    R --> P2[📦 Pod]
    R --> P3[📦 Pod ...]

    style HPA fill:#22c55e,color:#fff
    style R fill:#F4511E,color:#fff
```

During K6 load testing, CPU utilization increased and HPA scaled the application:

<div align="center">

**2 replicas → 3 replicas** (under load) → back toward minimum after load decreased

</div>

<br>

## 🔟 Helm

Deployment is fully managed via Helm.

```bash
# Validate
helm lint helm/app

# Render
helm template performance-api helm/app
```

The Helm chart manages: `Rollout` · `Service` · `HPA` · `ConfigMap` · `Secret` · `ServiceMonitor` · `Istio Gateway` · `Istio VirtualService` · `Istio DestinationRule`

This keeps the Kubernetes desired state **version-controlled and reproducible.**

<br>

## 1️⃣1️⃣ GitOps with Argo CD

Argo CD handles **Continuous Delivery** — the Git repository is the single source of truth.

```mermaid
flowchart TD
    CI[⚙️ GitHub Actions] -->|update Helm values| GH[(📦 Git Repository)]
    GH -->|detects change| ACD[🔄 Argo CD]
    ACD --> HR[📦 Helm Rendering]
    HR --> K8S[☸️ Kubernetes]

    style CI fill:#2088FF,color:#fff
    style GH fill:#24292e,color:#fff
    style ACD fill:#EF7B4D,color:#fff
    style HR fill:#0F1689,color:#fff
    style K8S fill:#326CE5,color:#fff
```

> 🚫 GitHub Actions **never** runs `kubectl apply`, `kubectl set image`, or `kubectl patch` as a deployment step. CI only updates the desired Helm state and pushes to Git — **Argo CD reconciles the cluster.**

<br>

## 1️⃣2️⃣ Continuous Integration

```mermaid
flowchart LR
    A[🔀 Git Push] --> B[🧪 Run Tests]
    B --> C[🐳 Build Image]
    C --> D[📤 Push to GHCR]
    D --> E[📝 Update Helm Version]
    E --> F[✅ Commit Desired State]
    F --> G[📤 Push to Git]

    style A fill:#24292e,color:#fff
    style B fill:#f59e0b,color:#fff
    style C fill:#2496ED,color:#fff
    style D fill:#2496ED,color:#fff
    style E fill:#0F1689,color:#fff
    style G fill:#22c55e,color:#fff
```

Application tests run with **pytest**, and the pipeline only builds/publishes when appropriate.

<br>

## 1️⃣3️⃣ Dynamic Build Versioning

🚫 **Never hardcode** `image.tag: latest`.

```mermaid
flowchart LR
    A[⚙️ CI Build] -->|dynamic version| B[📦 GHCR Image]
    B --> C[📝 helm/app/values.yaml]
    C --> D[🔄 Argo CD]

    style A fill:#2088FF,color:#fff
    style B fill:#2496ED,color:#fff
    style C fill:#0F1689,color:#fff
    style D fill:#EF7B4D,color:#fff
```

**Example:**

```
Build 42 → ghcr.io/rithuraj6/devops-perfomance-api:42 → Helm values → Argo CD
```

Every deployment is traceable to a specific CI build number.

<br>

## 1️⃣4️⃣ Canary Deployment

Argo Rollouts manages progressive delivery using a **Canary** strategy.

```mermaid
flowchart LR
    S[🟦 Stable] -->|10%| C1[🟪 Canary]
    C1 -->|25%| C2[🟪 Canary]
    C2 -->|50%| C3[🟪 Canary]
    C3 -->|75%| C4[🟪 Canary]
    C4 -->|100%| NS[🟦 New Stable]

    style S fill:#0ea5e9,color:#fff
    style C1 fill:#8b5cf6,color:#fff
    style C2 fill:#8b5cf6,color:#fff
    style C3 fill:#8b5cf6,color:#fff
    style C4 fill:#8b5cf6,color:#fff
    style NS fill:#0ea5e9,color:#fff
```

| Stage | Traffic to Canary |
|:---:|:---:|
| 1 | 🟪 10% |
| 2 | 🟪🟪 25% |
| 3 | 🟪🟪🟪🟪🟪 50% |
| 4 | 🟪🟪🟪🟪🟪🟪🟪 75% |
| 5 | 🟪🟪🟪🟪🟪🟪🟪🟪🟪🟪 100% |

Pauses are included between stages so the new version receives **gradually increasing traffic** instead of an immediate 100% cutover.

<br>

## 1️⃣5️⃣ Istio Traffic Management

```mermaid
flowchart TD
    GW[🚪 Istio Gateway] --> VS[🔀 VirtualService]
    VS --> DR[📐 DestinationRule]
    DR --> STB[🟦 stable]
    DR --> CAN[🟪 canary]

    style GW fill:#466BB0,color:#fff
    style VS fill:#466BB0,color:#fff
    style DR fill:#466BB0,color:#fff
    style STB fill:#0ea5e9,color:#fff
    style CAN fill:#8b5cf6,color:#fff
```

```yaml
route:
  - destination:
      host: performance-api
      subset: stable
    weight: 100

  - destination:
      host: performance-api
      subset: canary
    weight: 0
```

During a canary rollout, these weights are **dynamically adjusted by Argo Rollouts.**

<br>

## 1️⃣6️⃣ Zero-Downtime Deployment

Achieved through the combination of:

✅ Multiple application replicas · ✅ Kubernetes Service · ✅ Readiness probes · ✅ Liveness probes · ✅ Argo Rollouts · ✅ Progressive traffic shifting · ✅ Istio traffic management · ✅ Controlled rollout progression

Traffic is shifted **gradually**, never by replacing all pods simultaneously.

<br>

## 1️⃣7️⃣ Blue-Green Deployment

Included as a supported progressive-delivery design.

```mermaid
flowchart LR
    T[🌐 Traffic] --> AS[🧭 Active Service]
    AS --> BLUE[🔵 BLUE — current version]
    BLUE -.switch traffic.-> GREEN[🟢 GREEN — new version]

    style T fill:#6366f1,color:#fff
    style AS fill:#0ea5e9,color:#fff
    style BLUE fill:#3b82f6,color:#fff
    style GREEN fill:#22c55e,color:#fff
```

`BLUE` = current version · `GREEN` = new version — traffic is switched between them atomically.

> ℹ️ **Canary** remains the primary live deployment strategy for the performance demonstration; Blue-Green is retained as a supported strategy for the project requirement.

<br>

## 1️⃣8️⃣ PostgreSQL

| Setting | Value |
|---|---|
| Database | `performance_db` |
| User | `app_user` |
| Port | `5432` |
| Persistent storage | `10Gi` (PVC) |

Deployed via Helm; data validated after restarting the database workload. Sample data includes products such as **Kubernetes Laptop** and **DevOps Monitor**.

<br>

## 1️⃣9️⃣ Redis

Used as the application caching layer, deployed via Helm with **1Gi** persistence.

```mermaid
flowchart TD
    C[📱 Client] --> F[🧩 FastAPI]
    F -->|cache hit| R[(⚡ Redis)]
    F -->|cache miss| PG[(🗄️ PostgreSQL)]

    style C fill:#6366f1,color:#fff
    style F fill:#00C7B7,color:#000
    style R fill:#DC382D,color:#fff
    style PG fill:#4169E1,color:#fff
```

<br>

## 2️⃣0️⃣ Prometheus Monitoring

Metrics exposed at `/metrics`, discovered via a Kubernetes `ServiceMonitor` (`helm/app/templates/servicemonitor.yaml`).

**Key metrics:**
- `http_requests_total`
- `http_request_duration_seconds_bucket`
- `http_request_duration_seconds_count`
- `http_request_duration_seconds_sum`

✅ Prometheus verified to scrape both application pods successfully.

<br>

## 2️⃣1️⃣ Grafana

```mermaid
flowchart LR
    A[🧩 Application] --> P[📈 Prometheus]
    P --> G[📊 Grafana]

    style A fill:#00C7B7,color:#000
    style P fill:#E6522C,color:#fff
    style G fill:#F46800,color:#fff
```

**Dashboard panels:** API request rate · HPA replica count · HPA desired replicas · P95 latency · CPU utilization

<br>

## 2️⃣2️⃣ Performance Testing

K6 load test script: `load-test/api-load.js`

```mermaid
flowchart LR
    A[10 VUs] --> B[25 VUs]
    B --> C[50 VUs]
    C --> D[0 VUs]

    style A fill:#a5b4fc,color:#000
    style B fill:#818cf8,color:#fff
    style C fill:#6366f1,color:#fff
    style D fill:#e0e7ff,color:#000
```

Validates: HTTP success rate · response latency · request throughput · application scalability · HPA behavior

<br>

## 2️⃣3️⃣ Performance Test Results

**Target:** `GET /api/products` · **Duration:** 3 minutes · **Max VUs:** 50

<div align="center">

| Metric | Result |
|---|:---:|
| 📊 Total requests | **4,144** |
| ⚡ Average throughput | **22.96 req/s** |
| ❌ HTTP failures | **0.00%** ✅ |
| ⏱️ P95 latency | **18.43 ms** |
| 👥 Maximum VUs | **50** |
| ✅ Checks passed | **100%** |

</div>

![Zero Failures](https://img.shields.io/badge/HTTP%20failures-0.00%25-brightgreen?style=for-the-badge)
![Checks](https://img.shields.io/badge/checks%20passed-100%25-brightgreen?style=for-the-badge)
![Throughput](https://img.shields.io/badge/throughput-22.96%20req%2Fs-blue?style=for-the-badge)

The application successfully handled the load **without any HTTP request failures.**

<br>

## 2️⃣4️⃣ HPA Performance During Load

```mermaid
flowchart LR
    A[2 replicas] -->|increased CPU load| B[3 replicas]

    style A fill:#94a3b8,color:#000
    style B fill:#22c55e,color:#fff
```

| Setting | Value |
|---|---|
| `minReplicas` | 2 |
| `maxReplicas` | 5 |
| CPU target | 60% |

This confirms the application **automatically scales based on CPU utilization.**

<br>

## 2️⃣5️⃣ Prometheus P95 Latency

```promql
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
```

| Source | P95 Latency |
|---|:---:|
| 📈 Prometheus (monitoring window) | ~95 ms |
| 🧪 K6 (end-to-end test run) | 18.43 ms |

> The difference is expected — the measurements come from different observation windows and measurement layers.

<br>

## 2️⃣6️⃣ CPU Monitoring

```promql
sum by (pod) (
  rate(
    container_cpu_usage_seconds_total{
      namespace="performance-platform",
      pod=~"performance-api-.*",
      cpu="total"
    }[5m]
  )
) * 100
```

Used to correlate CPU utilization directly with HPA scaling behavior.

<br>

## 2️⃣7️⃣ Health Validation

```bash
curl -i http://performance.local/health
curl -i http://performance.local/ready
curl -i http://performance.local/api/products
curl -i http://performance.local/api/products/1
```

✅ All tested endpoints returned successful responses, validated through the Istio ingress path.

<br>

## 2️⃣8️⃣ Useful Commands

<details>
<summary><b>☸️ Kubernetes</b></summary>

```bash
kubectl get nodes
kubectl get pods -n performance-platform
kubectl get rollout -n performance-platform
kubectl get hpa -n performance-platform
kubectl get svc -n performance-platform
```
</details>

<details>
<summary><b>🚀 Argo Rollouts</b></summary>

```bash
kubectl argo rollouts get rollout performance-api \
  -n performance-platform

# Watch live
kubectl argo rollouts get rollout performance-api \
  -n performance-platform \
  --watch
```
</details>

<details>
<summary><b>📦 Helm</b></summary>

```bash
helm lint helm/app
helm template performance-api helm/app
```
</details>

<details>
<summary><b>📈 Prometheus</b></summary>

```bash
kubectl port-forward \
  -n monitoring \
  svc/monitoring-kube-prometheus-prometheus \
  9090:9090
```
</details>

<details>
<summary><b>📊 Grafana</b></summary>

```bash
kubectl port-forward \
  -n monitoring \
  svc/monitoring-grafana \
  3000:80
```
</details>

<br>

## 2️⃣9️⃣ GitOps Deployment Flow

The complete lifecycle, from a code change to a stable canary rollout:

```mermaid
flowchart TD
    A[1️⃣ Developer changes application] --> B[2️⃣ git push]
    B --> C[3️⃣ GitHub Actions starts]
    C --> C1[🧪 pytest]
    C --> C2[🐳 Docker build]
    C --> C3[📤 Push image to GHCR]
    C --> C4[🔢 Generate build/version]
    C --> C5[📝 Update Helm values]
    C --> C6[✅ Commit desired state]
    C6 --> D[4️⃣ GitHub repository changes]
    D --> E[5️⃣ Argo CD detects Git change]
    E --> F[6️⃣ Argo CD renders Helm chart]
    F --> G[7️⃣ Argo Rollouts creates new ReplicaSet]
    G --> H[8️⃣ Istio controls traffic]
    H --> I[9️⃣ Canary progression]
    I --> J[🔟 New version becomes stable]

    style A fill:#6366f1,color:#fff
    style C fill:#2088FF,color:#fff
    style D fill:#24292e,color:#fff
    style E fill:#EF7B4D,color:#fff
    style F fill:#0F1689,color:#fff
    style G fill:#F4511E,color:#fff
    style H fill:#466BB0,color:#fff
    style J fill:#22c55e,color:#fff
```

<div align="center">

| Responsibility | Owner |
|---|:---:|
| 🧪 **CI** | GitHub Actions |
| 🔄 **CD** | Argo CD |
| 🚀 **Progressive Delivery** | Argo Rollouts |
| 🔀 **Traffic Management** | Istio |

</div>

<br>

---

<div align="center">

### 🎯 From commit to canary — fully automated, fully observable.

![Made with Kubernetes](https://img.shields.io/badge/built%20for-Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![GitOps](https://img.shields.io/badge/delivery-GitOps-EF7B4D?style=flat-square&logo=argo&logoColor=white)

</div>
