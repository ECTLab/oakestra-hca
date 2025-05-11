# Installing the Horizontal Autoscaler

To enable horizontal autoscaling in your cluster setup, follow these steps to update your Docker Compose files.

## Step 1: Update Your **Root Compose**

In the **root** compose file, add the following service definition:

```yaml
root_horizontal_autoscaler:
  image: docker.io/sadegh81/root-hca:v2 # or v1
  pull_policy: always
  container_name: root_horizontal_autoscaler
  hostname: root_horizontal_autoscaler
  expose:
    - "10080"
  ports:
    - "10080:10080"
  environment:
    - MY_PORT=10080
  depends_on:
    - system_manager
    - mongo_root
    - mongo_rootnet
````

## Step 2: Update Your **Cluster Compose**

In the **cluster** compose file, add the following service definition:

```yaml
cluster_horizontal_autoscaler:
  image: docker.io/sadegh81/cluster-hca:v2 # or v1
  pull_policy: always
  container_name: cluster_horizontal_autoscaler
  hostname: cluster_horizontal_autoscaler
  expose:
    - "10180"
  ports:
    - "10180:10180"
  environment:
    - MY_PORT=10180
  depends_on:
    - system_manager
    - root_horizontal_autoscaler
    - mongo_cluster
    - mongo_clusternet
```

## Notes

* If the autoscaler fails to work properly, try restarting the containers.
* This may happen because the autoscaler occasionally fails to register itself with the root orchestrator on the first run.

