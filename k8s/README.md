# Kubernetes Deployment

This directory contains Kubernetes manifests for the DevOps Performance Platform.

## Environment

The local development environment uses Minikube.

## Namespace

All application workloads are deployed into:

`performance-platform`

## Configuration

- `base/configmap.yaml` contains non-sensitive configuration.
- `base/secret.yaml` contains local credentials and is intentionally excluded from Git.
- `base/secret.example.yaml` documents the expected secret structure.

## Planned Components

- FastAPI application
- PostgreSQL
- Redis
- Kubernetes Services
- Horizontal Pod Autoscaler
- NGINX Ingress
- Canary deployment
- Prometheus monitoring
- Grafana dashboards
