import os
from threading import Lock
from pymongo import MongoClient


# mongo cluster uri
MONGO_CLUSTER_URI = os.environ.get("MONGO_CLUSTER_URI", "mongodb://46.249.99.42:10107/")
# database name
DATABASE_CLUSTER_HCA = os.environ.get("DATABASE_CLUSTER_HCA", "horizontal_autoscaler")
# collection name
COLLECTION_CLUSTER_HCA = os.environ.get("COLLECTION_CLUSTER_HCA", "scaling_data")

# database name
DATABASE_CLUSTER_NAME = os.environ.get("DATABASE_CLUSTER_NAME", "jobs")
# collection name
COLLECTION_CLUSTER_NAME = os.environ.get("COLLECTION_CLUSTER_NAME", "jobs")

# horizontal autoscaler database
client_hca = MongoClient(MONGO_CLUSTER_URI)
db_hca = client_hca[DATABASE_CLUSTER_HCA]
scaling_data = db_hca[COLLECTION_CLUSTER_HCA]

# cluster database
client_cluster = MongoClient(MONGO_CLUSTER_URI)
db_cluster = client_cluster[DATABASE_CLUSTER_NAME]
collection_cluster = db_cluster[COLLECTION_CLUSTER_NAME]

mongo_lock = Lock()


def set_scaling_config(service_id, scaling_config):
    """
    Set the scaling config for a service in the database.
    """
    try:
        with mongo_lock:
            scaling_data.update_one({"service_id": service_id}, {"$set": scaling_config}, upsert=True)
    except Exception as e:
        print(e)


def get_scaling_config(service_id):
    """
    Get the scaling config for a service from the database.
    """
    try:
        with mongo_lock:
            result = scaling_data.find_one({"service_id": service_id})
        return result
    except Exception as e:
        print(e)
        return None


def restore_scaling_configs(scaler):
    """
    Restore the scaling configs from the database.
    """
    try:
        with mongo_lock:
            configs = list(scaling_data.find())

        for config in configs:
            service_id = config["service_id"]
            cluster_id = config["cluster_id"]
            check_interval = config.get("check_interval", 30)
            print(f"Restoring monitoring for service {service_id}")
            scaler.start_monitoring_services(service_id, config, check_interval, cluster_id)
    except Exception as e:
        print(e)


def delete_scaling_config(service_id):
    """
    Delete the scaling config for a service from the database.
    """
    try:
        with mongo_lock:
            scaling_data.delete_one({"service_id": service_id})
    except Exception as e:
        print(e)


def get_service_data(service_id):
    """
    Fetch service data from MongoDB and extract CPU and RAM usage for all instances and return the data.
    """
    try:
        service_data = collection_cluster.find_one({"system_job_id": service_id})

        if not service_data:
            print(f"No data found for service_id: {service_id}")

        instance_list = service_data.get("instance_list", [])
        cpu_usage = [float(instance.get("cpu", 0)) for instance in instance_list]
        ram_usage = [float(instance.get("memory", 0)) for instance in instance_list]

        return {
            "cpu_per_container": cpu_usage,
            "ram_per_container": ram_usage,
            "replica_count": len(instance_list),
        }

    except Exception as e:
        print(f"Error fetching service data: {e}")