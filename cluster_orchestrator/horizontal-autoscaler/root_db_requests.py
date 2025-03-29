import os
from pymongo import MongoClient
from bson.objectid import ObjectId


MONGO_ROOT_URI = os.environ.get("MONGO_ROOT_URI", "mongodb://46.249.99.42:10007/")
DATABASE_ROOT_NAME = os.environ.get("DATABASE_ROOT_NAME", "clusters")
COLLECTION_ROOT_NAME = os.environ.get("COLLECTION_ROOT_NAME", "clusters")

client_root = MongoClient(MONGO_ROOT_URI)
db_root = client_root[DATABASE_ROOT_NAME]
collection = db_root[COLLECTION_ROOT_NAME]


def is_cluster_full(cluster_id):
    """
    Check if a cluster is full and return the data.
    """
    cluster_data = collection.find_one({"_id": ObjectId(cluster_id)})
    if not cluster_data:
        return False

    cpu_history = cluster_data.get("cpu_history", [])
    memory_history = cluster_data.get("memory_history", [])
    total_cpu_cores = cluster_data.get("total_cpu_cores", 0)

    if not cpu_history or not memory_history:
        return False

    last_cpu = cpu_history[-1]["value"]
    last_memory = memory_history[-1]["value"]

    return last_cpu >= (total_cpu_cores - (total_cpu_cores * 0.20)) or last_memory >= 80
    # return last_cpu >= (total_cpu_cores - (total_cpu_cores * 0.80)) or last_memory >= 80
