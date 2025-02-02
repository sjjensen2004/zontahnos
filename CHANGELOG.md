# Changelog

## [0.0.1] - 2025-01-31
### Added
- Initial beta release with FastAPI, InfluxDB, and Grafana to service ICMP probe endpoints.

## [0.0.2] - 2025-02-01
### Added
- HashiCorp Vault to store KV secrets
- Added scripts/seed_zontahnos.py to seed vault, grafana, and influx as well as attach inlfux to grafana
- Automated the grafana API generation (Stored in vault)