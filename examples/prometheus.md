# Prometheus config example

```yaml
scrape_configs:
  - job_name: "intel-gpu_exporter"
    scrape_interval: 5s ## Change this to the same value as REFRESH_PERIOD_MS (or remove this line)
    static_configs:
      - targets:
          - "cloud.host.example.local:8080"
```
