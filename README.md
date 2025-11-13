# Monitoring Project Documentation

![Logo](/images/icon.png)

Monitoring is a powerful distributed monitoring system with a web interface, built on a "Server-Worker" architecture. The system allows you to monitor the availability and performance of your websites, services, and Docker containers from multiple geographically distributed points.

## Key Advantages

- **Distributed Architecture**: Deploy workers in different data centers to get an objective picture of availability.
- **Flexibility**: Monitor various types of services: HTTP(S), TCP ports, Ping, Docker containers.
- **Multi-tenancy**: Support for multiple users and groups with a role-based access control system.
- **Centralized Management**: All settings, data, and notifications are managed through a single web interface.
- **Reliable Alerts**: Intelligent notifications in Telegram and Mattermost that don't spam during partial failures.

## Architecture

The system consists of two main components:

### Server (akeb/monitoring)

- Central web server with management UI
- Stores all configurations, users, monitors, and check results
- Generates unique keys for workers
- Sends notifications

### Worker (akeb/mmonitoring-worker)

- Lightweight agent deployed on remote servers
- Periodically polls the Server to get a list of tasks (monitors) for checking
- Performs checks (HTTP requests, Ping, etc.) and sends results to the Server

## Quick Start

### 1. Install the Server

Deploy the Docker image `akeb/monitoring:latest` on your main server. Configure the database and environment variables (details in full documentation).

### 2. Create a Worker in UI

- Log in to the Server web interface
- Go to the "Workers" section
- Create a new worker. The system will generate a unique key for it

### 3. Deploy the Worker

On each server from which you want to perform monitoring, run a Docker container with the `akeb/monitoring-worker:latest` image, specifying the environment variables:

- `SERVER_URL` - URL of your Server
- `WORKER_KEY` - Unique key obtained in the previous step

Example command:

    docker run -d \
    -e SERVER_URL=https://your-monitoring-server.com \
    -e WORKER_KEY=your_unique_worker_key_here \
    akeb/monitoring-worker:latest

### 4. Create Your First Monitor

- In the web interface, go to "Monitors"
- Click "Create"
- Select the type (e.g., HTTPS), specify URL, check frequency, and select workers that should test it
- Save. You'll see the first results within a minute

## Main Features

### User and Access Management

- Authentication via built-in mechanism, OpenID Connect, or OAuth 2.0
- User groups for simplified rights management
- Detailed permission system for monitors, workers, dockers, and users

### Monitoring

- **Check Types**:
  - **Folder**: For organizing monitors in a tree structure
  - **HTTPS**: Website checking via GET or POST requests (cURL)
  - **TCP Port**: TCP port availability checking
  - **Ping**: Host availability checking via ICMP
  - **Docker**: Container status monitoring via Docker API
- **Flexible Scheduling**: Custom check frequency for each monitor
- **Status Logic**:
  - **Red**: Error from majority of workers → notification sent
  - **Yellow**: Error from some workers → warning in UI
  - **Green**: All workers reported success

### Notifications

- **Telegram**: Send to private chats, groups, and channels with thread support
- **Mattermost**: Integration via incoming webhooks

### Docker Monitoring

- Add Docker hosts via API
- Monitor container status (running/stopped) from selected workers

### Additional Features

- Audit Log: Complete history of all changes made by users in the system
- Maintenance Mode: Schedule downtime periods to exclude false error notifications

## 📄 License

This software is available under dual licensing:

- **AGPLv3** - for private, non-commercial use
- **Commercial License** - for organizations and commercial use

If you represent a company and want to use Monitoring in your infrastructure,
please purchase a commercial license. Contact us at [vadimakeb@gmail.com](mailto:vadimakeb@gmail.com)
