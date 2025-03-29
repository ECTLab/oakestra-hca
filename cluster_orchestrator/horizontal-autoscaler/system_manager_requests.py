import os
import json
import requests


SYSTEM_MANAGER_ADDR = (
    "http://"
    + os.environ.get("SYSTEM_MANAGER_URL", "46.249.99.42")
    + ":"
    + str(os.environ.get("SYSTEM_MANAGER_PORT", "10000"))
)

token = None


def login_to_system_manager():
    """
    Login to the System Manager and get the token.
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
         return None
    except requests.exceptions.ConnectionError as e:
         print(f"Connection error logging in to System Manager: {e}")
         return None
    except requests.exceptions.HTTPError as e:
         print(f"HTTP error logging in to System Manager: {e}")
         return None
    except requests.exceptions.RequestException as e:
         print(f"Request error logging in to System Manager: {e}")
         return None
    except Exception as e:
        print(f"Error logging in to System Manager: {e}")
        return None
    


def manager_deploy_request(cluster_id, job_id):
    """
    Deploy a job to a cluster and return the response.
    """
    request_address = SYSTEM_MANAGER_ADDR + "/api/result/deploy"
    try:
        response = requests.post(
            request_address,
            json={"cluster_id": cluster_id, "job_id": job_id},
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            print(f"Successfully deployed job {job_id} to cluster {cluster_id}")
        elif response.status_code == 401:
            login_to_system_manager()
            manager_deploy_request(cluster_id, job_id)
        else:
            print(f"Failed to deploy job {job_id} to cluster {cluster_id}. Status code: {response.status_code}")

    except requests.exceptions.Timeout as e:
        print(f"Timeout error deploying job {job_id} to cluster {cluster_id}: {e}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error deploying job {job_id} to cluster {cluster_id}: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error deploying job {job_id} to cluster {cluster_id}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request error deploying job {job_id} to cluster {cluster_id}: {e}")
        return None
    except Exception as e:
        print(f"Error deploying job {job_id} to cluster {cluster_id}: {e}")
        return None


def delete_instance_from_service(service_id, instance_id):
    """
    Delete an instance from a service and return the response.
    """
    request_address = SYSTEM_MANAGER_ADDR + f"/api/service/{service_id}/instance/{instance_id}"
    try:
        response = requests.delete(request_address, headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            print(f"Successfully deleted instance {instance_id} from service {service_id}")
        elif response.status_code == 401:
            login_to_system_manager()
            delete_instance_from_service(service_id, instance_id)
        else:
            print(f"Failed to delete instance {instance_id} from service {service_id}. Status code: {response.status_code}")

    except requests.exceptions.Timeout as e:
        print(f"Timeout error deleting instance {instance_id} from service {service_id}: {e}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error deleting instance {instance_id} from service {service_id}: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error deleting instance {instance_id} from service {service_id}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request error deleting instance {instance_id} from service {service_id}: {e}")
        return None
    except Exception as e:
        print(f"Error deleting instance {instance_id} from service {service_id}: {e}")
        return None


def create_instance_for_service(service_id):
    """
    Create a new instance for a service and return the response.
    """
    print("Creating new instance for service...")
    request_address = SYSTEM_MANAGER_ADDR + f"/api/service/{service_id}/instance"
    try:
        response = requests.post(request_address, headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            print(f"Successfully created new instance for service {service_id}")
        elif response.status_code == 401:
            login_to_system_manager()
            create_instance_for_service(service_id)
        else:
            print(f"Failed to create instance for service {service_id}. Status code: {response.status_code}")

    except requests.exceptions.Timeout as e:
        print(f"Timeout error creating instance for service {service_id}: {e}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error creating instance for service {service_id}: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error creating instance for service {service_id}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request error creating instance for service {service_id}: {e}")
        return None
    except Exception as e:
        print(f"Error creating instance for service {service_id}: {e}")
        return None


def get_instance_list(service_id):
    """
    Get list of instances for a service from the System Manager API and return the data.
    """
    request_address = SYSTEM_MANAGER_ADDR + f"/api/service/{service_id}"
    try:
        response = requests.get(request_address, headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            service_data = response.json()
            if isinstance(service_data, str):
                service_data = json.loads(service_data)

            instance_list = service_data.get("instance_list", [])

            return [instance["instance_number"] for instance in instance_list]
        elif response.status_code == 401:
            login_to_system_manager()
            get_instance_list(service_id)
        else:
            print(f"Failed to get instances for service {service_id}. Status code: {response.status_code}")

    except requests.exceptions.Timeout as e:
        print(f"Timeout error getting instances for service {service_id}: {e}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error getting instances for service {service_id}: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error getting instances for service {service_id}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request error getting instances for service {service_id}: {e}")
        return None
    except Exception as e:
        print(f"Error getting instances for service {service_id}: {e}")
        return None


def get_service_cluster_id(service_id):
    """
    Get cluster id of a service, it will fetch all the instances and set a cluster that has most replicas in it.
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
        elif response.status_code == 401:
            login_to_system_manager()
            get_service_cluster_id(service_id)
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
        print(f"Request error getting service data: {e}")
        return None
    except Exception as e:
        print(f"Error getting service data: {e}")
        return None
