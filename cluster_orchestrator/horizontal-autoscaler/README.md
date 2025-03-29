# Cluster Orchestrator - Horizontal Autoscaler

## Overview

The `cluster_orchestrator/horizontal-autoscaler` is a Kubernetes-native service responsible for monitoring and managing service scaling within a single cluster. It dynamically adjusts the number of service replicas based on real-time CPU, memory, and custom metrics.

This document provides an in-depth guide on the functionality, setup, and operation of the cluster-level horizontal auto-scaler.

---

## Features

- **Per-Cluster Auto-Scaling**: Adjusts replicas within a single Kubernetes cluster.
- **Persistence with MongoDB**: Stores scaling configurations and historical data.
- **Threshold-Based Scaling**: Uses CPU and memory thresholds to scale services.
- **Auto-Recovery**: Restores scaling configurations on restart.
- **Cluster-Wide Load Balancing**: Distributes workloads efficiently.
- **Event-Driven Scaling**: Reacts to workload surges dynamically.
- **Concurrency Management**: Uses multi-threading for efficient monitoring.

---

## Architecture

The cluster orchestrator operates as follows:

1. **Collects Metrics** from monitored services.
2. **Analyzes Thresholds** to determine scaling actions.
3. **Communicates with Kubernetes** to scale services.
4. **Persists Scaling Data** in MongoDB for recovery.
5. **Reinstates Scaling Operations** after restarts.

### Components

- **Service Monitor**: Collects and processes service metrics.
- **Scaling Decision Engine**: Determines when to scale services up or down.
- **MongoDB Storage**: Stores configurations and operational state.
- **Kubernetes Controller**: Interacts with Kubernetes API to modify replicas.
- **Recovery Mechanism**: Restores previously running auto-scalers.

---

## Installation

### Prerequisites

- Kubernetes cluster
- Python 3.8+
- MongoDB instance
- Helm for Kubernetes deployment
- Docker & Kubernetes CLI

### Deployment Steps

#### 1. Clone Repository
```sh
$ git clone https://github.com/your-repo/cluster_orchestrator/horizontal-autoscaler.git
$ cd cluster_orchestrator/horizontal-autoscaler
```

#### 2. Install Dependencies
```sh
$ pip install -r requirements.txt
```

#### 3. Configure Environment Variables
```sh
export MONGO_URI="mongodb://localhost:27017"
export KUBERNETES_CONFIG="~/.kube/config"
```

#### 4. Deploy to Kubernetes
```sh
$ kubectl apply -f deployment.yaml
```

#### 5. Start the Auto-Scaler
```sh
$ python main.py
```

---

## Usage

### Start Monitoring a Service
```sh
curl -X POST http://localhost:5000/start-scaling -d '{ "service_id": "web-app", "cpu_threshold": 75, "ram_threshold": 80, "max_replicas": 10, "min_replicas": 2 }'
```

### Stop Monitoring a Service
```sh
curl -X POST http://localhost:5000/stop-scaling -d '{ "service_id": "web-app" }'
```

### Check Scaling Status
```sh
curl -X GET http://localhost:5000/status
```

---

## Auto-Recovery Mechanism

### How It Works
1. On startup, the orchestrator queries MongoDB for active scaling services.
2. It retrieves saved scaling configurations.
3. It automatically restarts monitoring for previously managed services.

### Manual Recovery
If auto-recovery fails, restart monitoring manually:
```sh
$ python recover.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|-------------|-------------|
| POST | `/start-scaling` | Starts monitoring a service |
| POST | `/stop-scaling` | Stops monitoring a service |
| GET | `/status` | Retrieves the current scaling status |

---

## Monitoring and Logging

### Check Logs
```sh
$ tail -f logs/autoscaler.log
```

### View MongoDB Records
```sh
$ mongo
> use autoscaler_db
> db.scaling_configs.find()
```

---

## Conclusion

The `cluster_orchestrator/horizontal-autoscaler` is a critical component in ensuring optimal resource allocation within Kubernetes clusters. Its ability to automatically adjust workloads, persist scaling data, and restore operations makes it a powerful tool for maintaining service efficiency and availability.

For additional support, open an issue on GitHub or contact the development team.


