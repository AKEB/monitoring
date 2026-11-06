# Monitoring Project Documentation

![Logo](images/icon.png)

- Server
![Docker Pulls](https://img.shields.io/docker/pulls/akeb/monitoring) ![Docker Image Size](https://img.shields.io/docker/image-size/akeb/monitoring/latest) ![Docker Version](https://img.shields.io/docker/v/akeb/monitoring) ![Docker Stars](https://img.shields.io/docker/stars/akeb/monitoring) ![License](https://img.shields.io/badge/license-AGPLv3-blue)

- Worker
![Docker Pulls](https://img.shields.io/docker/pulls/akeb/monitoring-worker-go) ![Docker Image Size](https://img.shields.io/docker/image-size/akeb/monitoring-worker-go/latest) ![Docker Version](https://img.shields.io/docker/v/akeb/monitoring-worker-go) ![Docker Stars](https://img.shields.io/docker/stars/akeb/monitoring-worker-go) ![License](https://img.shields.io/badge/license-AGPLv3-blue)

- Agent
![Docker Pulls](https://img.shields.io/docker/pulls/akeb/monitoring-agent) ![Docker Image Size](https://img.shields.io/docker/image-size/akeb/monitoring-agent/latest) ![Docker Version](https://img.shields.io/docker/v/akeb/monitoring-agent) ![Docker Stars](https://img.shields.io/docker/stars/akeb/monitoring-agent) ![License](https://img.shields.io/badge/license-AGPLv3-blue)

Monitoring is a powerful distributed monitoring system with a web interface, built on a Server / Worker / Agent architecture. Monitor websites, services, Docker containers and host metrics from geographically distributed points.

- [Website](https://akeb.github.io/monitoring/)

Docker images:
- [akeb/monitoring:latest](https://hub.docker.com/r/akeb/monitoring)
- [akeb/monitoring-worker-go:latest](https://hub.docker.com/r/akeb/monitoring-worker-go)
- [akeb/monitoring-agent:latest](https://hub.docker.com/r/akeb/monitoring-agent)

## Site map

| Page | Path |
|------|------|
| Landing | [`index.html`](index.html) |
| Docs hub | [`docs/index.html`](docs/index.html) |
| Architecture | [`docs/architecture.html`](docs/architecture.html) |
| Installation | [`docs/installation.html`](docs/installation.html) |
| Quick Start | [`docs/quick-start.html`](docs/quick-start.html) |
| Environment variables | [`docs/environment.html`](docs/environment.html) |
| Using the UI | [`docs/usage.html`](docs/usage.html) |
| Features | [`docs/features/`](docs/features/index.html) |

Russian mirrors live under [`ru/`](ru/index.html).

Regenerate HTML after content edits: `python3 _generate.py`.

## License

Dual licensing:

- **AGPLv3** — private, non-commercial use
- **Commercial License** — organizations and commercial use

Contact: [vadimakeb@gmail.com](mailto:vadimakeb@gmail.com)
