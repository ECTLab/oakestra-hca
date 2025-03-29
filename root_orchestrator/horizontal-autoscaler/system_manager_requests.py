import os
import json
import requests


SYSTEM_MANAGER_ADDR = (
    "http://"
    + os.environ.get("SYSTEM_MANAGER_URL", "46.249.99.42")
    + ":"
    + str(os.environ.get("SYSTEM_MANAGER_PORT", "10000"))
)

CLUSTER_MANAGER_ADDR = (
    "http://"
    + os.environ.get("CLUSTER_MANAGER_URL", "46.249.99.42")
    + ":"
    + str(os.environ.get("CLUSTER_MANAGER_PORT", "10105"))
)

token = None


def login_to_system_manager():
    """
    Login to the System Manager and return the token.
    """
    request_address = SYSTEM_MANAGER_ADDR + "/api/auth/login"
    try:
        response = requests.post(request_address, json={"username": "Admin", "password": "Admin"})
        if response.status_code == 200:
            global token
            token = response.json()["token"]
            print("Successfully logged in to System Manager")
        else:
            print(f"Failed to login to System Manager. Status code: {response.status_code}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout error logging in to System Manager: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error logging in to System Manager: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error logging in to System Manager: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error logging in to System Manager: {e}")
    except Exception as e:
        print(f"Error logging in to System Manager: {e}")


def deploy_request(cluster_id, job_id):
    """
    Deploy a job to a cluster and return the response.
    """
    request_address = SYSTEM_MANAGER_ADDR + "/api/result/deploy"
    try:
        requests.post(
            request_address,
            json={"cluster_id": cluster_id, "job_id": job_id},
            headers={"Authorization": f"Bearer {token}"}
        )
    except requests.exceptions.Timeout as e:
        print(f"Timeout error deploying job to cluster {cluster_id}: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error deploying job to cluster {cluster_id}: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error deploying job to cluster {cluster_id}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error deploying job to cluster {cluster_id}: {e}")
    except Exception as e:
        print(f"Error deploying job to cluster {cluster_id}: {e}")


def get_service_cluster_id(service_id):
    """
    Get cluster id of a service, it will fetch all the instances and set a cluster that has most replicas in it.
    and return the cluster id.
    """
    request_address = SYSTEM_MANAGER_ADDR + f"/api/service/{service_id}"
    try:
        response = requests.get(request_address, headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            service_data = response.json()
            instance_list = []
            if isinstance(service_data, str):
                service_data = json.loads(service_data)
            if isinstance(service_data, dict) and "instance_list" in service_data:
                instance_list = service_data["instance_list"]

            cluster_counts = {}
            for instance in instance_list:
                cluster_id = instance.get("cluster_id")
                if cluster_id:
                    cluster_counts[cluster_id] = cluster_counts.get(cluster_id, 0) + 1

            if cluster_counts:
                most_common_cluster = max(cluster_counts.items(), key=lambda x: x[1])[0]
                return most_common_cluster

            return None
        else:
            print(f"Failed to get service data. Status code: {response.status_code}")
            return None
    except requests.exceptions.Timeout as e:
        print(f"Timeout error getting service data: {e}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error getting service data: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error getting service data: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error getting service data: {e}")
        return None
    except Exception as e:
        print(f"Error getting service data: {e}")
        return None


def get_cluster_ip_by_id(cluster_id):
    """
    Get cluster ip by id and return the ip.
    """
    request_address = SYSTEM_MANAGER_ADDR + "/api/clusters"
    try:
        response = requests.get(request_address, headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            cluster_data = response.json()
            for cluster in cluster_data:
                if cluster["_id"] == cluster_id:
                    return cluster["ip"]
            return None
        else:
            print(f"Failed to get cluster data. Status code: {response.status_code}")
            return None
    
    except requests.exceptions.Timeout as e:
        print(f"Timeout error getting cluster IP for cluster {cluster_id}: {e}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error getting cluster IP for cluster {cluster_id}: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error getting cluster IP for cluster {cluster_id}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error getting cluster data: {e}")
        return None
    except Exception as e:
        print(f"Error getting cluster data: {e}")
        return None
