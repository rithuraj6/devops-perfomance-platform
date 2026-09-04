# k6 Performance Test Report

## Test Environment

- Application: DevOps Performance Platform API
- Load-testing tool: k6
- Target: `http://performance.local:30900/api/products`
- Test type: staged load test
- Maximum virtual users: 50
- Test duration: approximately 3 minutes
- Kubernetes environment: local multi-node Minikube cluster
- Monitoring: Prometheus and Grafana

## Load Profile

| Stage | Duration | Target VUs |
|---|---:|---:|
| Ramp up | 30s | 10 |
| Ramp up | 60s | 25 |
| Ramp up | 60s | 50 |
| Ramp down | 30s | 0 |

## Results

| Metric | Result |
|---|---:|
| Total HTTP requests | 4,169 |
| Throughput | 23.10 req/s |
| HTTP failures | 0.00% |
| Successful checks | 4,169 / 4,169 (100%) |
| Average latency | 1.89 ms |
| Median latency | 1.67 ms |
| P90 latency | 2.29 ms |
| P95 latency | 2.64 ms |
| Maximum latency | 60.72 ms |
| Maximum VUs | 50 |
| Data received | 1.2 MB |
| Data sent | 379 kB |

## Thresholds

The k6 thresholds configured for the test were satisfied:

- `http_req_duration`: P95 < 1000 ms — **PASS** (`2.64 ms`)
- `http_req_failed`: failure rate < 1% — **PASS** (`0.00%`)

## Observations

1. The API maintained a 100% successful response rate during the staged load test.
2. P95 latency remained very low at 2.64 ms, well below the 1000 ms threshold.
3. The maximum observed latency was 60.72 ms, indicating a small number of slower requests while the overall latency distribution remained low.
4. The test reached 50 concurrent virtual users without request failures.
5. Grafana/HPA monitoring showed the API operating with 2 replicas during the observed test period; the CPU target was not exceeded sufficiently to trigger additional replicas.
6. The `/api/products` endpoint is cache-backed by Redis, which contributes to the low response latency observed in this test.

## Conclusion

The tested API handled the configured 50-VU staged load successfully with zero request failures and a P95 latency of 2.64 ms. The k6 performance thresholds were passed.

These results represent the tested local Minikube environment and should not be interpreted as equivalent to production or cloud-scale capacity.
