import requests

from flask import jsonify


def get_hca_data(cluster_ip, service_id):
    """
    Get hca data from cluster hca and return the data.
    """
    request_address = f"http://{cluster_ip}:10180/api/v1/hca/{service_id}"
    try:
        response = requests.get(request_address)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get HCA data. Status code: {response.status_code}")
            return None
    except requests.exceptions.Timeout as e:
        print(f"Timeout error getting HCA data for service {service_id}: {e}")
        return jsonify({"error": f"Timeout error getting HCA data for service {service_id}: {e}"}), 500
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error getting HCA data for service {service_id}: {e}")
        return jsonify({"error": f"Connection error getting HCA data for service {service_id}: {e}"}), 500
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error getting HCA data for service {service_id}: {e}")
        return jsonify({"error": f"HTTP error getting HCA data for service {service_id}: {e}"}), 500
    except requests.exceptions.RequestException as e:
        print(f"Request error getting HCA data for service {service_id}: {e}")
        return jsonify({"error": f"Request error getting HCA data for service {service_id}: {e}"}), 500
    except Exception as e:
        print(f"Error getting HCA data: {e}")
        return None


def post_hca_monitor_data(cluster_ip, service_id, data):
    """
    Post hca data to cluster hca and return the response.
    """
    request_address = f"http://{cluster_ip}:10180/api/v1/hca/{service_id}"
    try:
        response = requests.post(request_address, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to post HCA monitor data. Status code: {response.status_code}")
            return None
    except requests.exceptions.Timeout as e:
        print(f"Timeout error posting HCA data for service {service_id}: {e}")
        return jsonify({"error": f"Timeout error posting HCA data for service {service_id}: {e}"}), 500
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error posting HCA data for service {service_id}: {e}")
        return jsonify({"error": f"Connection error posting HCA data for service {service_id}: {e}"}), 500
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error posting HCA data for service {service_id}: {e}")
        return jsonify({"error": f"HTTP error posting HCA data for service {service_id}: {e}"}), 500
    except requests.exceptions.RequestException as e:
        print(f"Request error posting HCA data for service {service_id}: {e}")
        return jsonify({"error": f"Request error posting HCA data for service {service_id}: {e}"}), 500
    except Exception as e:
        print(f"Error posting HCA monitor data: {e}")
        return None


def delete_hca_monitor_data(cluster_ip, service_id):
    """
    Delete hca data from cluster hca and return the response.
    """
    request_address = f"http://{cluster_ip}:10180/api/v1/hca/{service_id}"
    try:
        response = requests.delete(request_address)
        return response.json()
    
    except requests.exceptions.Timeout as e:
        print(f"Timeout error deleting HCA data for service {service_id}: {e}")
        return jsonify({"error": f"Timeout error deleting HCA data for service {service_id}: {e}"}), 500
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error deleting HCA data for service {service_id}: {e}")
        return jsonify({"error": f"Connection error deleting HCA data for service {service_id}: {e}"}), 500
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error deleting HCA data for service {service_id}: {e}")
        return jsonify({"error": f"HTTP error deleting HCA data for service {service_id}: {e}"}), 500
    except requests.exceptions.RequestException as e:
        print(f"Request error deleting HCA data for service {service_id}: {e}")
        return jsonify({"error": f"Request error deleting HCA data for service {service_id}: {e}"}), 500
    except Exception as e:
        print(f"Error deleting HCA monitor data: {e}")


def put_hca_monitor_data(cluster_ip, service_id, data):
    """
    Put hca data to cluster hca and return the response.
    """
    request_address = f"http://{cluster_ip}:10180/api/v1/hca/{service_id}"
    try:
        response = requests.put(request_address, json=data)
        return response.json()
    
    except requests.exceptions.Timeout as e:
        print(f"Timeout error putting HCA data for service {service_id}: {e}")
        return jsonify({"error": f"Timeout error putting HCA data for service {service_id}: {e}"}), 500
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error putting HCA data for service {service_id}: {e}")
        return jsonify({"error": f"Connection error putting HCA data for service {service_id}: {e}"}), 500
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error putting HCA data for service {service_id}: {e}")
        return jsonify({"error": f"HTTP error putting HCA data for service {service_id}: {e}"}), 500
    except requests.exceptions.RequestException as e:
        print(f"Request error putting HCA data for service {service_id}: {e}")
        return jsonify({"error": f"Request error putting HCA data for service {service_id}: {e}"}), 500
    except Exception as e:
        print(f"Error putting HCA monitor data: {e}")


def post_manual_scale(cluster_ip, data):
    """
    Post manual scale data to cluster hca and return the response.
    """
    request_address = f"http://{cluster_ip}:10180/api/v1/hca/manual"
    try:
        response = requests.post(request_address, json=data)
        return response.json(), response.status_code

    except requests.exceptions.Timeout as e:
        print(f"Timeout error posting manual scale for service {service_id}: {e}")
        return jsonify({"error": f"Timeout error posting manual scale for service {service_id}: {e}"}), 500
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error posting manual scale for service {service_id}: {e}")
        return jsonify({"error": f"Connection error posting manual scale for service {service_id}: {e}"}), 500
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error posting manual scale for service {service_id}: {e}")
        return jsonify({"error": f"HTTP error posting manual scale for service {service_id}: {e}"}), 500
    except requests.exceptions.RequestException as e:
        print(f"Request error posting manual scale for service {service_id}: {e}")
        return jsonify({"error": f"Request error posting manual scale for service {service_id}: {e}"}), 500
    except Exception as e:
        print(f"Error posting manual scale: {e}")