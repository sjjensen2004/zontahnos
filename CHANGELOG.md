# Changelog

## [0.0.1] - 2025-01-31
### Added
- Initial beta release with FastAPI, InfluxDB, and Grafana to service ICMP probe endpoints.

## [0.0.2] - 2025-02-01
### Added
- HashiCorp Vault to store KV secrets
- Added scripts/seed_zontahnos.py to seed vault, grafana, and influx as well as attach inlfux to grafana
- Automated the grafana API generation (Stored in vault)

## [0.0.3] - 2025-02-03
### Added
- Postgres and migrated icmp probe creation to postgres (out of influx)
- Introduced versioning to DB actions

## [0.0.4] - 2025-02-04
### Added
- Created prod, dev, and test environments 
- Added automated test coverage via pytest 
- Seeded test converage for icmp_probes