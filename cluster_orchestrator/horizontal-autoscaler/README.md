# Cluster Orchestrator - Horizontal Autoscaler

## Overview

The `cluster_orchestrator/horizontal-autoscaler` is a critical component of a distributed auto-scaling system, responsible for dynamically adjusting the number of service replicas within a specific cluster. This ensures optimal resource utilization and maintains application performance based on real-time metrics.

This document provides a comprehensive guide to understanding, configuring, and using the cluster-level horizontal auto-scaler.

---

## Features

- **Cluster-Specific Auto-Scaling**: Independently manages scaling within a single cluster.
- **Persistent State Storage with MongoDB**: Ensures continuity across restarts.
- **Real-Time Monitoring**: Tracks container CPU, memory, and other metrics.
- **Threshold-Based Scaling**: Adjusts replicas based on preconfigured thresholds.
- **Event-Driven Scaling**: Responds dynamically to workload spikes.
- **Auto-Recovery**: Resumes previous scaling tasks upon restart.
- **Logging and Debugging**: Provides extensive logs for monitoring and troubleshooting.

---

## Architecture

The cluster orchestrator operates at the individual cluster level and performs the following tasks:

1. **Monitors running containers** to track CPU and memory utilization.
2. **Stores and retrieves scaling configurations** from MongoDB.
3. **Decides scaling actions** based on threshold rules.
4. **Communicates with the root orchestrator**, if present, for cross-cluster coordination.
5. **Automatically recovers and resumes scaling** based on stored states.

### Components

- **Scaling Controller**: Manages decision-making for scaling up or down.
- **MongoDB Storage Layer**: Maintains persistent scaling data.
- **Container Monitor**: Collects real-time service metrics.
- **Logging Mechanism**: Records operational details for auditing and debugging.

---

## Installation

### Prerequisites

- Python 3.8+
- MongoDB

### Deployment Steps

#### 1. Clone Repository
```sh
$ git clone https://github.com/ECTLab/oakestra-hca.git
$ cd cluster_orchestrator/horizontal-autoscaler
```

#### 2. Install Dependencies
```sh
$ pip install -r requirements.txt
```

#### 3. Configure Environment Variables
```sh
export SYSTEM_MANAGER_URL=localhost
export SYSTEM_MANAGER_PORT=10000
export MY_PORT=10180
export CHECK_INTERVAL=10
export MONGO_CLUSTER_URI=mongodb://localhost:10007/
export DATABASE_CLUSTER_HCA=horizontal_autoscaler
export COLLECTION_CLUSTER_HCA=service_monitoring
```

#### 4. Start the Auto-Scaler
```sh
$ python3 horizontal_autoscaler.py
```

---

## Usage

### API Endpoints

| Method | Endpoint | Description |
|--------|-------------|-------------|
| GET | `/api/v1/hca/<service_id>` | Retrieves service data |
| POST | `/api/v1/hca/<service_id>` | Starts monitoring a service |
| PUT | `/api/v1/hca/<service_id>` | Updates monitoring configuration |
| DELETE | `/api/v1/hca/<service_id>` | Stops monitoring a service |
| POST | `/api/v1/hca/manual` | Manually scales a service |

### Example Commands

#### Retrieve Service Data
```sh
curl -X GET http://localhost:10180/api/v1/hca/<service_id>
```

#### Start Monitoring a Service
```sh
curl -X POST http://localhost:10180/api/v1/hca/<service_id> --data '{
    "cpu_threshold": 1,
    "ram_threshold": 40,
    "max_replicas": 4,
    "min_replicas": 1
}'
```

#### Update Scaling Configuration
```sh
curl -X PUT http://localhost:10180/api/v1/hca/<service_id> --data '{
    "cpu_threshold": 1,
    "ram_threshold": 40,
    "max_replicas": 8,
    "min_replicas": 1
}'
```

#### Stop Monitoring a Service
```sh
curl -X DELETE http://localhost:10180/api/v1/hca/<service_id>
```

#### Manually Scale a Service
```sh
curl -X POST http://localhost:10180/api/v1/hca/manual --data '{
    "scale_type": "up",  // could be up or down
    "service_id": "67e142b1adbe153707b38bb8",
    "cluster_id": "67dda17adea7a1ce9586ad94"
}'
```

---

## Auto-Recovery Mechanism

### How It Works
1. On startup, the orchestrator queries MongoDB for previous scaling tasks.
2. It retrieves stored scaling configurations.
3. It restarts monitoring services automatically.

---

## Monitoring and Logging

### Check Logs
```sh
$ tail -f logs/hca.log
```

### View MongoDB Records
```sh
$ mongo
> use horizontal_autoscaler
> db.service_monitoring.find()
```

---

## Conclusion

The `cluster_orchestrator/horizontal-autoscaler` ensures that Kubernetes services within a cluster dynamically adjust to fluctuating workloads. With auto-recovery, persistent storage, and real-time monitoring, it provides a reliable solution for maintaining optimal resource usage and application performance.

